from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_stdout_and_filesystem_sinks_receive_identical_carrier_bytes(
    run_dx,
    tmp_path,
):
    source = ROOT / "tests/fixtures/source"
    output = tmp_path / "filesystem.dx.txt"

    filesystem = run_dx(
        "pack",
        str(source),
        "-o",
        str(output),
        cwd=tmp_path,
    )
    stdout = run_dx(
        "pack",
        str(source),
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert filesystem.returncode == 0
    assert stdout.returncode == 0
    assert stdout.stderr == b""
    assert output.read_bytes() == stdout.stdout


def test_filesystem_sink_preserves_conflict_exit_category(
    run_dx,
    tmp_path,
):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_bytes(b"a\n")

    output = tmp_path / "artifact.dx.txt"

    first = run_dx(
        "pack",
        str(source),
        "-o",
        str(output),
        cwd=tmp_path,
    )
    conflict = run_dx(
        "pack",
        str(source),
        "-o",
        str(output),
        cwd=tmp_path,
    )
    replacement = run_dx(
        "pack",
        str(source),
        "-o",
        str(output),
        "--force",
        cwd=tmp_path,
    )

    assert first.returncode == 0
    assert conflict.returncode == 5
    assert b"use --force" in conflict.stderr
    assert replacement.returncode == 0
