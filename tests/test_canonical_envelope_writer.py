from __future__ import annotations

import base64
import hashlib
import io
import stat
import zipfile

import pytest

from dx_artifacts.envelope import (
    EnvelopeIntegrityError,
    InvalidEnvelopeError,
    build_canonical_envelope,
    verify_canonical_envelope,
)
from dx_artifacts.profiles import CANONICAL_V1


CARRIER = b"%%DX v2.0.0\n%%END\n"


def test_canonical_profile_is_immutable_and_complete():
    assert CANONICAL_V1.name == "canonical-v1"
    assert CANONICAL_V1.envelope_version == "v1.0.0"
    assert CANONICAL_V1.default_carrier_name == "carrier.dx.txt"
    assert CANONICAL_V1.base64_line_width == 76
    assert CANONICAL_V1.zip_compression == zipfile.ZIP_DEFLATED
    assert CANONICAL_V1.zip_compresslevel == 9
    assert CANONICAL_V1.zip_timestamp == (1980, 1, 1, 0, 0, 0)
    assert CANONICAL_V1.zip_create_system == 3
    assert CANONICAL_V1.zip_external_attr == (
        stat.S_IFREG | 0o644
    ) << 16
    assert CANONICAL_V1.zip_archive_comment == b""
    assert CANONICAL_V1.zip_entry_comment == b""
    assert CANONICAL_V1.zip_extra == b""

    with pytest.raises(AttributeError):
        CANONICAL_V1.name = "changed"  # type: ignore[misc]


def test_writer_preserves_exact_carrier_and_self_verifies():
    produced = build_canonical_envelope(CARRIER)
    verified = verify_canonical_envelope(produced.envelope_bytes)

    assert produced.carrier_bytes == CARRIER
    assert verified.carrier_bytes == CARRIER
    assert produced.carrier_version == "v2.0.0"
    assert produced.carrier_size == len(CARRIER)
    assert produced.carrier_sha256 == hashlib.sha256(CARRIER).hexdigest()
    assert produced.zip_size == len(produced.zip_bytes)
    assert produced.zip_sha256 == hashlib.sha256(
        produced.zip_bytes
    ).hexdigest()
    assert produced.envelope_size == len(produced.envelope_bytes)
    assert produced.envelope_sha256 == hashlib.sha256(
        produced.envelope_bytes
    ).hexdigest()


def test_repeated_production_is_byte_identical():
    first = build_canonical_envelope(CARRIER)
    second = build_canonical_envelope(CARRIER)

    assert first.zip_bytes == second.zip_bytes
    assert first.envelope_bytes == second.envelope_bytes


def test_canonical_zip_metadata_and_payload_are_exact():
    produced = build_canonical_envelope(
        CARRIER,
        carrier_name="sample.dx.txt",
    )

    with zipfile.ZipFile(io.BytesIO(produced.zip_bytes), "r") as archive:
        assert archive.comment == b""
        entries = archive.infolist()
        assert len(entries) == 1

        info = entries[0]
        assert info.filename == "sample.dx.txt"
        assert info.date_time == (1980, 1, 1, 0, 0, 0)
        assert info.create_system == 3
        assert info.compress_type == zipfile.ZIP_DEFLATED
        assert info.flag_bits & 0x1 == 0
        assert info.flag_bits & 0x8 == 0
        assert info.comment == b""
        assert info.extra == b""
        assert stat.S_IFMT(info.external_attr >> 16) == stat.S_IFREG
        assert (info.external_attr >> 16) & 0o777 == 0o644
        assert archive.read(info) == CARRIER


def test_canonical_base64_and_framing():
    produced = build_canonical_envelope(CARRIER)
    lines = produced.envelope_bytes.splitlines()

    assert lines[0] == (
        b'%%DX-ENVELOPE v1.0.0 profile="canonical-v1"'
    )
    assert lines[1].startswith(
        b'%%CARRIER filename="carrier.dx.txt" '
    )
    assert lines[2].startswith(
        b'%%PAYLOAD media_type="application/zip" '
        b'encoding="base64" '
    )
    assert lines[-2:] == [b"%%ENDPAYLOAD", b"%%END"]
    assert b"\r" not in produced.envelope_bytes
    assert produced.envelope_bytes.endswith(b"%%END\n")

    payload = lines[3:-2]
    assert payload
    assert all(len(line) == 76 for line in payload[:-1])
    assert 1 <= len(payload[-1]) <= 76
    assert base64.b64decode(b"".join(payload), validate=True) == (
        produced.zip_bytes
    )


@pytest.mark.parametrize(
    "carrier_name",
    [
        "",
        ".",
        "..",
        "carrier.txt",
        "../carrier.dx.txt",
        "/carrier.dx.txt",
        "folder/carrier.dx.txt",
        "folder\\carrier.dx.txt",
        "carrier\n.dx.txt",
    ],
)
def test_writer_rejects_unsafe_logical_names(carrier_name):
    with pytest.raises(InvalidEnvelopeError):
        build_canonical_envelope(
            CARRIER,
            carrier_name=carrier_name,
        )


@pytest.mark.parametrize(
    "carrier",
    [
        b"",
        b"%%END\n",
        b"%%DX v2.0.0\n",
        b"%%DX-ENVELOPE v1.0.0\n",
    ],
)
def test_writer_rejects_invalid_carrier_boundary(carrier):
    with pytest.raises(InvalidEnvelopeError):
        build_canonical_envelope(carrier)


def test_noncanonical_but_integrity_valid_envelope_fails_canonical_policy():
    produced = build_canonical_envelope(CARRIER)
    lines = produced.envelope_bytes.splitlines()

    payload = b"".join(lines[3:-2])
    mutated_payload_lines = [
        payload[index : index + 60]
        for index in range(0, len(payload), 60)
    ]
    mutated = b"\n".join(
        [
            *lines[:3],
            *mutated_payload_lines,
            b"%%ENDPAYLOAD",
            b"%%END",
            b"",
        ]
    )

    with pytest.raises(
        EnvelopeIntegrityError,
        match="differs from canonical-v1",
    ):
        verify_canonical_envelope(mutated)
