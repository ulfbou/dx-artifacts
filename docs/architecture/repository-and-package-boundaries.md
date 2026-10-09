# DX Artifacts repository and package boundaries

## Native product boundary

The `ulfbou/dx-artifacts` repository owns:

- DX carrier and envelope specifications;
- the Python implementation;
- the supported Python API;
- command-line behavior;
- format and profile conformance;
- compatibility and deprecation policy;
- fixtures and golden artifacts;
- release evidence;
- installable and standalone distributions.

These are native DX Artifacts concerns, not responsibilities delegated to source or consumer repositories.

## Product identities

```text
Repository       ulfbou/dx-artifacts
Distribution     dx-artifacts
Import package   dx_artifacts
Console command  dx
Module command   python -m dx_artifacts
Standalone form  python dx.py
```

The console, module, supported API, and standalone forms originate from one source authority and must satisfy the same applicable observable contracts.

## Interface levels

1. Stable CLI contract.
2. Small, explicitly exported Python API.
3. Internal implementation modules.

Consumers must not depend on `argparse.Namespace`, internal parser classes, private module paths, concrete spool implementations, internal exception wiring, or CLI rendering helpers.

The package owns reusable artifact behavior. CLI adapters own process argument parsing, rendering, and exit mapping. Only an entry point converts a returned status into process termination.

## External repository relationships

### Dx.Domain

Dx.Domain is an external source of bootstrap implementation and release-gate evidence. After a consumer-ready DX Artifacts release exists, Dx.Domain may adopt a pinned installed or standalone distribution.

Dx.Domain continues to own release-gate orchestration, evidence selection, feedback dossier semantics, handoff policy, gate-result reporting, and consumer integration tests.

### Collab

Collab is an external source of compatibility evidence. After a consumer-ready release exists, Collab may adopt that release behind collaboration-specific adapters where required.

Collab continues to own collaboration orchestration, selection and evidence policy, supported historical command adapters, and consumer integration tests.

### pystd-suite

pystd-suite is related but independently governed. It neither owns nor supplies DX runtime code.

## Vendoring boundary

A future consumer may carry a standalone `dx.py` generated from a DX Artifacts release when repository-local availability is required. The consumer records the upstream software version, source release identity, SHA-256, acquisition or generation procedure, and consumer integration evidence.

The vendored artifact is not edited directly. Generic changes are made in DX Artifacts and consumed through a later release.
