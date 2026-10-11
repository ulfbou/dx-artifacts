#!/usr/bin/env python3
"""WP-11 consumer-ready distribution gate."""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
VERSION = "0.1.0"
RESULTS: list[tuple[str, bool, str]] = []


def record(identifier: str, passed: bool, detail: str) -> None:
    RESULTS.append((identifier, passed, detail))
    print(
        f"{'PASS' if passed else 'FAIL'}: "
        f"{identifier}: {detail}"
    )


def command_environment() -> dict[str, str]:
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(SRC)
        if not existing
        else str(SRC) + os.pathsep + existing
    )
    return environment


def run(
    identifier: str,
    command: list[str],
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=command_environment(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    record(
        identifier,
        result.returncode == 0,
        f"exit={result.returncode}",
    )
    if result.returncode:
        sys.stdout.buffer.write(result.stdout)
        sys.stderr.buffer.write(result.stderr)
    return result


def main() -> int:
    required = [
        ROOT / "src/dx_artifacts/__main__.py",
        ROOT / "src/dx_artifacts/api.py",
        ROOT / "src/dx_artifacts/_version.py",
        ROOT / "src/dx_artifacts/_runtime.py",
        ROOT / "scripts/build-standalone.py",
        ROOT / "docs/compatibility-and-deprecation-policy.md",
        ROOT / "docs/releases/0.1.0.md",
    ]
    record(
        "WP11-001 required paths",
        all(path.is_file() for path in required),
        ", ".join(
            str(path.relative_to(ROOT))
            for path in required
        ),
    )

    pyproject = (
        ROOT / "pyproject.toml"
    ).read_text(encoding="utf-8")
    record(
        "WP11-002 software version",
        f'version = "{VERSION}"' in pyproject,
        VERSION,
    )
    record(
        "WP11-003 console entry",
        (
            'dx = '
            '"dx_artifacts.__main__:console_main"'
        ) in pyproject,
        "dx_artifacts.__main__:console_main",
    )

    sys.path.insert(0, str(SRC))
    package = importlib.import_module("dx_artifacts")
    exports = tuple(package.__all__)
    public_exports = all(
        name == "__version__" or not name.startswith("_")
        for name in exports
    )
    record(
        "WP11-004 supported API explicit",
        bool(exports) and public_exports,
        repr(exports),
    )
    record(
        "WP11-005 package release identity",
        package.__version__ == VERSION,
        package.__version__,
    )

    run(
        "WP11-006 baseline and full pytest",
        [sys.executable, "scripts/validate-baseline.py"],
    )

    with tempfile.TemporaryDirectory(
        prefix="dx-wp11-"
    ) as temporary_name:
        temporary = Path(temporary_name)
        first = temporary / "dx.py"
        second = temporary / "dx-second.py"
        manifest = temporary / "standalone.json"
        second_manifest = (
            temporary / "standalone-second.json"
        )

        build_first = run(
            "WP11-007 standalone generation",
            [
                sys.executable,
                "scripts/build-standalone.py",
                "--version",
                VERSION,
                "--output",
                str(first),
                "--manifest",
                str(manifest),
            ],
        )
        build_second = run(
            "WP11-008 repeated standalone generation",
            [
                sys.executable,
                "scripts/build-standalone.py",
                "--version",
                VERSION,
                "--output",
                str(second),
                "--manifest",
                str(second_manifest),
            ],
        )

        deterministic = (
            build_first.returncode == 0
            and build_second.returncode == 0
            and first.is_file()
            and second.is_file()
            and first.read_bytes() == second.read_bytes()
        )
        record(
            "WP11-009 standalone deterministic",
            deterministic,
            (
                hashlib.sha256(
                    first.read_bytes()
                ).hexdigest()
                if first.is_file()
                else "missing"
            ),
        )

        standalone_caps = run(
            "WP11-010 standalone capabilities",
            [
                sys.executable,
                str(first),
                "capabilities",
                "--json",
            ],
            cwd=temporary,
        )
        module_caps = run(
            "WP11-011 module capabilities",
            [
                sys.executable,
                "-m",
                "dx_artifacts",
                "capabilities",
                "--json",
            ],
        )
        repository_caps = run(
            "WP11-012 repository capabilities",
            [
                sys.executable,
                "dx.py",
                "capabilities",
                "--json",
            ],
        )

        equivalent = (
            standalone_caps.returncode == 0
            and module_caps.returncode == 0
            and repository_caps.returncode == 0
            and standalone_caps.stdout
            == module_caps.stdout
            == repository_caps.stdout
            and standalone_caps.stderr
            == module_caps.stderr
            == repository_caps.stderr
            == b""
        )
        record(
            "WP11-013 command-form equivalence",
            equivalent,
            "capabilities bytes and channels",
        )

        digest_ok = False
        if manifest.is_file() and first.is_file():
            evidence = json.loads(
                manifest.read_text(encoding="utf-8")
            )
            digest_ok = (
                evidence["software_version"] == VERSION
                and evidence["standalone"]["bytes"]
                == first.stat().st_size
                and evidence["standalone"]["sha256"]
                == hashlib.sha256(
                    first.read_bytes()
                ).hexdigest()
                and evidence["source_runtime"]["sha256"]
                == hashlib.sha256(
                    (ROOT / "dx.py").read_bytes()
                ).hexdigest()
            )
        record(
            "WP11-014 standalone provenance",
            digest_ok,
            "manifest size and SHA-256",
        )

    full_pass = all(
        passed for _, passed, _ in RESULTS
    )
    evidence_dir = ROOT / ".dx" / "wp-11"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence = {
        "schema_version": 1,
        "work_package": "WP-11",
        "software_version": VERSION,
        "success": full_pass,
        "results": [
            {
                "identifier": identifier,
                "status": (
                    "pass" if passed else "fail"
                ),
                "observed": detail,
            }
            for identifier, passed, detail in RESULTS
        ],
    }
    (
        evidence_dir / "wp-11-gate.json"
    ).write_text(
        json.dumps(
            evidence,
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0 if full_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
