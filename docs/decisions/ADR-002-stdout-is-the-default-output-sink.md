# ADR-002: Stdout is the default artifact output sink

## Status

Proposed. Not active during bootstrap or behavior-preserving decomposition.

## Context

Artifact bytes do not require a destination path for identity. Pipeline composition should not require user-managed temporary files.

## Decision

When this decision is activated at WP-10, artifact-producing commands treat omitted `-o` and `-o -` as stdout. `-o FILE` selects controlled filesystem publication.

## Consequences

Benefits:

- natural process composition;
- fewer implicit filesystem effects;
- destination-independent artifact identity;
- consistent producer behavior.

Trade-offs:

- shell redirection cannot provide DX-controlled atomic publication;
- DX cannot infer or self-exclude a shell redirection target;
- `--force` has no meaning for stdout;
- reports require a separate channel.

## Rejected alternative

Automatic numbered output filenames remain available only as an explicitly designed convenience, not the default artifact sink.

## Verification obligations

- omitted `-o` and `-o -` produce identical bytes;
- stdout and `-o FILE` artifact bytes are identical;
- diagnostics never contaminate artifact stdout;
- `--force` is rejected for stdout;
- filesystem publication retains atomic and symlink-safe behavior.
