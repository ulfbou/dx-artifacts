from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_pr_scope_has_no_product_evolution():
    assert not (ROOT/"src/dx_artifacts").exists()
    dx=(ROOT/"dx.py").read_text(encoding="utf-8")
    assert "%%DX-ENVELOPE" not in dx
    assert "def envelope" not in dx

def test_required_governance_documents_exist():
    for rel in [
      "docs/coding-standards.md","docs/documentation-standards.md",
      "docs/migration/accepted-baseline.md","docs/implementation/baseline-import-pr-plan.md",
      "docs/conformance/baseline-characterization-matrix.md","docs/conformance/baseline-acceptance-ready.md"]:
        assert (ROOT/rel).is_file(), rel
