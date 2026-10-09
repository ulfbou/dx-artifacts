import json


def plan(run_dx, tmp_path, *args):
    result = run_dx("pack", ".", "--dry-run", "--json", *args, cwd=tmp_path)
    return result, json.loads(result.stdout)


def test_default_excludes_and_disable(run_dx, tmp_path):
    (tmp_path / "keep.txt").write_text("k", encoding="utf-8")
    (tmp_path / "Thumbs.db").write_text("x", encoding="utf-8")
    result, data = plan(run_dx, tmp_path)
    assert result.returncode == 0
    selected = {item["path"] for item in data["files"]}
    assert selected == {"keep.txt"}
    result, data = plan(run_dx, tmp_path, "--no-default-excludes")
    assert result.returncode == 0
    assert {item["path"] for item in data["files"]} == {"Thumbs.db", "keep.txt"}


def test_include_exclude_and_force_include(run_dx, tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    result, data = plan(run_dx, tmp_path, "--include", "*.txt")
    assert result.returncode == 0
    assert [item["path"] for item in data["files"]] == ["a.txt"]
    result, data = plan(run_dx, tmp_path, "--exclude", "a.txt")
    assert result.returncode == 0
    assert [item["path"] for item in data["files"]] == ["b.md"]
    (tmp_path / ".dxignore").write_text("a.txt\n", encoding="utf-8")
    result, data = plan(run_dx, tmp_path, "--force-include", "a.txt")
    assert result.returncode == 0
    assert "a.txt" in {item["path"] for item in data["files"]}


def test_scope_only_and_path_provider(run_dx, tmp_path):
    (tmp_path / "one").mkdir()
    (tmp_path / "two").mkdir()
    (tmp_path / "one/a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "two/b.txt").write_text("b", encoding="utf-8")
    result = run_dx("pack", ".", "--scope", "one", "--dry-run", "--json", cwd=tmp_path)
    assert result.returncode == 0
    assert [x["path"] for x in json.loads(result.stdout)["files"]] == ["one/a.txt"]
    result = run_dx("pack", ".", "--only", "two", "--dry-run", "--json", cwd=tmp_path)
    assert result.returncode == 0
    assert [x["path"] for x in json.loads(result.stdout)["files"]] == ["two/b.txt"]


def test_empty_selection_exit_7(run_dx, tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    result = run_dx("pack", ".", "--include", "*.md", "--dry-run", "--json", cwd=tmp_path)
    assert result.returncode == 7
    assert json.loads(result.stdout)["success"] is False


def test_unsafe_include_git_requires_force(run_dx, tmp_path):
    result = run_dx("pack", ".", "--unsafe-include-git", "--dry-run", cwd=tmp_path)
    assert result.returncode == 2
    assert b"requires --force" in result.stderr


def test_operand_traversal_is_rejected(run_dx, tmp_path):
    result = run_dx("pack", ".", "--path", "../outside", "--dry-run", cwd=tmp_path)
    assert result.returncode == 2
    assert b"lexical traversal" in result.stderr
