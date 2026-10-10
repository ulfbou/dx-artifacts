from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tests/fixtures/source"
CARRIER = (
    ROOT / "tests/fixtures/carriers/golden/mixed.dx.txt"
)
ENVELOPE = (
    ROOT
    / "tests/fixtures/envelopes/golden/"
    "mixed.dx.envelope.txt"
)


def load_report(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_pack_carrier_report_records_exact_identity(
    run_dx,
    tmp_path,
):
    report = tmp_path / "pack-report.json"

    result = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        "-",
        "--report",
        str(report),
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stdout == CARRIER.read_bytes()
    assert result.stderr == b""

    payload = load_report(report)
    assert payload["schema_version"] == 1
    assert payload["command"] == "pack"
    assert payload["success"] is True
    assert payload["artifact"] == {
        "media_type": "application/vnd.dx.carrier",
        "format_version": "v2.0.0",
        "size": len(result.stdout),
        "sha256": hashlib.sha256(
            result.stdout
        ).hexdigest(),
    }
    assert payload["delivery"] == {
        "sink": "stdout",
        "completed": True,
        "bytes_written": len(result.stdout),
        "destination": None,
    }


def test_integrated_envelope_report_records_layers(
    run_dx,
    tmp_path,
):
    report = tmp_path / "envelope-report.json"

    result = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        "--report",
        str(report),
        cwd=tmp_path,
    )

    assert result.returncode == 0
    payload = load_report(report)

    assert payload["artifact"]["sha256"] == (
        hashlib.sha256(result.stdout).hexdigest()
    )
    assert payload["artifact"]["size"] == len(
        result.stdout
    )
    assert [
        item["media_type"]
        for item in payload["representations"]
    ] == [
        "application/vnd.dx.carrier",
        "application/zip",
    ]
    assert payload["verification"] == [
        {
            "policy": "structural",
            "passed": True,
            "layer": "carrier",
        },
        {
            "policy": "canonical",
            "passed": True,
            "layer": "envelope",
        },
    ]


def test_report_destination_does_not_change_artifact_bytes(
    run_dx,
    tmp_path,
):
    report = tmp_path / "operation.json"

    without_report = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
    )
    with_report = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        "--report",
        str(report),
        cwd=tmp_path,
    )

    assert without_report.returncode == 0
    assert with_report.returncode == 0
    assert with_report.stdout == without_report.stdout


def test_filesystem_delivery_report_is_complete(
    run_dx,
    tmp_path,
):
    artifact = tmp_path / "artifact.dx.txt"
    report = tmp_path / "operation.json"

    result = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        str(artifact),
        "--report",
        str(report),
        cwd=tmp_path,
    )

    assert result.returncode == 0
    payload = load_report(report)
    assert payload["delivery"] == {
        "sink": "filesystem",
        "completed": True,
        "bytes_written": len(artifact.read_bytes()),
        "destination": str(artifact),
    }


def test_envelope_and_unwrap_reports(
    run_dx,
    tmp_path,
):
    envelope_report = tmp_path / "envelope.json"
    unwrap_report = tmp_path / "unwrap.json"

    wrapped = run_dx(
        "envelope",
        str(CARRIER),
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        "--report",
        str(envelope_report),
        cwd=tmp_path,
    )
    unwrapped = run_dx(
        "unwrap",
        str(ENVELOPE),
        "-o",
        "-",
        "--report",
        str(unwrap_report),
        cwd=tmp_path,
    )

    assert wrapped.returncode == 0
    assert unwrapped.returncode == 0
    assert unwrapped.stdout == CARRIER.read_bytes()
    assert load_report(envelope_report)["command"] == (
        "envelope"
    )
    assert load_report(unwrap_report)["command"] == (
        "unwrap"
    )


def test_artifact_and_report_collision_is_rejected(
    run_dx,
    tmp_path,
):
    output = tmp_path / "same.json"

    result = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        str(output),
        "--report",
        str(output),
        cwd=tmp_path,
    )

    assert result.returncode == 5
    assert not output.exists()


def test_requested_report_failure_is_nonzero(
    run_dx,
    tmp_path,
):
    report_parent = tmp_path / "not-a-directory"
    report_parent.write_bytes(b"x")
    report = report_parent / "report.json"

    result = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        "-",
        "--report",
        str(report),
        cwd=tmp_path,
    )

    assert result.returncode == 4


def test_report_symlink_is_rejected(
    run_dx,
    tmp_path,
):
    target = tmp_path / "target.json"
    target.write_text("original", encoding="utf-8")
    report = tmp_path / "report.json"

    try:
        report.symlink_to(target)
    except (NotImplementedError, OSError):
        return

    result = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        "-",
        "--report",
        str(report),
        cwd=tmp_path,
    )

    assert result.returncode == 4
    assert target.read_text(encoding="utf-8") == (
        "original"
    )
