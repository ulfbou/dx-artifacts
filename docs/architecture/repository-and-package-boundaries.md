# DX Artifacts repository and package boundaries

## Native product boundary

The `ulfbou/dx-artifacts` repository owns:

- DX carrier and envelope specifications;
- the Python library implementation;
- the supported Python API;
- format and profile conformance;
- compatibility and deprecation policy for the library;
- fixtures and golden artifacts;
- release evidence;
- wheel and source distributions.

These are native DX Artifacts concerns, not responsibilities delegated to source or consumer repositories.

## Product identities

```text
Repository          ulfbou/dx-artifacts
Library product     DX Artifacts
Distribution        dx-artifacts
Import package      dx_artifacts
Reference adapter   python -m dx_artifacts
Future application  DXS
```

The reference adapter is non-stable. Release 0.1.0 installs no console command and publishes no supported standalone CLI.

## Interface levels

1. Small, explicitly exported Python API.
2. Internal implementation modules.
3. Non-stable reference and conformance adapters.

Consumers must not depend on `argparse.Namespace`, parser classes, private module paths, spool implementations, exception wiring, rendering helpers, or adapter syntax.

The package owns reusable artifact behavior. Adapters own process argument parsing, rendering, and exit mapping. Only an adapter entry point may convert a returned status into process termination.

## External repository relationships

### Dx.Domain

Dx.Domain is an external source of bootstrap implementation and release-gate evidence. After a DX Artifacts library release exists, Dx.Domain may adopt a pinned library distribution behind repository-specific orchestration.

### Collab

Collab is an external source of compatibility evidence. After a DX Artifacts library release exists, Collab may adopt that release behind collaboration-specific adapters.

### pystd-suite

pystd-suite is related but independently governed. It neither owns nor supplies DX runtime code.

## Future DXS boundary

DXS is reserved for a separately governed future CLI application. It may depend on `dx-artifacts` and own command names, help, configuration, exit mapping, shell behavior, and CLI compatibility. This repository does not publish DXS in release 0.1.0.
