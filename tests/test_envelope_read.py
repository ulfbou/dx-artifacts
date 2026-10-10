from __future__ import annotations

import base64
import hashlib
import io
import stat
import zipfile

import pytest

from dx_artifacts.envelope import (
    EnvelopeIntegrityError,
    EnvelopeLimits,
    InvalidEnvelopeError,
    parse_envelope,
    verify_envelope,
)


CARRIER = b"%%DX v2.0.0\n%%END\n"
NAME = "carrier.dx.txt"


def make_zip(
    carrier: bytes = CARRIER,
    *,
    name: str = NAME,
    extra_entries: tuple[tuple[str, bytes], ...] = (),
    archive_comment: bytes = b"",
    entry_comment: bytes = b"",
    external_attr: int | None = None,
) -> bytes:
    output = io.BytesIO()

    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        info = zipfile.ZipInfo(name)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.comment = entry_comment
        info.create_system = 3
        info.external_attr = (
            external_attr
            if external_attr is not None
            else (stat.S_IFREG | 0o644) << 16
        )
        archive.writestr(info, carrier)

        for extra_name, extra_data in extra_entries:
            archive.writestr(extra_name, extra_data)

        archive.comment = archive_comment

    return output.getvalue()


def make_envelope(
    *,
    carrier: bytes = CARRIER,
    zip_bytes: bytes | None = None,
    filename: str = NAME,
    carrier_version: str = "v2.0.0",
    carrier_size: int | None = None,
    carrier_sha256: str | None = None,
    payload_size: int | None = None,
    payload_sha256: str | None = None,
    profile: str = "canonical-v1",
    payload_lines: list[bytes] | None = None,
) -> bytes:
    archive = (
        make_zip(carrier, name=filename)
        if zip_bytes is None
        else zip_bytes
    )

    encoded = base64.b64encode(archive)
    lines = (
        [
            encoded[index : index + 76]
            for index in range(0, len(encoded), 76)
        ]
        if payload_lines is None
        else payload_lines
    )

    return b"\n".join(
        [
            (
                b'%%DX-ENVELOPE v1.0.0 profile="'
                + profile.encode("ascii")
                + b'"'
            ),
            (
                b'%%CARRIER filename="'
                + filename.encode("utf-8")
                + b'" version="'
                + carrier_version.encode("ascii")
                + b'" size="'
                + str(
                    len(carrier)
                    if carrier_size is None
                    else carrier_size
                ).encode("ascii")
                + b'" sha256="'
                + (
                    hashlib.sha256(carrier).hexdigest()
                    if carrier_sha256 is None
                    else carrier_sha256
                ).encode("ascii")
                + b'"'
            ),
            (
                b'%%PAYLOAD media_type="application/zip" '
                b'encoding="base64" size="'
                + str(
                    len(archive)
                    if payload_size is None
                    else payload_size
                ).encode("ascii")
                + b'" sha256="'
                + (
                    hashlib.sha256(archive).hexdigest()
                    if payload_sha256 is None
                    else payload_sha256
                ).encode("ascii")
                + b'"'
            ),
            *lines,
            b"%%ENDPAYLOAD",
            b"%%END",
            b"",
        ]
    )


def test_parse_and_integrity_verify_recover_exact_carrier_bytes():
    envelope = make_envelope()

    parsed = parse_envelope(envelope)
    verified = verify_envelope(envelope)

    assert parsed.version == "v1.0.0"
    assert parsed.profile == "canonical-v1"
    assert parsed.carrier.filename == NAME
    assert verified.carrier_bytes == CARRIER
    assert verified.carrier_size == len(CARRIER)
    assert verified.carrier_sha256 == hashlib.sha256(CARRIER).hexdigest()
    assert verified.parsed_carrier_version == "v2.0.0"


@pytest.mark.parametrize(
    ("mutation", "marker"),
    [
        (
            lambda value: value.replace(
                b"%%DX-ENVELOPE v1.0.0",
                b"%%DX-ENVELOPE v9.0.0",
            ),
            "unsupported envelope version",
        ),
        (
            lambda value: value.replace(
                b'profile="canonical-v1"',
                b'profile="unknown"',
            ),
            "unsupported envelope profile",
        ),
        (
            lambda value: value.replace(
                b"%%ENDPAYLOAD\n",
                b"",
            ),
            "missing %%ENDPAYLOAD",
        ),
        (
            lambda value: value.replace(
                b"%%END\n",
                b"",
            ),
            "missing %%END",
        ),
        (
            lambda value: value + b"extra\n",
            "content after %%END",
        ),
    ],
)
def test_invalid_framing_is_rejected(mutation, marker):
    with pytest.raises(InvalidEnvelopeError, match=marker):
        parse_envelope(mutation(make_envelope()))


def test_invalid_base64_is_rejected_before_zip_processing():
    envelope = make_envelope(payload_lines=[b"%%%="])

    with pytest.raises(InvalidEnvelopeError, match="invalid Base64"):
        verify_envelope(envelope)


@pytest.mark.parametrize(
    "zip_bytes",
    [
        b"not-a-zip",
        b"PK\\x03\\x04",
        b"PK\\x05\\x06" + b"\\x00" * 10,
    ],
)
def test_malformed_zip_is_reported_as_invalid_envelope(zip_bytes):
    envelope = make_envelope(zip_bytes=zip_bytes)

    with pytest.raises(
        InvalidEnvelopeError,
        match=(
            "ZIP end-of-central-directory record is missing"
            "|truncated ZIP end-of-central-directory record"
            "|invalid ZIP payload"
        ),
    ):
        verify_envelope(envelope)


@pytest.mark.parametrize(
    ("field", "marker"),
    [
        ("payload_size", "ZIP payload size mismatch"),
        ("payload_sha256", "ZIP payload sha256 mismatch"),
        ("carrier_size", "carrier size mismatch"),
        ("carrier_sha256", "carrier sha256 mismatch"),
    ],
)
def test_independent_integrity_mismatches(field, marker):
    values = {
        "payload_size": None,
        "payload_sha256": None,
        "carrier_size": None,
        "carrier_sha256": None,
    }

    if field.endswith("size"):
        values[field] = 1
    else:
        values[field] = "0" * 64

    with pytest.raises(EnvelopeIntegrityError, match=marker):
        verify_envelope(make_envelope(**values))


def test_declared_and_parsed_carrier_versions_must_agree():
    with pytest.raises(
        EnvelopeIntegrityError,
        match="carrier version mismatch",
    ):
        verify_envelope(make_envelope(carrier_version="v1.3.1"))


@pytest.mark.parametrize(
    ("zip_bytes", "marker"),
    [
        (
            make_zip(extra_entries=(("extra.txt", b"x"),)),
            "exactly one entry",
        ),
        (
            make_zip(name="../carrier.dx.txt"),
            "differs from carrier declaration",
        ),
        (
            make_zip(name="/carrier.dx.txt"),
            "differs from carrier declaration",
        ),
        (
            make_zip(
                external_attr=(stat.S_IFLNK | 0o777) << 16,
            ),
            "not a regular file",
        ),
        (
            make_zip(archive_comment=b"comment"),
            "archive comments are forbidden",
        ),
        (
            make_zip(entry_comment=b"comment"),
            "entry comments are forbidden",
        ),
    ],
)
def test_unsafe_zip_structures_are_rejected(zip_bytes, marker):
    with pytest.raises(InvalidEnvelopeError, match=marker):
        verify_envelope(make_envelope(zip_bytes=zip_bytes))


def test_concatenated_zip_data_is_rejected():
    archive = make_zip() + b"trailing"

    with pytest.raises(
        InvalidEnvelopeError,
        match="trailing or concatenated data",
    ):
        verify_envelope(make_envelope(zip_bytes=archive))


def test_nested_envelope_payload_is_rejected():
    nested = b"%%DX-ENVELOPE v1.0.0 profile=\"canonical-v1\"\n"

    with pytest.raises(
        InvalidEnvelopeError,
        match="nested DX envelopes",
    ):
        verify_envelope(make_envelope(carrier=nested))


def test_envelope_input_limit_is_enforced():
    envelope = make_envelope()

    with pytest.raises(
        InvalidEnvelopeError,
        match="input limit",
    ):
        parse_envelope(
            envelope,
            limits=EnvelopeLimits(
                max_envelope_bytes=len(envelope) - 1,
            ),
        )


def test_base64_line_limit_is_enforced():
    envelope = make_envelope()

    with pytest.raises(
        InvalidEnvelopeError,
        match="physical line",
    ):
        parse_envelope(
            envelope,
            limits=EnvelopeLimits(
                max_base64_line_bytes=20,
            ),
        )


def test_declared_zip_and_carrier_limits_are_enforced_before_expansion():
    with pytest.raises(
        InvalidEnvelopeError,
        match="payload size exceeds",
    ):
        parse_envelope(
            make_envelope(),
            limits=EnvelopeLimits(max_zip_bytes=1),
        )

    with pytest.raises(
        InvalidEnvelopeError,
        match="carrier size exceeds",
    ):
        parse_envelope(
            make_envelope(),
            limits=EnvelopeLimits(max_carrier_bytes=1),
        )


def test_compression_ratio_limit_is_enforced():
    carrier = (
        b"%%DX v2.0.0\n"
        + b"a" * 10000
        + b"\n%%END\n"
    )

    with pytest.raises(
        InvalidEnvelopeError,
        match="compression ratio",
    ):
        verify_envelope(
            make_envelope(carrier=carrier),
            limits=EnvelopeLimits(
                max_compression_ratio=2.0,
            ),
        )


def test_reader_does_not_extract_zip_to_filesystem(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    verified = verify_envelope(make_envelope())

    assert verified.carrier_bytes == CARRIER
    assert list(tmp_path.iterdir()) == []
