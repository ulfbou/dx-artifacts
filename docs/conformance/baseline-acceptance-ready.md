# Baseline-import acceptance-ready criteria

The PR is acceptance-ready only when every applicable result is explicit and passing.

## Source and provenance

- Accepted root `dx.py` matches the recorded byte size and SHA-256.
- Source repository, source path, carrier identity, and accepted status are recorded.
- No implementation change is hidden inside fixture or documentation work.

## Executable evidence

- Pytest collection succeeds.
- Baseline identity tests pass.
- Controlling golden carrier bytes pass without regeneration.
- CLI, parser, serializer, selection, pack, inspect, unpack/apply, diagnostics, and reachable exit classes have characterization evidence.
- Temporary workspaces are isolated and deterministic.

## Contract preservation

- The accepted bootstrap baseline used numbered filesystem publication for omitted output. WP-10 supersedes that default: omitted output now selects stdout.
- Explicit stdout behavior remains byte-exact and diagnostics stay off artifact stdout.
- Current supported carrier parsing remains characterized.
- Read-only, binary, escaped text, deterministic ordering, and trailing-newline behavior remain characterized.

## Scope

- No package extraction.
- No envelope implementation.
- No stdout-default activation.
- No diagnostic redesign.
- No consumer-specific generic behavior.
- No unsupported public Python API claim.

## Documentation

- Baseline status is accepted rather than pending.
- Collab remains compatibility evidence evaluated against the accepted baseline.
- Roadmap and work-package ordering remain coherent.

Missing evidence, unexplained byte drift, or an unresolved generic compatibility obligation returns non-zero and blocks acceptance.
