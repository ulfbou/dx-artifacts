from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_documented_library_product_matches_adr_008() -> None:
    adr = (ROOT / "docs/decisions/ADR-008-dx-artifacts-is-a-library-product.md").read_text(encoding="utf-8")
    entry = (ROOT / "docs/README.md").read_text(encoding="utf-8")
    assert "DX Artifacts is a Python library product" in adr
    assert "authoritative Python library product" in entry
    assert "no console command" in entry
    assert "no supported standalone CLI" in entry


def test_implemented_adapter_capabilities_remain_truthful_evidence() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "dx.py"), "capabilities", "--json"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert result.stderr == b""
    payload = json.loads(result.stdout)
    assert payload["carrier"]["write_version"] == "v2.0.0"
    assert payload["envelope"] == {"read_versions": ["v1.0.0"], "write_version": "v1.0.0", "profiles": ["canonical-v1"]}
    assert payload["verification_policies"] == ["structural", "integrity", "canonical"]
