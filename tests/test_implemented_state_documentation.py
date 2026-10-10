from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_MARKERS = {
    "docs/README.md": (
        "defines the target stdout-first contract and its activation boundary",
    ),
    "docs/implementation/cli-command-semantics.md": (
        "Target defaults after the applicable command and WP-10 gates pass:",
        "After the applicable command and WP-10 gates pass",
        "## 7. Target sink options",
    ),
    "docs/specifications/cli-output-contract.md": (
        "Target defaults after the applicable command and WP-10 gates pass:",
    ),
    "docs/specifications/capabilities-contract.md": (
        "Capability output is unavailable until its implementation and "
        "conformance gates pass.",
    ),
    "docs/specifications/operation-report-contract.md": (
        "Operation reports are not supported until WP-08 and its applicable "
        "conformance gate pass.",
    ),
    "docs/specifications/envelope-v1.md": (
        "Proposed prototype specification.",
    ),
    "docs/specifications/canonical-envelope-profile-v1.md": (
        "Proposed implementation profile for DX envelope v1.",
    ),
    "docs/decisions/README.md": (
        "ADR-001-envelope-is-a-separate-format.md), Proposed.",
        "ADR-003-canonical-profiles-over-low-level-options.md), Proposed.",
        "ADR-004-serialize-once-verify-exact-bytes.md), Proposed.",
    ),
}

ADR_STATUSES = {
    "docs/decisions/ADR-001-envelope-is-a-separate-format.md":
        "Accepted and implemented.",
    "docs/decisions/ADR-003-canonical-profiles-over-low-level-options.md":
        "Accepted and implemented by WP-05.",
    "docs/decisions/ADR-004-serialize-once-verify-exact-bytes.md":
        "Accepted and implemented by WP-07.",
}

REQUIRED_MARKERS = {
    "docs/README.md": (
        "defines the active stdout-first contract.",
    ),
    "docs/implementation/cli-command-semantics.md": (
        "## 7. Active sink options",
        "Input defaults to stdin and output defaults to stdout.",
    ),
    "docs/specifications/cli-output-contract.md": (
        "Accepted and active following WP-10.",
    ),
    "docs/specifications/capabilities-contract.md": (
        "Accepted and active following WP-09.",
    ),
    "docs/specifications/operation-report-contract.md": (
        "Accepted and active following WP-08.",
    ),
    "docs/specifications/envelope-v1.md": (
        "Accepted and active following WP-06 and WP-07.",
    ),
    "docs/specifications/canonical-envelope-profile-v1.md": (
        "Accepted and active following WP-05.",
    ),
    "docs/decisions/README.md": (
        "ADR-001-envelope-is-a-separate-format.md), "
        "Accepted and implemented.",
        "ADR-003-canonical-profiles-over-low-level-options.md), "
        "Accepted and implemented by WP-05.",
        "ADR-004-serialize-once-verify-exact-bytes.md), "
        "Accepted and implemented by WP-07.",
    ),
}


def test_no_implemented_capability_is_documented_as_pending() -> None:
    failures: list[str] = []

    for relative_path, markers in FORBIDDEN_MARKERS.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker in text:
                failures.append(
                    f"{relative_path}: forbidden marker: {marker!r}"
                )

    assert not failures, "\n".join(failures)


def test_implemented_capabilities_have_active_documentation() -> None:
    failures: list[str] = []

    for relative_path, markers in REQUIRED_MARKERS.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(
                    f"{relative_path}: required marker missing: {marker!r}"
                )

    for relative_path, expected_status in ADR_STATUSES.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        match = re.search(
            r"(?m)^## Status\s*\n\s*([^\n]+)",
            text,
        )
        if match is None:
            failures.append(
                f"{relative_path}: no ## Status value found"
            )
        elif match.group(1).strip() != expected_status:
            failures.append(
                f"{relative_path}: expected status "
                f"{expected_status!r}, found "
                f"{match.group(1).strip()!r}"
            )

    assert not failures, "\n".join(failures)


def test_documented_capabilities_match_runtime_advertisement() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "dx.py"), "capabilities", "--json"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr.decode(
        "utf-8",
        errors="replace",
    )
    assert result.stderr == b""

    payload = json.loads(result.stdout)

    assert payload["commands"] == [
        "pack",
        "envelope",
        "unwrap",
        "inspect",
        "verify",
        "capabilities",
    ]
    assert payload["envelope"] == {
        "read_versions": ["v1.0.0"],
        "write_version": "v1.0.0",
        "profiles": ["canonical-v1"],
    }
    assert payload["verification_policies"] == [
        "structural",
        "integrity",
        "canonical",
    ]
    assert payload["artifact_output"] == {
        "default_sink": "stdout",
        "explicit_stdout": "-",
        "filesystem_option": "-o FILE",
        "commands": ["pack", "envelope", "unwrap"],
    }
