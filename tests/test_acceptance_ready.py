from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_wp01_scope_has_no_product_evolution():
    package = ROOT / "src/dx_artifacts"
    assert (package / "__init__.py").is_file()
    assert (package / "_spool.py").is_file()
    assert (package / "envelope.py").is_file()
    assert (package / "profiles.py").is_file()
    assert (package / "sinks.py").is_file()
    assert (package / "errors.py").is_file()
    assert (package / "verification.py").is_file()

    dx = (ROOT / "dx.py").read_text(encoding="utf-8")
    assert "def envelope_command" in dx
    assert "def unwrap_command" in dx
    assert "def verify_command" in dx
    assert "--format" in dx


def test_accepted_monolith_is_preserved_as_immutable_evidence():
    assert (ROOT / "tests/baseline/accepted-dx.py").is_file()

def test_required_governance_documents_exist():
    for rel in [
      "docs/coding-standards.md","docs/documentation-standards.md",
      "docs/migration/accepted-baseline.md","docs/implementation/baseline-import-pr-plan.md",
      "docs/conformance/baseline-characterization-matrix.md","docs/conformance/baseline-acceptance-ready.md"]:
        assert (ROOT/rel).is_file(), rel
