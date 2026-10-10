from __future__ import annotations

import json

from dx_artifacts.capabilities import (
    CAPABILITY_SCHEMA_VERSION,
    COMMANDS,
    Capabilities,
    current_capabilities,
    serialize_capabilities,
)


def test_current_capabilities_are_immutable_and_complete():
    capabilities = current_capabilities()

    assert isinstance(capabilities, Capabilities)
    assert capabilities.schema_version == (
        CAPABILITY_SCHEMA_VERSION
    )
    assert capabilities.tool_name == "dx-artifacts"
    assert capabilities.software_version == "0.0.0"
    assert capabilities.carrier_read_versions == (
        "v1.3.1",
        "v2.0.0",
    )
    assert capabilities.carrier_write_version == (
        "v2.0.0"
    )
    assert capabilities.envelope_read_versions == (
        "v1.0.0",
    )
    assert capabilities.envelope_write_version == (
        "v1.0.0"
    )
    assert capabilities.envelope_profiles == (
        "canonical-v1",
    )
    assert capabilities.verification_policies == (
        "structural",
        "integrity",
        "canonical",
    )
    assert capabilities.digests == ("sha256",)
    assert capabilities.commands == COMMANDS


def test_capability_serialization_is_deterministic():
    first = serialize_capabilities()
    second = serialize_capabilities()

    assert first == second
    assert first.endswith(b"\n")
    assert b"\r" not in first

    payload = json.loads(first)
    assert payload == current_capabilities().to_json()


def test_capability_arrays_have_deterministic_order():
    payload = json.loads(serialize_capabilities())

    assert payload["carrier"]["read_versions"] == [
        "v1.3.1",
        "v2.0.0",
    ]
    assert payload["envelope"]["profiles"] == [
        "canonical-v1",
    ]
    assert payload["verification_policies"] == [
        "structural",
        "integrity",
        "canonical",
    ]
    assert payload["digests"] == ["sha256"]
    assert payload["commands"] == [
        "pack",
        "envelope",
        "unwrap",
        "inspect",
        "verify",
        "capabilities",
    ]
