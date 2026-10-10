from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tests/fixtures/source"
GOLDEN_CARRIER = (
    ROOT / "tests/fixtures/carriers/golden/mixed.dx.txt"
)


def test_integrated_envelope_equals_explicit_composition(
    run_dx,
    tmp_path,
):
    integrated = run_dx(
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
    carrier = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        "-",
        cwd=tmp_path,
    )
    explicit = run_dx(
        "envelope",
        "-",
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
        input_bytes=carrier.stdout,
    )

    assert integrated.returncode == 0
    assert carrier.returncode == 0
    assert explicit.returncode == 0
    assert integrated.stderr == b""
    assert carrier.stderr == b""
    assert explicit.stderr == b""
    assert integrated.stdout == explicit.stdout


def test_integrated_envelope_unwraps_to_exact_carrier(
    run_dx,
    tmp_path,
):
    integrated = run_dx(
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
    unwrapped = run_dx(
        "unwrap",
        "-",
        "-o",
        "-",
        cwd=tmp_path,
        input_bytes=integrated.stdout,
    )

    assert integrated.returncode == 0
    assert unwrapped.returncode == 0
    assert unwrapped.stdout == GOLDEN_CARRIER.read_bytes()


def test_integrated_stdout_and_filesystem_are_identical(
    run_dx,
    tmp_path,
):
    output = tmp_path / "integrated.dx.envelope.txt"

    filesystem = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        str(output),
        cwd=tmp_path,
    )
    stdout = run_dx(
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

    assert filesystem.returncode == 0
    assert stdout.returncode == 0
    assert output.read_bytes() == stdout.stdout


def test_integrated_omitted_output_preserves_pre_wp10_filesystem_default(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--carrier-name",
        "mixed.dx.txt",
        cwd=tmp_path,
    )
    output = (
        tmp_path / "dx-envelope-1.dx.envelope.txt"
    )

    assert result.returncode == 0
    assert result.stdout == b""
    assert output.is_file()


def test_carrier_format_remains_default_and_byte_identical(
    run_dx,
    tmp_path,
):
    implicit = run_dx(
        "pack",
        str(SOURCE),
        "-o",
        "-",
        cwd=tmp_path,
    )
    explicit = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "carrier",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert implicit.returncode == 0
    assert explicit.returncode == 0
    assert implicit.stdout == GOLDEN_CARRIER.read_bytes()
    assert explicit.stdout == implicit.stdout


def test_envelope_options_require_envelope_format(
    run_dx,
    tmp_path,
):
    profile = run_dx(
        "pack",
        str(SOURCE),
        "--envelope-profile",
        "canonical-v1",
        "-o",
        "-",
        cwd=tmp_path,
    )
    name = run_dx(
        "pack",
        str(SOURCE),
        "--carrier-name",
        "mixed.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert profile.returncode == 2
    assert name.returncode == 2


def test_unsupported_profile_is_rejected(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--envelope-profile",
        "unsupported",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert result.returncode == 2


def test_invalid_integrated_carrier_name_is_rejected(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "pack",
        str(SOURCE),
        "--format",
        "envelope",
        "--carrier-name",
        "../unsafe.dx.txt",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert result.returncode == 3


def test_wp10_remains_inactive(
    run_dx,
    tmp_path,
):
    capabilities = run_dx(
        "capabilities",
        "--json",
        cwd=tmp_path,
    )

    assert capabilities.returncode == 0
    payload = json.loads(capabilities.stdout)
    assert payload["schema_version"] == 1
    assert "stdout_default" not in json.dumps(
        payload,
        sort_keys=True,
    )

    dx_source = (ROOT / "dx.py").read_text(
        encoding="utf-8"
    )
    assert "--report" in dx_source
    assert "capabilities_command" in dx_source
