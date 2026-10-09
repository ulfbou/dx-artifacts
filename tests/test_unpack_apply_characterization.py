import json
import pytest


def carrier_with_files(run_dx, tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_bytes(b"alpha\n\n")
    (source / "b.bin").write_bytes(b"x\x00y")
    carrier = tmp_path / "c.dx.txt"
    assert run_dx("pack", str(source), "-o", str(carrier), cwd=tmp_path).returncode == 0
    return carrier


@pytest.mark.parametrize("command", ["unpack", "apply"])
def test_exact_extraction(run_dx, tmp_path, command):
    carrier = carrier_with_files(run_dx, tmp_path)
    dest = tmp_path / command
    result = run_dx(command, str(carrier), str(dest), cwd=tmp_path)
    assert result.returncode == 0
    assert (dest / "a.txt").read_bytes() == b"alpha\n\n"
    assert (dest / "b.bin").read_bytes() == b"x\x00y"


def test_existing_policies(run_dx, tmp_path):
    carrier = carrier_with_files(run_dx, tmp_path)
    dest = tmp_path / "dest"
    dest.mkdir()
    (dest / "a.txt").write_text("local", encoding="utf-8")
    assert run_dx("unpack", str(carrier), str(dest), cwd=tmp_path).returncode == 0
    assert (dest / "a.txt").read_text() == "local"
    assert run_dx("unpack", str(carrier), str(dest), "--existing", "fail", cwd=tmp_path).returncode == 5
    assert run_dx("unpack", str(carrier), str(dest), "--existing", "overwrite", cwd=tmp_path).returncode == 0
    assert (dest / "a.txt").read_bytes() == b"alpha\n\n"


def test_dry_run_json_does_not_mutate(run_dx, tmp_path):
    carrier = carrier_with_files(run_dx, tmp_path)
    dest = tmp_path / "dest"
    result = run_dx("unpack", str(carrier), str(dest), "--dry-run", "--json", cwd=tmp_path)
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["files_would_write"] == 2
    assert not dest.exists()


def test_readonly_entry_is_not_written(run_dx, tmp_path):
    carrier = tmp_path / "readonly.dx.txt"
    carrier.write_text(
        '%%DX v2.0.0\n%%FILE path="a.txt" readonly="true"\na\n%%ENDBLOCK\n%%END\n',
        encoding="utf-8",
    )
    dest = tmp_path / "dest"
    result = run_dx("unpack", str(carrier), str(dest), cwd=tmp_path)
    assert result.returncode == 0
    assert not (dest / "a.txt").exists()
