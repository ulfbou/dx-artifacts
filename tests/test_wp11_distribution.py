from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import dx_artifacts

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def command(*args: str) -> subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(SRC)
        if not existing
        else str(SRC) + os.pathsep + existing
    )
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_supported_api_is_explicit_and_versioned():
    assert dx_artifacts.__version__ == "0.1.0"
    assert dx_artifacts.__all__
    assert "__version__" in dx_artifacts.__all__
    assert "build_canonical_envelope" in dx_artifacts.__all__
    assert "verify_canonical_envelope" in dx_artifacts.__all__
    assert all(
        name == "__version__" or not name.startswith("_")
        for name in dx_artifacts.__all__
    )


def test_module_command_matches_repository_command():
    module = command(
        "-m",
        "dx_artifacts",
        "capabilities",
        "--json",
    )
    repository = command(
        str(ROOT / "dx.py"),
        "capabilities",
        "--json",
    )
    assert module.returncode == repository.returncode == 0
    assert module.stdout == repository.stdout
    assert module.stderr == repository.stderr == b""
    payload = json.loads(module.stdout)
    assert payload["tool"]["software_version"] == "0.1.0"


def test_wp11_policy_and_release_record_exist():
    assert (
        ROOT / "docs/compatibility-and-deprecation-policy.md"
    ).is_file()
    release = (
        ROOT / "docs/releases/0.1.0.md"
    ).read_text(encoding="utf-8")
    assert "carrier v2.0.0" in release
    assert "envelope v1.0.0" in release
    assert "canonical-v1" in release
