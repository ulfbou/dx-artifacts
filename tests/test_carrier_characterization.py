
def test_pack_explicit_stdout_and_inspect(run_dx, tmp_path):
    (tmp_path / "a.txt").write_bytes(b"alpha\n")
    r = run_dx("pack", ".", "-o", "-", cwd=tmp_path)
    assert r.returncode == 0
    assert r.stdout.startswith(b"%%DX v2.0.0\n")
    assert r.stdout.endswith(b"%%END\n")
    carrier = tmp_path / "sample.dx.txt"
    carrier.write_bytes(r.stdout)
    listed = run_dx("inspect", str(carrier), "--list", cwd=tmp_path)
    assert listed.returncode == 0
    assert listed.stdout.splitlines() == [b"a.txt"]


def test_omitted_output_is_numbered_file(run_dx, tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    r = run_dx("pack", ".", cwd=tmp_path)
    assert r.returncode == 0
    assert (tmp_path / "dx-carrier-1.dx.txt").is_file()


def test_force_conflict(run_dx, tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    out = tmp_path / "out.dx.txt"
    assert run_dx("pack", "a.txt", "-o", str(out), cwd=tmp_path).returncode == 0
    assert run_dx("pack", "a.txt", "-o", str(out), cwd=tmp_path).returncode == 5
    assert run_dx("pack", "a.txt", "-o", str(out), "--force", cwd=tmp_path).returncode == 0


def test_binary_and_newlines_round_trip(run_dx, tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "binary.bin").write_bytes(b"a\x00b\r\n")
    (source / "text.txt").write_bytes(b"x\n\n")
    carrier = tmp_path / "c.dx.txt"
    assert run_dx("pack", str(source), "-o", str(carrier), cwd=tmp_path).returncode == 0
    dest = tmp_path / "dest"
    assert run_dx("unpack", str(carrier), str(dest), cwd=tmp_path).returncode == 0
    assert (dest / "binary.bin").read_bytes() == b"a\x00b\r\n"
    assert (dest / "text.txt").read_bytes() == b"x\n\n"


def test_invalid_carrier_exit_3(run_dx, tmp_path):
    bad = tmp_path / "bad.dx.txt"
    bad.write_text("%%DX v2.0.0\n", encoding="utf-8")
    r = run_dx("inspect", str(bad), "--verify", cwd=tmp_path)
    assert r.returncode == 3
    assert b"missing %%END" in r.stderr
