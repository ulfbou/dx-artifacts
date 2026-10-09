from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]

def test_accepted_baseline_identity():
    manifest=json.loads((ROOT/"tests/baseline/accepted-baseline.json").read_text(encoding="utf-8"))
    data=(ROOT/manifest["implementation_path"]).read_bytes()
    assert manifest["status"] == "accepted"
    assert manifest["source_repository"] == "Dx.Domain"
    assert len(data) == manifest["implementation_size"]
    assert hashlib.sha256(data).hexdigest() == manifest["implementation_sha256"]
