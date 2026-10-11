# Compatibility and deprecation policy

## Status

Accepted for the DX Artifacts 0.1.0 library release under ADR-008.

## Version domains

Software releases, carrier versions, envelope versions, canonical profiles, operation-report schemas, capability schemas, and supported Python API versions are independent identities. A software release does not implicitly change an artifact-format identity.

## Stable interfaces

Names explicitly exported through `dx_artifacts.__all__` and documented as supported constitute the 0.1.0 compatibility surface.

Private modules, parser objects, adapter syntax, internal classes, spool implementations, rendering helpers, exception wiring, root `dx.py`, and generated artifacts are not supported interfaces.

`python -m dx_artifacts` is a non-stable reference and conformance adapter. The distribution installs no console command and publishes no supported standalone CLI.

## Compatibility

Patch releases preserve supported API behavior and established artifact bytes. Minor releases may add backward-compatible supported exports, result fields, formats, or capabilities. Incompatible API, schema, carrier, envelope, or profile changes require an explicitly versioned boundary.

Canonical-profile output remains byte-identical for identical inputs and effective options. An incompatible canonical representation requires a new profile identity.

## Deprecation

A supported library interface is deprecated before removal. Deprecation documentation identifies the affected interface, replacement, first deprecated software release, and earliest permitted removal release. Security or safety defects may require accelerated removal with explicit evidence and release documentation.

## Consumer pinning

Consumers pin a released distribution by software version and artifact identity, verify its provenance, and run consumer-owned integration evidence.
