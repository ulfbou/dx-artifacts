from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_stdout_default_remains_documented_as_adapter_behavior() -> None:
    pipeline = (ROOT / "docs/architecture/pipeline-and-streams.md").read_text(encoding="utf-8")
    output = (ROOT / "docs/specifications/cli-output-contract.md").read_text(encoding="utf-8")
    migration = (ROOT / "docs/migration/wp-10-stdout-default.md").read_text(encoding="utf-8")
    assert "No -o supplied     → stdout" in pipeline
    assert "No -o supplied     → stdout" in output
    assert "Artifact-producing commands now select stdout" in migration


def test_stdout_contract_does_not_override_library_product_boundary() -> None:
    adr = (ROOT / "docs/decisions/ADR-008-dx-artifacts-is-a-library-product.md").read_text(encoding="utf-8")
    assert "Existing CLI behavior remains useful characterization evidence" in adr
    assert "not stable library contracts" in adr
