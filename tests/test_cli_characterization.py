import json


def test_version(run_dx):
    r = run_dx("--version")
    assert r.returncode == 0
    assert b"dx.py v2.0.0" in r.stdout
    assert r.stderr == b""


def test_help(run_dx):
    r = run_dx("--help")
    assert r.returncode == 0
    assert b"DX v2.0.0 carrier utility" in r.stdout


def test_unknown_command_is_usage_error(run_dx):
    r = run_dx("unknown")
    assert r.returncode == 2
    assert b"ERROR:" in r.stderr


def test_no_arguments_preserve_dry_run(run_dx, tmp_path):
    (tmp_path / "a.txt").write_text("a\n", encoding="utf-8")
    r = run_dx(cwd=tmp_path)
    assert r.returncode == 0
    assert b"No files were written." in r.stderr
    assert not list(tmp_path.glob("*.dx.txt"))


def test_pack_dry_run_json(run_dx, tmp_path):
    (tmp_path / "a.txt").write_text("a\n", encoding="utf-8")
    r = run_dx("pack", ".", "--dry-run", "--json", cwd=tmp_path)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["schema_version"] == 3
    assert data["selected_files"] == 1
