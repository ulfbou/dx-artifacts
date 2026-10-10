"""Bounded DX envelope v1 parsing and integrity verification.

This module reads and verifies envelopes. It does not write envelopes,
publish artifacts, expose CLI commands, or claim canonical conformance.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import io
import re
import stat
import struct
import zipfile
from dataclasses import dataclass
from pathlib import PurePosixPath

from .errors import InvalidCarrierError, VerifyError


ENVELOPE_VERSION = "v1.0.0"
SUPPORTED_PROFILE = "canonical-v1"
PAYLOAD_MEDIA_TYPE = "application/zip"
PAYLOAD_ENCODING = "base64"

DEFAULT_MAX_ENVELOPE_BYTES = 64 * 1024 * 1024
DEFAULT_MAX_BASE64_LINE_BYTES = 76
DEFAULT_MAX_ZIP_BYTES = 48 * 1024 * 1024
DEFAULT_MAX_CARRIER_BYTES = 128 * 1024 * 1024
DEFAULT_MAX_COMPRESSION_RATIO = 100.0

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_UINT_RE = re.compile(r"^(0|[1-9][0-9]*)$")
_ATTR_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)="([^"]*)"')
_CARRIER_HEADER_RE = re.compile(rb"^%%DX[ \t]+([^ \t\r\n]+)")


class InvalidEnvelopeError(InvalidCarrierError):
    """Malformed envelope framing, encoding, or unsafe archive structure."""

    diagnostic_code = "envelope.invalid"
    layer = "envelope"


class EnvelopeIntegrityError(VerifyError):
    """Declared envelope integrity does not match recovered bytes."""

    diagnostic_code = "verification.integrity"
    layer = "integrity"


@dataclass(frozen=True)
class EnvelopeLimits:
    """Resource limits applied before or during envelope expansion."""

    max_envelope_bytes: int = DEFAULT_MAX_ENVELOPE_BYTES
    max_base64_line_bytes: int = DEFAULT_MAX_BASE64_LINE_BYTES
    max_zip_bytes: int = DEFAULT_MAX_ZIP_BYTES
    max_carrier_bytes: int = DEFAULT_MAX_CARRIER_BYTES
    max_compression_ratio: float = DEFAULT_MAX_COMPRESSION_RATIO

    def __post_init__(self) -> None:
        integer_limits = (
            self.max_envelope_bytes,
            self.max_base64_line_bytes,
            self.max_zip_bytes,
            self.max_carrier_bytes,
        )
        if any(value <= 0 for value in integer_limits):
            raise ValueError("envelope byte limits must be positive")
        if self.max_compression_ratio <= 0:
            raise ValueError("compression ratio limit must be positive")


@dataclass(frozen=True)
class CarrierDeclaration:
    filename: str
    version: str
    size: int
    sha256: str


@dataclass(frozen=True)
class PayloadDeclaration:
    media_type: str
    encoding: str
    size: int
    sha256: str


@dataclass(frozen=True)
class ParsedEnvelope:
    version: str
    profile: str
    carrier: CarrierDeclaration
    payload: PayloadDeclaration
    payload_lines: tuple[bytes, ...]


@dataclass(frozen=True)
class VerifiedEnvelope:
    envelope: ParsedEnvelope
    zip_size: int
    zip_sha256: str
    carrier_bytes: bytes
    carrier_size: int
    carrier_sha256: str
    parsed_carrier_version: str


def _invalid(message: str) -> InvalidEnvelopeError:
    return InvalidEnvelopeError(message)


def _integrity(message: str) -> EnvelopeIntegrityError:
    return EnvelopeIntegrityError(message)


def _parse_directive(
    line: bytes,
    directive: bytes,
    positional_version: bool = False,
) -> tuple[str | None, dict[str, str]]:
    try:
        text = line.decode("ascii")
    except UnicodeDecodeError as exc:
        raise _invalid(
            f"{directive.decode()} directive is not ASCII"
        ) from exc

    prefix = directive.decode()
    if text == prefix:
        remainder = ""
    elif text.startswith(prefix + " "):
        remainder = text[len(prefix) + 1 :]
    else:
        raise _invalid(f"expected {prefix}")

    version: str | None = None

    if positional_version:
        if not remainder:
            raise _invalid(f"{prefix} requires a version")
        version, separator, remainder = remainder.partition(" ")
        if not version:
            raise _invalid(f"{prefix} requires a version")
        if not separator:
            remainder = ""

    attrs: dict[str, str] = {}
    position = 0

    while position < len(remainder):
        match = _ATTR_RE.match(remainder, position)
        if match is None:
            raise _invalid(f"malformed attributes on {prefix}")

        key, value = match.groups()
        if key in attrs:
            raise _invalid(f"duplicate attribute {key!r} on {prefix}")
        attrs[key] = value

        position = match.end()
        if position == len(remainder):
            break
        if remainder[position] != " ":
            raise _invalid(f"malformed attributes on {prefix}")
        position += 1
        if position == len(remainder):
            raise _invalid(f"trailing space on {prefix}")

    return version, attrs


def _require_exact_attributes(
    attrs: dict[str, str],
    expected: tuple[str, ...],
    directive: str,
) -> None:
    actual = tuple(attrs)
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        unknown = sorted(set(actual) - set(expected))
        raise _invalid(
            f"{directive} attributes differ: "
            f"missing={missing} unknown={unknown}"
        )


def _parse_size(value: str, field: str, maximum: int) -> int:
    if not _UINT_RE.fullmatch(value):
        raise _invalid(f"{field} must be a non-negative decimal integer")

    result = int(value)
    if result > maximum:
        raise _invalid(
            f"{field} exceeds configured limit: {result} > {maximum}"
        )
    return result


def _parse_sha256(value: str, field: str) -> str:
    if not _SHA256_RE.fullmatch(value):
        raise _invalid(
            f"{field} must be 64 lowercase hexadecimal characters"
        )
    return value


def _validate_carrier_name(value: str) -> str:
    if not value or value in {".", ".."}:
        raise _invalid("unsafe carrier filename")

    if not value.endswith(".dx.txt"):
        raise _invalid("carrier filename must end in .dx.txt")

    if "/" in value or "\\" in value:
        raise _invalid("carrier filename must be a basename")

    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise _invalid("carrier filename contains a control character")

    if PurePosixPath(value).name != value:
        raise _invalid("unsafe carrier filename")

    return value


def parse_envelope(
    envelope_bytes: bytes,
    *,
    limits: EnvelopeLimits | None = None,
) -> ParsedEnvelope:
    """Parse DX envelope framing under explicit resource limits."""

    effective = limits or EnvelopeLimits()

    if not isinstance(envelope_bytes, bytes):
        raise TypeError("envelope input must be bytes")

    if len(envelope_bytes) > effective.max_envelope_bytes:
        raise _invalid(
            "envelope exceeds configured input limit: "
            f"{len(envelope_bytes)} > {effective.max_envelope_bytes}"
        )

    if b"\r" in envelope_bytes:
        raise _invalid("envelope framing must use LF line endings")

    if not envelope_bytes.endswith(b"\n"):
        raise _invalid("envelope must end with LF")

    lines = envelope_bytes.split(b"\n")

    if lines[-1] != b"":
        raise _invalid("invalid envelope termination")

    lines = lines[:-1]

    if len(lines) < 6:
        raise _invalid("incomplete envelope framing")

    version, header_attrs = _parse_directive(
        lines[0],
        b"%%DX-ENVELOPE",
        positional_version=True,
    )
    _require_exact_attributes(
        header_attrs,
        ("profile",),
        "%%DX-ENVELOPE",
    )

    assert version is not None

    if version != ENVELOPE_VERSION:
        raise _invalid(f"unsupported envelope version: {version}")

    profile = header_attrs["profile"]
    if profile != SUPPORTED_PROFILE:
        raise _invalid(f"unsupported envelope profile: {profile}")

    _, carrier_attrs = _parse_directive(lines[1], b"%%CARRIER")
    _require_exact_attributes(
        carrier_attrs,
        ("filename", "version", "size", "sha256"),
        "%%CARRIER",
    )

    carrier = CarrierDeclaration(
        filename=_validate_carrier_name(carrier_attrs["filename"]),
        version=carrier_attrs["version"],
        size=_parse_size(
            carrier_attrs["size"],
            "carrier size",
            effective.max_carrier_bytes,
        ),
        sha256=_parse_sha256(
            carrier_attrs["sha256"],
            "carrier sha256",
        ),
    )

    if not carrier.version or any(
        character.isspace() for character in carrier.version
    ):
        raise _invalid("invalid declared carrier version")

    _, payload_attrs = _parse_directive(lines[2], b"%%PAYLOAD")
    _require_exact_attributes(
        payload_attrs,
        ("media_type", "encoding", "size", "sha256"),
        "%%PAYLOAD",
    )

    payload = PayloadDeclaration(
        media_type=payload_attrs["media_type"],
        encoding=payload_attrs["encoding"],
        size=_parse_size(
            payload_attrs["size"],
            "payload size",
            effective.max_zip_bytes,
        ),
        sha256=_parse_sha256(
            payload_attrs["sha256"],
            "payload sha256",
        ),
    )

    if payload.media_type != PAYLOAD_MEDIA_TYPE:
        raise _invalid(
            f"unsupported payload media type: {payload.media_type}"
        )

    if payload.encoding != PAYLOAD_ENCODING:
        raise _invalid(
            f"unsupported payload encoding: {payload.encoding}"
        )

    try:
        end_payload = lines.index(b"%%ENDPAYLOAD", 3)
    except ValueError as exc:
        raise _invalid("missing %%ENDPAYLOAD") from exc

    payload_lines = tuple(lines[3:end_payload])

    if not payload_lines:
        raise _invalid("empty envelope payload")

    if any(not line for line in payload_lines):
        raise _invalid("blank Base64 payload line")

    for line in payload_lines:
        if len(line) > effective.max_base64_line_bytes:
            raise _invalid(
                "Base64 physical line exceeds configured limit: "
                f"{len(line)} > {effective.max_base64_line_bytes}"
            )

        if line != line.strip():
            raise _invalid("Base64 payload lines may not contain whitespace")

    remainder = lines[end_payload + 1 :]

    if remainder != [b"%%END"]:
        if not remainder:
            raise _invalid("missing %%END")
        if b"%%END" in remainder:
            raise _invalid("content after %%END is not allowed")
        raise _invalid("unexpected envelope directive after %%ENDPAYLOAD")

    return ParsedEnvelope(
        version=version,
        profile=profile,
        carrier=carrier,
        payload=payload,
        payload_lines=payload_lines,
    )


def _decode_payload(
    envelope: ParsedEnvelope,
    limits: EnvelopeLimits,
) -> bytes:
    encoded = b"".join(envelope.payload_lines)

    maximum_encoded = ((limits.max_zip_bytes + 2) // 3) * 4
    if len(encoded) > maximum_encoded:
        raise _invalid("encoded payload exceeds configured ZIP limit")

    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise _invalid("invalid Base64 envelope payload") from exc

    if len(decoded) > limits.max_zip_bytes:
        raise _invalid(
            "decoded ZIP exceeds configured limit: "
            f"{len(decoded)} > {limits.max_zip_bytes}"
        )

    return decoded


def _verify_exact_identity(
    data: bytes,
    declared_size: int,
    declared_sha256: str,
    label: str,
) -> tuple[int, str]:
    actual_size = len(data)
    actual_sha256 = hashlib.sha256(data).hexdigest()

    if actual_size != declared_size:
        raise _integrity(
            f"{label} size mismatch: "
            f"declared={declared_size} actual={actual_size}"
        )

    if actual_sha256 != declared_sha256:
        raise _integrity(
            f"{label} sha256 mismatch: "
            f"declared={declared_sha256} actual={actual_sha256}"
        )

    return actual_size, actual_sha256


def _validate_eocd(zip_bytes: bytes) -> None:
    signature = b"PK\x05\x06"
    position = zip_bytes.rfind(signature)

    if position < 0:
        raise _invalid("ZIP end-of-central-directory record is missing")

    if len(zip_bytes) - position < 22:
        raise _invalid("truncated ZIP end-of-central-directory record")

    comment_length = struct.unpack_from(
        "<H",
        zip_bytes,
        position + 20,
    )[0]

    expected_end = position + 22 + comment_length
    if expected_end != len(zip_bytes):
        raise _invalid("ZIP contains trailing or concatenated data")

    if comment_length != 0:
        raise _invalid("ZIP archive comments are forbidden")


def _validate_zip_entry(
    info: zipfile.ZipInfo,
    declaration: CarrierDeclaration,
    limits: EnvelopeLimits,
) -> None:
    if info.filename != declaration.filename:
        raise _invalid(
            "ZIP entry name differs from carrier declaration: "
            f"{info.filename!r}"
        )

    _validate_carrier_name(info.filename)

    if info.is_dir():
        raise _invalid("ZIP entry may not be a directory")

    if info.flag_bits & 0x1:
        raise _invalid("encrypted ZIP entries are forbidden")

    if info.comment:
        raise _invalid("ZIP entry comments are forbidden")

    if info.file_size > limits.max_carrier_bytes:
        raise _invalid(
            "ZIP carrier entry exceeds configured limit: "
            f"{info.file_size} > {limits.max_carrier_bytes}"
        )

    creator_system = info.create_system
    mode = (info.external_attr >> 16) & 0xFFFF

    if creator_system == 3 and mode:
        file_type = stat.S_IFMT(mode)
        if file_type not in {0, stat.S_IFREG}:
            raise _invalid("ZIP entry is not a regular file")

    if info.compress_type not in {
        zipfile.ZIP_STORED,
        zipfile.ZIP_DEFLATED,
    }:
        raise _invalid(
            f"unsupported ZIP compression method: {info.compress_type}"
        )

    compressed = max(info.compress_size, 1)
    ratio = info.file_size / compressed

    if ratio > limits.max_compression_ratio:
        raise _invalid(
            "ZIP compression ratio exceeds configured limit: "
            f"{ratio:.2f} > {limits.max_compression_ratio:.2f}"
        )


def _read_single_carrier(
    zip_bytes: bytes,
    declaration: CarrierDeclaration,
    limits: EnvelopeLimits,
) -> bytes:
    _validate_eocd(zip_bytes)

    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as archive:
            if archive.comment:
                raise _invalid("ZIP archive comments are forbidden")

            entries = archive.infolist()
            if len(entries) != 1:
                raise _invalid(
                    "ZIP must contain exactly one entry: "
                    f"actual={len(entries)}"
                )

            info = entries[0]
            _validate_zip_entry(info, declaration, limits)

            try:
                with archive.open(info, "r") as source:
                    chunks: list[bytes] = []
                    total = 0

                    while True:
                        chunk = source.read(1024 * 1024)
                        if not chunk:
                            break

                        total += len(chunk)
                        if total > limits.max_carrier_bytes:
                            raise _invalid(
                                "extracted carrier exceeds configured limit"
                            )
                        chunks.append(chunk)

                    carrier_bytes = b"".join(chunks)
            except (RuntimeError, NotImplementedError) as exc:
                raise _invalid(f"cannot read ZIP carrier entry: {exc}") from exc

    except InvalidEnvelopeError:
        raise
    except (
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
        OSError,
        ValueError,
    ) as exc:
        raise _invalid(f"invalid ZIP payload: {exc}") from exc

    return carrier_bytes


def carrier_version_from_bytes(carrier_bytes: bytes) -> str:
    """Read the declared carrier version without normalizing carrier bytes."""

    first_line = carrier_bytes.split(b"\n", 1)[0]

    if first_line.startswith(b"%%DX-ENVELOPE"):
        raise _invalid("nested DX envelopes are forbidden")

    match = _CARRIER_HEADER_RE.match(first_line)
    if match is None:
        raise _invalid("inner carrier lacks a valid %%DX header")

    try:
        return match.group(1).decode("ascii")
    except UnicodeDecodeError as exc:
        raise _invalid("inner carrier version is not ASCII") from exc


def verify_envelope(
    envelope_bytes: bytes,
    *,
    limits: EnvelopeLimits | None = None,
) -> VerifiedEnvelope:
    """Parse and integrity-verify one envelope without filesystem extraction."""

    effective = limits or EnvelopeLimits()
    parsed = parse_envelope(envelope_bytes, limits=effective)
    zip_bytes = _decode_payload(parsed, effective)

    zip_size, zip_sha256 = _verify_exact_identity(
        zip_bytes,
        parsed.payload.size,
        parsed.payload.sha256,
        "ZIP payload",
    )

    carrier_bytes = _read_single_carrier(
        zip_bytes,
        parsed.carrier,
        effective,
    )

    carrier_size, carrier_sha256 = _verify_exact_identity(
        carrier_bytes,
        parsed.carrier.size,
        parsed.carrier.sha256,
        "carrier",
    )

    parsed_carrier_version = carrier_version_from_bytes(carrier_bytes)

    if parsed_carrier_version != parsed.carrier.version:
        raise _integrity(
            "carrier version mismatch: "
            f"declared={parsed.carrier.version} "
            f"parsed={parsed_carrier_version}"
        )

    return VerifiedEnvelope(
        envelope=parsed,
        zip_size=zip_size,
        zip_sha256=zip_sha256,
        carrier_bytes=carrier_bytes,
        carrier_size=carrier_size,
        carrier_sha256=carrier_sha256,
        parsed_carrier_version=parsed_carrier_version,
    )
