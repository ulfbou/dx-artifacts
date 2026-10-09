from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pack_stdout_matches_controlling_golden_bytes(run_dx, tmp_path):
    source = ROOT / "tests/fixtures/source"

    result = run_dx(
        "pack",
        str(source),
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stderr == b""
    assert result.stdout == (
        ROOT / "tests/fixtures/carriers/golden/mixed.dx.txt"
    ).read_bytes()


def test_spooled_filesystem_and_stdout_outputs_are_identical(
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
    assert output.read_bytes() == stdout.stdout


def test_omitted_output_behavior_remains_numbered(run_dx, tmp_path):
    (tmp_path / "a.txt").write_bytes(b"a\n")

    result = run_dx("pack", ".", cwd=tmp_path)

    assert result.returncode == 0
    assert result.stdout == b""
    assert (tmp_path / "dx-carrier-1.dx.txt").is_file()
