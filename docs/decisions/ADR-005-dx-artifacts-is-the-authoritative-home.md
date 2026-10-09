# ADR-005: DX Artifacts is the authoritative home

## Status

Accepted.

## Context

Before this repository was established, Collab and Dx.Domain independently maintained generic DX functionality. DX Artifacts requires one native product authority while preserving those repositories as attributed source evidence and prospective consumers.

## Decision

DX Artifacts is the authoritative repository for DX carrier and envelope specifications, the Python implementation, supported Python API, command-line behavior, format and profile conformance, compatibility policy, fixtures and golden artifacts, releases, and standalone distributions.

Consumer repositories may install or mechanically vendor a released DX Artifacts distribution. They must not independently modify the generic implementation.

## Consequences

- DX Artifacts has one native upstream authority from repository inception.
- Consumer-specific behavior stays in consumer adapters.
- Generic defects are corrected once upstream.
- Compatibility requirements become explicit consumer evidence.
- Repository-local vendoring remains possible without split ownership.
- A vendored copy identifies its upstream version and digest and is not edited directly.

## Verification obligations

- Release provenance identifies one upstream source.
- Consumer integration evidence runs against the pinned upstream artifact.
- Mechanical checks reject or detect direct edits to vendored copies.
- No consumer may present an installed, generated, or vendored copy as an independent generic DX upstream.
