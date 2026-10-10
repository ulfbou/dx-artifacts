from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CARRIER = (
    ROOT
    / "tests/fixtures/carriers/golden/mixed.dx.txt"
)
ENVELOPE = (
    ROOT
    / "tests/fixtures/envelopes/golden/"
    "mixed.dx.envelope.txt"
)


def test_envelope_stdout_matches_golden(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "envelope",
        str(CARRIER),
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stdout == ENVELOPE.read_bytes()
    assert result.stderr == b""


def test_envelope_filesystem_equals_stdout(
    run_dx,
    tmp_path,
):
    output = tmp_path / "output.dx.envelope.txt"

    filesystem = run_dx(
        "envelope",
        str(CARRIER),
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        str(output),
        cwd=tmp_path,
    )
    stdout = run_dx(
        "envelope",
        str(CARRIER),
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert filesystem.returncode == 0
    assert stdout.returncode == 0
    assert output.read_bytes() == stdout.stdout


def test_unwrap_stdout_is_exact(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "unwrap",
        str(ENVELOPE),
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stdout == CARRIER.read_bytes()
    assert result.stderr == b""


def test_unwrap_filesystem_is_exact(
    run_dx,
    tmp_path,
):
    output = tmp_path / "recovered.dx.txt"

    result = run_dx(
        "unwrap",
        str(ENVELOPE),
        "-o",
        str(output),
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert output.read_bytes() == CARRIER.read_bytes()


def test_stdin_pipeline_is_exact(
    run_dx,
    tmp_path,
):
    wrapped = run_dx(
        "envelope",
        "-",
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
        input_bytes=CARRIER.read_bytes(),
    )
    assert wrapped.returncode == 0
    assert wrapped.stderr == b""

    unwrapped = run_dx(
        "unwrap",
        "-",
        "-o",
        "-",
        cwd=tmp_path,
        input_bytes=wrapped.stdout,
    )
    assert unwrapped.returncode == 0
    assert unwrapped.stdout == CARRIER.read_bytes()
    assert unwrapped.stderr == b""


def test_verify_defaults_by_physical_format(
    run_dx,
    tmp_path,
):
    carrier = run_dx(
        "verify",
        str(CARRIER),
        "--json",
        cwd=tmp_path,
    )
    envelope = run_dx(
        "verify",
        str(ENVELOPE),
        "--json",
        cwd=tmp_path,
    )

    assert carrier.returncode == 0
    assert envelope.returncode == 0
    assert json.loads(carrier.stdout)["policy"] == (
        "structural"
    )
    assert json.loads(envelope.stdout)["policy"] == (
        "integrity"
    )


@pytest.mark.parametrize(
    "policy",
    ("structural", "integrity", "canonical"),
)
def test_envelope_verification_policies(
    run_dx,
    tmp_path,
    policy,
):
    result = run_dx(
        "verify",
        str(ENVELOPE),
        "--policy",
        policy,
        "--json",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stderr == b""

    payload = json.loads(result.stdout)
    assert payload["command"] == "verify"
    assert payload["format"] == "envelope"
    assert payload["policy"] == policy
    assert payload["valid"] is True


def test_carrier_rejects_nonstructural_policy(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "verify",
        str(CARRIER),
        "--policy",
        "integrity",
        cwd=tmp_path,
    )

    assert result.returncode == 2


def test_malformed_envelope_returns_invalid_artifact(
    run_dx,
    tmp_path,
):
    malformed = (
        tmp_path / "malformed.dx.envelope.txt"
    )
    malformed.write_bytes(
        b"%%DX-ENVELOPE v1.0.0\n"
    )

    result = run_dx(
        "verify",
        str(malformed),
        cwd=tmp_path,
    )

    assert result.returncode == 3


def test_integrity_mismatch_returns_verification_failure(
    run_dx,
    tmp_path,
):
    corrupted = bytearray(ENVELOPE.read_bytes())
    payload_line = corrupted.find(
        b'%%PAYLOAD media_type="application/zip"'
    )
    assert payload_line >= 0

    marker = b'sha256="'
    digest = corrupted.find(marker, payload_line)
    assert digest >= 0
    digest += len(marker)
    corrupted[digest] = (
        ord("0")
        if corrupted[digest] != ord("0")
        else ord("1")
    )

    path = tmp_path / "corrupt.dx.envelope.txt"
    path.write_bytes(bytes(corrupted))

    result = run_dx(
        "verify",
        str(path),
        cwd=tmp_path,
    )

    assert result.returncode == 6


def test_conflict_force_stdout_and_identity(
    run_dx,
    tmp_path,
):
    output = tmp_path / "result.dx.envelope.txt"
    output.write_bytes(b"existing")

    conflict = run_dx(
        "envelope",
        str(CARRIER),
        "-o",
        str(output),
        cwd=tmp_path,
    )
    assert conflict.returncode == 5
    assert output.read_bytes() == b"existing"

    replaced = run_dx(
        "envelope",
        str(CARRIER),
        "-o",
        str(output),
        "--force",
        cwd=tmp_path,
    )
    assert replaced.returncode == 0
    assert output.read_bytes().startswith(
        b"%%DX-ENVELOPE "
    )

    stdout_force = run_dx(
        "envelope",
        str(CARRIER),
        "-o",
        "-",
        "--force",
        cwd=tmp_path,
    )
    assert stdout_force.returncode == 2

    same = tmp_path / "same.dx.txt"
    same.write_bytes(CARRIER.read_bytes())

    identity = run_dx(
        "envelope",
        str(same),
        "-o",
        str(same),
        "--force",
        cwd=tmp_path,
    )
    assert identity.returncode == 5


def test_destination_symlink_is_rejected(
    run_dx,
    tmp_path,
):
    target = tmp_path / "target.dx.envelope.txt"
    target.write_bytes(b"target")

    output = tmp_path / "output.dx.envelope.txt"
    try:
        output.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("symlinks unavailable")

    result = run_dx(
        "envelope",
        str(CARRIER),
        "-o",
        str(output),
        "--force",
        cwd=tmp_path,
    )

    assert result.returncode == 5
    assert target.read_bytes() == b"target"
