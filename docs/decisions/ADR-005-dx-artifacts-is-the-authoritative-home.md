# ADR-005: DX Artifacts is the authoritative home

## Status

Accepted, partially superseded by ADR-008.

## Context

Before this repository was established, Collab and Dx.Domain independently maintained generic DX functionality. DX Artifacts requires one native authority while preserving those repositories as attributed source evidence and prospective consumers.

## Decision

DX Artifacts is the authoritative repository for DX carrier and envelope specifications, the Python library implementation, supported Python API, format and profile conformance, compatibility policy, fixtures, golden artifacts, release evidence, and library releases.

Consumer repositories may install a released DX Artifacts library. They must not independently modify the generic implementation.

ADR-008 supersedes the earlier assignment of a supported command-line product and standalone distributions to this repository. DXS is reserved for a separate future application product.

## Consequences

- DX Artifacts has one native upstream authority.
- Consumer-specific behavior stays in consumer adapters or applications.
- Generic defects are corrected once upstream.
- Compatibility requirements become explicit consumer evidence.
- Library consumers identify the upstream version and distribution artifact they use.

## Verification obligations

- Release provenance identifies one upstream library source.
- Consumer integration evidence runs against a pinned upstream library artifact.
- No consumer presents a copied implementation as an independent generic DX upstream.
- Current product claims conform to ADR-008.
