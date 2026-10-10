from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED = {
    "schema_version": 1,
    "tool": {
        "name": "dx-artifacts",
        "software_version": "0.0.0",
    },
    "carrier": {
        "read_versions": [
            "v1.3.1",
            "v2.0.0",
        ],
        "write_version": "v2.0.0",
    },
    "envelope": {
        "read_versions": ["v1.0.0"],
        "write_version": "v1.0.0",
        "profiles": ["canonical-v1"],
    },
    "verification_policies": [
        "structural",
        "integrity",
        "canonical",
    ],
    "digests": ["sha256"],
    "commands": [
        "pack",
        "envelope",
        "unwrap",
        "inspect",
        "verify",
        "capabilities",
    ],
}


def test_capabilities_json_is_exact_and_clean(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "capabilities",
        "--json",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stderr == b""
    assert result.stdout.endswith(b"\n")
    assert b"\r" not in result.stdout
    assert json.loads(result.stdout) == EXPECTED


def test_capabilities_output_is_deterministic(
    run_dx,
    tmp_path,
):
    first = run_dx(
        "capabilities",
        "--json",
        cwd=tmp_path,
    )
    second = run_dx(
        "capabilities",
        "--json",
        cwd=tmp_path,
    )

    assert first.returncode == 0
    assert second.returncode == 0
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == b""


def test_capabilities_requires_json(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "capabilities",
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert result.stdout == b""
    assert b"requires --json" in result.stderr


def test_capabilities_rejects_unknown_options(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "capabilities",
        "--json",
        "--unsupported",
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert result.stdout == b""


def test_advertised_commands_are_available(
    run_dx,
    tmp_path,
):
    for command in EXPECTED["commands"]:
        result = run_dx(
            command,
            "-h",
            cwd=tmp_path,
        )

        assert result.returncode == 0, command


def test_advertised_carrier_versions_are_readable(
    run_dx,
    tmp_path,
):
    for version in EXPECTED["carrier"]["read_versions"]:
        carrier = tmp_path / (
            version.replace(".", "-") + ".dx.txt"
        )
        carrier.write_bytes(
            f"%%DX {version}\n%%END\n".encode("ascii")
        )

        result = run_dx(
            "verify",
            str(carrier),
            "--policy",
            "structural",
            "--json",
            cwd=tmp_path,
        )

        assert result.returncode == 0, version
        assert json.loads(result.stdout)["version"] == (
            version
        )


def test_advertised_carrier_write_version_is_actual(
    run_dx,
    tmp_path,
):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_bytes(b"a\n")

    result = run_dx(
        "pack",
        str(source),
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert result.returncode == 0
    assert result.stdout.startswith(
        b"%%DX v2.0.0\n"
    )


def test_advertised_envelope_profile_is_actual(
    run_dx,
    tmp_path,
):
    carrier = tmp_path / "carrier.dx.txt"
    carrier.write_bytes(
        b"%%DX v2.0.0\n%%END\n"
    )

    envelope = run_dx(
        "envelope",
        str(carrier),
        "--envelope-profile",
        "canonical-v1",
        "-o",
        "-",
        cwd=tmp_path,
    )

    assert envelope.returncode == 0
    assert envelope.stdout.startswith(
        b'%%DX-ENVELOPE v1.0.0 '
        b'profile="canonical-v1"\n'
    )


def test_advertised_verification_policies_execute(
    run_dx,
    tmp_path,
):
    envelope = (
        ROOT
        / "tests/fixtures/envelopes/golden/"
        "mixed.dx.envelope.txt"
    )

    for policy in EXPECTED["verification_policies"]:
        result = run_dx(
            "verify",
            str(envelope),
            "--policy",
            policy,
            "--json",
            cwd=tmp_path,
        )

        assert result.returncode == 0, policy
        assert json.loads(result.stdout)["policy"] == (
            policy
        )


def test_planned_wp10_behavior_is_not_advertised(
    run_dx,
    tmp_path,
):
    result = run_dx(
        "capabilities",
        "--json",
        cwd=tmp_path,
    )
    payload = json.loads(result.stdout)

    encoded = json.dumps(
        payload,
        sort_keys=True,
    )

    assert "stdout_default" not in encoded
    assert "default_output_sink" not in encoded
    assert "check" not in encoded
    assert "consumer-ready" not in encoded
