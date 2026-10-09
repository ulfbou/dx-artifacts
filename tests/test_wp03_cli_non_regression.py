from __future__ import annotations

import json


def test_valid_structural_verification_preserves_cli_output(
    run_dx,
    tmp_path,
):
    carrier = tmp_path / "valid.dx.txt"
    carrier.write_bytes(b"%%DX v2.0.0\n%%END\n")

    result = run_dx(
        "inspect",
        str(carrier),
        "--verify",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stdout == b""
    assert b"Carrier structure OK" in result.stderr
    assert b"0 entries parsed successfully" in result.stderr


def test_invalid_structural_verification_preserves_exit_and_diagnostic(
    run_dx,
    tmp_path,
):
    carrier = tmp_path / "invalid.dx.txt"
    carrier.write_bytes(b"%%DX v2.0.0\n")

    result = run_dx(
        "inspect",
        str(carrier),
        "--verify",
        cwd=tmp_path,
    )

    assert result.returncode == 3
    assert result.stdout == b""
    assert b"ERROR: missing %%END" in result.stderr


def test_invalid_structural_verification_preserves_json_contract(
    run_dx,
    tmp_path,
):
    carrier = tmp_path / "invalid.dx.txt"
    carrier.write_bytes(b"%%DX v2.0.0\n")

    result = run_dx(
        "inspect",
        str(carrier),
        "--verify",
        "--json",
        cwd=tmp_path,
    )

    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["valid"] is False
    assert payload["errors"] == [
        {
            "code": "invalid_carrier",
            "message": "missing %%END",
        }
    ]
