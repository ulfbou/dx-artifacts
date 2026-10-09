from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]


def test_golden_carrier_identity():
    carrier = ROOT / "tests/fixtures/carriers/golden/mixed.dx.txt"
    expected = (ROOT / "tests/fixtures/manifests/mixed.sha256").read_text(encoding="ascii").strip()
    assert hashlib.sha256(carrier.read_bytes()).hexdigest() == expected


def test_golden_carrier_is_reproducible(run_dx, tmp_path):
    source = ROOT / "tests/fixtures/source"
    generated = tmp_path / "mixed.dx.txt"
    result = run_dx("pack", str(source), "-o", str(generated), cwd=tmp_path)
    assert result.returncode == 0
    expected = ROOT / "tests/fixtures/carriers/golden/mixed.dx.txt"
    assert generated.read_bytes() == expected.read_bytes()
