import json


def make_carrier(run_dx, tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_bytes(b"alpha\n")
    carrier = tmp_path / "c.dx.txt"
    assert run_dx("pack", str(source), "-o", str(carrier), cwd=tmp_path).returncode == 0
    return source, carrier


def test_summary_list_hashes_cat_and_json(run_dx, tmp_path):
    _, carrier = make_carrier(run_dx, tmp_path)
    summary = run_dx("inspect", str(carrier), cwd=tmp_path)
    assert summary.returncode == 0 and b"Files: 1" in summary.stdout
    listed = run_dx("inspect", str(carrier), "--list", cwd=tmp_path)
    assert listed.stdout.splitlines() == [b"a.txt"]
    hashes = run_dx("inspect", str(carrier), "--hashes", cwd=tmp_path)
    assert hashes.returncode == 0 and hashes.stdout.rstrip().endswith(b"  a.txt")
    cat = run_dx("inspect", str(carrier), "--cat", "a.txt", cwd=tmp_path)
    assert cat.returncode == 0 and cat.stdout == b"alpha\n"
    payload = json.loads(run_dx("inspect", str(carrier), "--json", cwd=tmp_path).stdout)
    assert payload["schema_version"] == 1 and payload["files"] == 1


def test_conflicting_modes_and_cat_json_fail(run_dx, tmp_path):
    _, carrier = make_carrier(run_dx, tmp_path)
    assert run_dx("inspect", str(carrier), "--list", "--hashes", cwd=tmp_path).returncode == 2
    assert run_dx("inspect", str(carrier), "--cat", "a.txt", "--json", cwd=tmp_path).returncode == 2


def test_compare_exit_categories(run_dx, tmp_path):
    source, carrier = make_carrier(run_dx, tmp_path)
    assert run_dx("inspect", str(carrier), "--compare", str(source), cwd=tmp_path).returncode == 0
    (source / "a.txt").write_text("changed", encoding="utf-8")
    result = run_dx("inspect", str(carrier), "--compare", str(source), cwd=tmp_path)
    assert result.returncode == 1 and b"M a.txt" in result.stdout


def test_invalid_verify_json_is_structured(run_dx, tmp_path):
    carrier = tmp_path / "bad.dx.txt"
    carrier.write_text("%%DX v2.0.0\n", encoding="utf-8")
    result = run_dx("inspect", str(carrier), "--verify", "--json", cwd=tmp_path)
    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["valid"] is False
