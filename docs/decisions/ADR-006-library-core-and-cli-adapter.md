# ADR-006: Library core and CLI adapter

## Status

Accepted, partially superseded by ADR-008.

## Context

Reusable artifact behavior must be importable without making CLI parsing, rendering, process termination, or every extracted function part of the supported API.

## Decision

The package owns reusable artifact behavior. Process adapters own argument parsing, rendering, and exit mapping. An adapter entry point alone may convert a returned status into process termination.

Consumers must not depend on `argparse.Namespace`, internal parser classes, private module paths, concrete spool implementations, internal exception wiring, or rendering helpers.

ADR-008 supersedes the earlier decision that DX Artifacts is also a command-line product. It also supersedes the installed `dx` command, stable module-command status, and stable CLI interface level. `python -m dx_artifacts` is now a non-stable reference and conformance adapter.

## Consequences

- Core behavior can be reused without process adaptation.
- Public API growth is deliberate and reviewable.
- Internal decomposition remains changeable behind supported library contracts.
- Adapter behavior can provide integration evidence without becoming library API.

## Verification obligations

- Supported API exports are enumerated and tested.
- Reusable operations neither render process output nor terminate the process.
- Process termination occurs only at adapter boundaries.
- Consumer evidence imports only supported exports.
- The reference adapter delegates to package behavior and does not become a second implementation authority.
