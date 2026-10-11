from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONTROLLING = (
    "docs/README.md",
    "docs/architecture/repository-and-package-boundaries.md",
    "docs/specifications/distribution-and-integration-contract.md",
    "docs/compatibility-and-deprecation-policy.md",
    "docs/documentation-standards.md",
)


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_adr_008_controls_the_library_product_boundary() -> None:
    adr = text("docs/decisions/ADR-008-dx-artifacts-is-a-library-product.md")
    assert "DX Artifacts is a Python library product" in adr
    assert "dx-artifacts" in adr
    assert "dx_artifacts" in adr
    assert "non-stable reference and conformance adapter" in adr
    assert "DXS" in adr
    assert "installs no `dx` or `dxs` console command" in adr
    assert "publishes no standalone CLI as a supported product form" in adr


def test_prior_product_decisions_record_partial_supersession() -> None:
    for path in (
        "docs/decisions/ADR-005-dx-artifacts-is-the-authoritative-home.md",
        "docs/decisions/ADR-006-library-core-and-cli-adapter.md",
    ):
        content = text(path)
        assert "partially superseded by ADR-008" in content
    register = text("docs/decisions/README.md")
    assert "ADR-008" in register
    assert "controlling for product identity and release forms" in register


def test_controlling_documents_expose_only_the_library_product() -> None:
    combined = "\n".join(text(path) for path in CONTROLLING)
    required = (
        "Python library product",
        "dx-artifacts",
        "dx_artifacts",
        "non-stable reference",
        "DXS",
        "no console command",
        "no supported standalone CLI",
    )
    for marker in required:
        assert marker in combined, marker


def test_controlling_documents_do_not_advertise_superseded_forms() -> None:
    forbidden = (
        "Console command  dx",
        "Installed CLI",
        "Standalone release artifact",
        "stable CLI contract",
        "canonical product command",
        "DX Artifacts is an importable Python package and a command-line product",
    )
    failures: list[str] = []
    for path in CONTROLLING:
        content = text(path)
        for marker in forbidden:
            if marker in content:
                failures.append(f"{path}: {marker}")
    assert not failures, "\n".join(failures)


def test_issue_18_does_not_change_format_identities() -> None:
    adr = text("docs/decisions/ADR-008-dx-artifacts-is-a-library-product.md")
    for marker in ("DX carrier and envelope", "canonical bytes"):
        assert marker in adr
    assert "unchanged by this decision" in adr
