# ADR-006: Library core and CLI adapter

## Status

Accepted.

## Context

Reusable artifact behavior must be importable without making CLI parsing, rendering, process termination, or every extracted function part of the supported API.

## Decision

DX Artifacts is an importable Python package and a command-line product. The package owns reusable artifact behavior. The CLI owns process adaptation. The entry point alone converts a returned status into process termination.

```text
Repository       ulfbou/dx-artifacts
Distribution     dx-artifacts
Import package   dx_artifacts
Console command  dx
Module command   python -m dx_artifacts
```

Supported interface levels are a stable CLI contract, a small explicitly exported Python API, and internal implementation modules.

Consumers must not depend on `argparse.Namespace`, internal parser classes, private module paths, concrete spool implementations, internal exception wiring, or CLI rendering helpers.

## Consequences

- Core behavior can be reused by consumers and all command forms.
- Public API growth is deliberate and reviewable.
- CLI compatibility and Python API compatibility can be governed explicitly.
- Internal decomposition remains changeable behind observable contracts.

## Verification obligations

- Console and module entry points run the same orchestration.
- Supported API exports are enumerated and tested.
- Process termination occurs only at entry-point boundaries.
- Consumer evidence imports only supported exports.
