"""Immutable internal envelope profile definitions."""

from __future__ import annotations

import stat
import zipfile
from dataclasses import dataclass


@dataclass(frozen=True)
class CanonicalEnvelopeProfile:
    """Complete immutable rules for canonical-v1 production."""

    name: str
    envelope_version: str
    default_carrier_name: str
    payload_media_type: str
    payload_encoding: str
    base64_line_width: int
    zip_compression: int
    zip_compresslevel: int
    zip_timestamp: tuple[int, int, int, int, int, int]
    zip_create_system: int
    zip_external_attr: int
    zip_flag_bits: int
    zip_archive_comment: bytes
    zip_entry_comment: bytes
    zip_extra: bytes


CANONICAL_V1 = CanonicalEnvelopeProfile(
    name="canonical-v1",
    envelope_version="v1.0.0",
    default_carrier_name="carrier.dx.txt",
    payload_media_type="application/zip",
    payload_encoding="base64",
    base64_line_width=76,
    zip_compression=zipfile.ZIP_DEFLATED,
    zip_compresslevel=9,
    zip_timestamp=(1980, 1, 1, 0, 0, 0),
    zip_create_system=3,
    zip_external_attr=(stat.S_IFREG | 0o644) << 16,
    zip_flag_bits=0,
    zip_archive_comment=b"",
    zip_entry_comment=b"",
    zip_extra=b"",
)
