from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dx_artifacts.envelope import (
    build_canonical_envelope,
    verify_canonical_envelope,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT / "tests/fixtures/manifests/mixed-envelope.json"
)


def test_canonical_envelope_golden_identities_and_reproduction():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    carrier_path = ROOT / manifest["source_carrier"]["path"]
    zip_path = ROOT / manifest["canonical_zip"]["path"]
    payload_path = ROOT / manifest["canonical_base64"]["path"]
    envelope_path = ROOT / manifest["canonical_envelope"]["path"]

    carrier_bytes = carrier_path.read_bytes()
    zip_bytes = zip_path.read_bytes()
    payload_bytes = payload_path.read_bytes()
    envelope_bytes = envelope_path.read_bytes()

    for record, data in (
        (manifest["source_carrier"], carrier_bytes),
        (manifest["canonical_zip"], zip_bytes),
        (manifest["canonical_base64"], payload_bytes),
        (manifest["canonical_envelope"], envelope_bytes),
    ):
        assert len(data) == record["bytes"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]

    reproduced = build_canonical_envelope(
        carrier_bytes,
        carrier_name="mixed.dx.txt",
    )

    assert reproduced.zip_bytes == zip_bytes
    assert reproduced.envelope_bytes == envelope_bytes

    payload_lines = envelope_bytes.splitlines()[3:-2]
    assert b"\n".join(payload_lines) + b"\n" == payload_bytes

    verified = verify_canonical_envelope(envelope_bytes)
    assert verified.carrier_bytes == carrier_bytes


def test_canonical_envelope_reproduction_is_stable_across_repetition():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    carrier_bytes = (
        ROOT / manifest["source_carrier"]["path"]
    ).read_bytes()

    first = build_canonical_envelope(
        carrier_bytes,
        carrier_name="mixed.dx.txt",
    )
    second = build_canonical_envelope(
        carrier_bytes,
        carrier_name="mixed.dx.txt",
    )

    assert first.zip_bytes == second.zip_bytes
    assert first.envelope_bytes == second.envelope_bytes
