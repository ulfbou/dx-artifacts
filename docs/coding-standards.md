# DX Artifacts coding standards

## Status

Accepted repository standard.

## Core principles

1. Readability is part of correctness.
2. Exact bytes, observable behavior, and explicit policy are controlling evidence.
3. Deterministic processes are reproducible from declared inputs.
4. Public behavior is tested and compatibility changes are separately gated.
5. Existing contracts are preserved or intentionally versioned.
6. Consumer-specific orchestration does not enter the generic DX core.

## Python

- Support the Python runtime range declared by project metadata and CI.
- Type annotate supported Python APIs and stable internal boundaries where practical.
- Prefer immutable value objects for artifact descriptors, options, evidence, and results.
- Keep carrier grammar, selection, serialization, verification, publication, CLI adaptation, and process termination separated.
- Treat bytes as bytes. Do not normalize transported content outside an explicit format rule.
- Keep filesystem effects behind explicit source, sink, or application boundaries.
- Do not expose `argparse.Namespace`, private modules, parser classes, spool implementations, exception wiring, or rendering helpers as supported API.
- Only process entry points convert returned status into process termination.
- Preserve stable diagnostic codes and exit categories unless an accepted change explicitly versions them.

## Accepted bootstrap baseline

- Root `dx.py` is the accepted bootstrap implementation baseline.
- Baseline-import work must preserve it byte-for-byte.
- Characterization tests may import pure functions for evidence, but that does not make those functions public API.
- Behavior-preserving extraction begins only after baseline identity and characterization gates pass.
- Envelope implementation, package extraction, and stdout-default activation are excluded from baseline import.

## Tests and fixtures

- Use pytest for native characterization and regression tests.
- Prefer subprocess tests for CLI, streams, diagnostics, exit categories, and filesystem effects.
- Read and compare golden artifacts as bytes.
- Every golden fixture records purpose, size, SHA-256, and source inputs.
- Tests must not silently regenerate controlling fixtures.
- Temporary workspaces must be isolated and must not depend on user-global Git or DX configuration.
