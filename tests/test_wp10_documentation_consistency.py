from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_ACTIVE_MARKERS = {
    "docs/README.md": (
        "stdout-default behavior remain inactive",
    ),
    "docs/decisions/README.md": (
        "Proposed and not activated during bootstrap",
    ),
    "docs/conformance/baseline-acceptance-ready.md": (
        "Current omitted-output behavior remains numbered filesystem publication.",
    ),
    "docs/conformance/baseline-characterization-matrix.md": (
        "`PK-006` omitted output preserves numbered filesystem output",
        "`NG-001` through `NG-010` protect source identity, golden bytes, "
        "supported parsing, serialization, omitted output",
    ),
    "docs/architecture/pipeline-and-streams.md": (
        "After activation, artifact-producing commands follow:",
        "Stdout-default activation occurs only in WP-10",
    ),
    "docs/architecture/system-architecture.md": (
        "After WP-10 activation, artifact-producing commands follow this "
        "contract. Before that boundary",
    ),
    "docs/migration/README.md": (
        "Migration does not itself change carrier or envelope grammar or "
        "activate stdout-default behavior.",
    ),
    "docs/migration/bootstrap-baseline.md": (
        "does not change omitted-`-o` behavior",
    ),
}

REQUIRED_ACTIVE_MARKERS = {
    "docs/README.md": (
        "Stdout-default behavior is active following WP-10.",
    ),
    "docs/decisions/README.md": (
        "Accepted and activated by WP-10",
    ),
    "docs/decisions/ADR-002-stdout-is-the-default-output-sink.md": (
        "Accepted and activated by WP-10.",
    ),
    "docs/specifications/cli-output-contract.md": (
        "Accepted and active following WP-10.",
    ),
    "docs/implementation/cli-command-semantics.md": (
        "Accepted contract. Stdout-default behavior is active following WP-10.",
    ),
    "docs/migration/wp-10-stdout-default.md": (
        "Artifact-producing commands now select stdout when `-o` is omitted:",
    ),
    "docs/architecture/pipeline-and-streams.md": (
        "WP-10 passed its compatibility gate and activated stdout as the "
        "default artifact sink.",
    ),
    "docs/architecture/system-architecture.md": (
        "Following WP-10 activation, artifact-producing commands follow this "
        "contract:",
    ),
}

def test_wp10_documentation_contains_no_active_pre_activation_contract() -> None:
    failures: list[str] = []

    for relative_path, markers in FORBIDDEN_ACTIVE_MARKERS.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker in text:
                failures.append(
                    f"{relative_path}: forbidden marker: {marker!r}"
                )

    assert not failures, "\n".join(failures)


def test_wp10_documentation_records_the_active_contract() -> None:
    failures: list[str] = []

    for relative_path, markers in REQUIRED_ACTIVE_MARKERS.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(
                    f"{relative_path}: missing marker: {marker!r}"
                )

    assert not failures, "\n".join(failures)
