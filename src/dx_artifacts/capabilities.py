"""Deterministic, conformance-gated DX capability discovery."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


CAPABILITY_SCHEMA_VERSION = 1
TOOL_NAME = "dx-artifacts"
SOFTWARE_VERSION = "0.0.0"

CARRIER_READ_VERSIONS = (
    "v1.3.1",
    "v2.0.0",
)
CARRIER_WRITE_VERSION = "v2.0.0"

ENVELOPE_READ_VERSIONS = (
    "v1.0.0",
)
ENVELOPE_WRITE_VERSION = "v1.0.0"
ENVELOPE_PROFILES = (
    "canonical-v1",
)

VERIFICATION_POLICIES = (
    "structural",
    "integrity",
    "canonical",
)

DIGESTS = (
    "sha256",
)

COMMANDS = (
    "pack",
    "envelope",
    "unwrap",
    "inspect",
    "verify",
    "capabilities",
)


@dataclass(frozen=True)
class Capabilities:
    """One immutable capability document."""

    schema_version: int
    tool_name: str
    software_version: str
    carrier_read_versions: tuple[str, ...]
    carrier_write_version: str
    envelope_read_versions: tuple[str, ...]
    envelope_write_version: str
    envelope_profiles: tuple[str, ...]
    verification_policies: tuple[str, ...]
    digests: tuple[str, ...]
    commands: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "tool": {
                "name": self.tool_name,
                "software_version": self.software_version,
            },
            "carrier": {
                "read_versions": list(
                    self.carrier_read_versions
                ),
                "write_version": self.carrier_write_version,
            },
            "envelope": {
                "read_versions": list(
                    self.envelope_read_versions
                ),
                "write_version": self.envelope_write_version,
                "profiles": list(self.envelope_profiles),
            },
            "verification_policies": list(
                self.verification_policies
            ),
            "digests": list(self.digests),
            "commands": list(self.commands),
        }


def current_capabilities() -> Capabilities:
    """Return only implemented and conformance-gated behavior."""

    return Capabilities(
        schema_version=CAPABILITY_SCHEMA_VERSION,
        tool_name=TOOL_NAME,
        software_version=SOFTWARE_VERSION,
        carrier_read_versions=CARRIER_READ_VERSIONS,
        carrier_write_version=CARRIER_WRITE_VERSION,
        envelope_read_versions=ENVELOPE_READ_VERSIONS,
        envelope_write_version=ENVELOPE_WRITE_VERSION,
        envelope_profiles=ENVELOPE_PROFILES,
        verification_policies=VERIFICATION_POLICIES,
        digests=DIGESTS,
        commands=COMMANDS,
    )


def serialize_capabilities(
    capabilities: Capabilities | None = None,
) -> bytes:
    """Serialize deterministic UTF-8 capability JSON."""

    effective = (
        capabilities
        if capabilities is not None
        else current_capabilities()
    )
    return (
        json.dumps(
            effective.to_json(),
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")
