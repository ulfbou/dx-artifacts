from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tests/fixtures/source"
CARRIER = ROOT / "tests/fixtures/carriers/golden/mixed.dx.txt"
ENVELOPE = ROOT / "tests/fixtures/envelopes/golden/mixed.dx.envelope.txt"


def test_pack_omitted_output_equals_explicit_stdout(run_dx, tmp_path):
    omitted = run_dx("pack", str(SOURCE), cwd=tmp_path)
    explicit = run_dx("pack", str(SOURCE), "-o", "-", cwd=tmp_path)
    assert omitted.returncode == explicit.returncode == 0
    assert omitted.stdout == explicit.stdout == CARRIER.read_bytes()
    assert omitted.stderr == explicit.stderr == b""
    assert not list(tmp_path.glob("dx-carrier-*.dx.txt"))


def test_integrated_envelope_omitted_output_equals_explicit_stdout(run_dx, tmp_path):
    args = ("pack", str(SOURCE), "--format", "envelope", "--carrier-name", "mixed.dx.txt")
    omitted = run_dx(*args, cwd=tmp_path)
    explicit = run_dx(*args, "-o", "-", cwd=tmp_path)
    assert omitted.returncode == explicit.returncode == 0
    assert omitted.stdout == explicit.stdout == ENVELOPE.read_bytes()
    assert omitted.stderr == explicit.stderr == b""


def test_envelope_and_unwrap_omitted_outputs_equal_explicit_stdout(run_dx, tmp_path):
    wrapped = run_dx("envelope", str(CARRIER), "--carrier-name", "mixed.dx.txt", cwd=tmp_path)
    wrapped_explicit = run_dx("envelope", str(CARRIER), "--carrier-name", "mixed.dx.txt", "-o", "-", cwd=tmp_path)
    assert wrapped.returncode == wrapped_explicit.returncode == 0
    assert wrapped.stdout == wrapped_explicit.stdout == ENVELOPE.read_bytes()
    assert wrapped.stderr == wrapped_explicit.stderr == b""
    unwrapped = run_dx("unwrap", str(ENVELOPE), cwd=tmp_path)
    unwrapped_explicit = run_dx("unwrap", str(ENVELOPE), "-o", "-", cwd=tmp_path)
    assert unwrapped.returncode == unwrapped_explicit.returncode == 0
    assert unwrapped.stdout == unwrapped_explicit.stdout == CARRIER.read_bytes()
    assert unwrapped.stderr == unwrapped_explicit.stderr == b""


def test_force_is_rejected_for_implicit_stdout(run_dx, tmp_path):
    for args in (
        ("pack", str(SOURCE), "--force"),
        ("envelope", str(CARRIER), "--force"),
        ("unwrap", str(ENVELOPE), "--force"),
    ):
        result = run_dx(*args, cwd=tmp_path)
        assert result.returncode == 2
        assert result.stdout == b""
        assert b"--force is not valid with stdout" in result.stderr


def test_filesystem_publication_remains_byte_identical(run_dx, tmp_path):
    carrier_file = tmp_path / "carrier.dx.txt"
    envelope_file = tmp_path / "artifact.dx.envelope.txt"
    unwrap_file = tmp_path / "unwrapped.dx.txt"
    assert run_dx("pack", str(SOURCE), "-o", str(carrier_file), cwd=tmp_path).returncode == 0
    assert carrier_file.read_bytes() == run_dx("pack", str(SOURCE), cwd=tmp_path).stdout
    assert run_dx("envelope", str(CARRIER), "--carrier-name", "mixed.dx.txt", "-o", str(envelope_file), cwd=tmp_path).returncode == 0
    assert envelope_file.read_bytes() == run_dx("envelope", str(CARRIER), "--carrier-name", "mixed.dx.txt", cwd=tmp_path).stdout
    assert run_dx("unwrap", str(ENVELOPE), "-o", str(unwrap_file), cwd=tmp_path).returncode == 0
    assert unwrap_file.read_bytes() == run_dx("unwrap", str(ENVELOPE), cwd=tmp_path).stdout


def test_report_remains_separate_from_default_stdout(run_dx, tmp_path):
    report = tmp_path / "operation.json"
    plain = run_dx("pack", str(SOURCE), cwd=tmp_path)
    reported = run_dx("pack", str(SOURCE), "--report", str(report), cwd=tmp_path)
    assert plain.returncode == reported.returncode == 0
    assert reported.stdout == plain.stdout
    assert reported.stderr == b""
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["delivery"]["sink"] == "stdout"
    assert payload["delivery"]["completed"] is True


def test_capabilities_advertise_stdout_default(run_dx, tmp_path):
    result = run_dx("capabilities", "--json", cwd=tmp_path)
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["artifact_output"] == {
        "default_sink": "stdout",
        "explicit_stdout": "-",
        "filesystem_option": "-o FILE",
        "commands": ["pack", "envelope", "unwrap"],
    }
