from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


root = Path(__file__).resolve().parents[1]
manifest = json.loads(
    (root / "tests/baseline/accepted-baseline.json").read_text(
        encoding="utf-8"
    )
)
accepted = root / manifest["implementation_path"]
data = accepted.read_bytes()

checks = [
    ("accepted status", manifest["status"] == "accepted"),
    ("accepted snapshot exists", accepted.is_file()),
    ("accepted byte size", len(data) == manifest["implementation_size"]),
    (
        "accepted sha256",
        hashlib.sha256(data).hexdigest()
        == manifest["implementation_sha256"],
    ),
    (
        "WP-01 package exists",
        (root / "src/dx_artifacts/__init__.py").is_file(),
    ),
    (
        "WP-01 spool exists",
        (root / "src/dx_artifacts/_spool.py").is_file(),
    ),
    (
        "WP-02 sinks exist",
        (root / "src/dx_artifacts/sinks.py").is_file(),
    ),
    (
        "WP-03 typed errors exist",
        (root / "src/dx_artifacts/errors.py").is_file(),
    ),
    (
        "WP-03 verification results exist",
        (root / "src/dx_artifacts/verification.py").is_file(),
    ),
    (
        "WP-04 envelope reader exists",
        (root / "src/dx_artifacts/envelope.py").is_file(),
    ),
    (
        "WP-05 canonical profile exists",
        (root / "src/dx_artifacts/profiles.py").is_file(),
    ),
    (
        "WP-06 standalone commands exist",
        (
            root
            / "tests/test_wp06_standalone_envelope_cli.py"
        ).is_file(),
    ),
    (
        "WP-07 integrated transformation exists",
        (
            root
            / "tests/test_wp07_integrated_pack_envelope.py"
        ).is_file(),
    ),
    (
        "WP-08 report contracts exist",
        (
            root
            / "src/dx_artifacts/reports.py"
        ).is_file()
        and (
            root
            / "tests/test_wp08_operation_reports.py"
        ).is_file(),
    ),
    (
        "WP-09 capability discovery exists",
        (
            root
            / "src/dx_artifacts/capabilities.py"
        ).is_file()
        and (
            root
            / "tests/test_wp09_capabilities_cli.py"
        ).is_file(),
    ),
]

for name, passed in checks:
    print(("PASS" if passed else "FAIL") + ": " + name)

if not all(passed for _, passed in checks):
    raise SystemExit(1)

raise SystemExit(
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=root,
        check=False,
    ).returncode
)
