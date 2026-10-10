from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_wp04_adds_reader_without_writer_or_cli_activation():
    envelope_path = ROOT / "src/dx_artifacts/envelope.py"
    assert envelope_path.is_file()

    source = envelope_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    functions = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }

    assert "parse_envelope" in functions
    assert "verify_envelope" in functions

    forbidden_cli_functions = {
        "envelope_command",
        "unwrap_command",
        "verify_command",
    }
    assert not (functions & forbidden_cli_functions)

    dx_source = (ROOT / "dx.py").read_text(encoding="utf-8")
    assert "envelope_command" in dx_source
    assert "unwrap_command" in dx_source
    assert "verify_command" in dx_source
    assert "capabilities_command" not in dx_source


def test_wp04_does_not_export_an_envelope_api_yet():
    package_source = (
        ROOT / "src/dx_artifacts/__init__.py"
    ).read_text(encoding="utf-8")

    assert "__all__: tuple[str, ...] = ()" in package_source
