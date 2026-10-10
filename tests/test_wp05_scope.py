from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_wp05_writer_remains_present_after_wp07_activation():
    envelope_source = (
        ROOT / "src/dx_artifacts/envelope.py"
    ).read_text(encoding="utf-8")
    envelope_tree = ast.parse(envelope_source)
    envelope_functions = {
        node.name
        for node in envelope_tree.body
        if isinstance(node, ast.FunctionDef)
    }

    assert "build_canonical_envelope" in envelope_functions
    assert "verify_canonical_envelope" in envelope_functions

    profile_source = (
        ROOT / "src/dx_artifacts/profiles.py"
    ).read_text(encoding="utf-8")
    assert "CANONICAL_V1" in profile_source

    dx_source = (ROOT / "dx.py").read_text(
        encoding="utf-8"
    )

    for marker in (
        "envelope_command",
        "unwrap_command",
        "verify_command",
        "--format",
        "--envelope-profile",
        "--carrier-name",
    ):
        assert marker in dx_source

    for marker in (
        "capabilities_command",
        "--report",
    ):
        assert marker not in dx_source

    package_source = (
        ROOT / "src/dx_artifacts/__init__.py"
    ).read_text(encoding="utf-8")
    assert "__all__: tuple[str, ...] = ()" in package_source
