# DX pipeline and streams

## 1. Principle

DX production is a composition of byte-preserving stages:

```text
source → construct → verify → transform → verify → publish
```

Integrated commands and explicit pipelines use the same logical stages.

## 2. Target stdout-first production

This section defines target behavior governed by ADR-002. Bootstrap and decomposition preserve the accepted baseline default until WP-10 activates this compatibility change.

After activation, artifact-producing commands follow:

```text
No -o supplied     → stdout
-o -               → stdout
-o FILE            → controlled filesystem publication
```

This applies to `pack`, `envelope`, and `unwrap`.

## 3. Stdin-first consumption

Single-artifact consumers follow:

```text
No INPUT supplied  → stdin
INPUT -             → stdin
INPUT FILE          → filesystem input
```

This applies to `envelope`, `unwrap`, `inspect`, and `verify`. `pack` differs because its normal source is workspace selection.

## 4. Channel contract

When stdout is an artifact channel, it contains artifact bytes only.

Stderr carries warnings, errors, and optional verbose diagnostics. Machine-readable operation reports use an explicit report sink.

A command must not write a JSON report and artifact bytes to the same stdout stream.

## 5. Sink guarantees

### 5.1 Stdout

Stdout provides composition and exact byte delivery to a downstream consumer. It does not provide filesystem atomicity, overwrite control, destination symlink validation, or output-path self-exclusion.

### 5.2 Filesystem

`-o FILE` permits DX to:

- validate before replacement;
- write to a temporary sibling;
- flush and synchronize where supported;
- atomically replace where supported;
- reject unsafe symlink targets;
- enforce conflict policy;
- exclude the known output path from workspace selection.

### 5.3 Check sink

A check sink constructs and verifies complete artifact bytes but publishes nothing. It supports release gates and exact preflight validation.

## 6. Shell redirection versus `-o FILE`

These forms may produce identical bytes:

```bash
dx pack SOURCE > artifact.dx.txt
dx pack SOURCE -o artifact.dx.txt
```

They have different publication guarantees. Shell redirection may create or truncate the destination before DX validates input. `-o FILE` allows DX-controlled atomic publication.

## 7. Spooling

Header-first envelope metadata requires sizes and hashes before final framing is emitted. Implementations should use a binary spooled stream:

```text
memory until threshold
→ temporary storage beyond threshold
→ rewind
→ verify exact bytes
→ transform or publish
```

Complete artifacts must not be required to remain in memory.

## 8. Serialize once

Integrated envelope production must serialize the carrier once, verify those exact bytes, and envelope those exact bytes.

It must not verify one serialization and envelope a second serialization from reread workspace state.

## 9. Dry-run and check

`--dry-run` evaluates source selection, options, and intended sinks without publishing an artifact. It must not claim exact final hashes unless it actually constructs the exact bytes.

A future `--check` mode constructs and verifies exact bytes internally, publishes nothing, and fails if production or verification fails.

## 10. Broken pipes

A downstream closure means complete stdout delivery did not occur. DX must avoid an unhandled traceback and must not report complete delivery as successful.

The precise process exit contract must be locked by implementation tests.

## 11. Composition invariants

Under identical effective options and stable input:

```text
pack SOURCE == pack SOURCE -o -
```

```text
pack SOURCE --format envelope == pack SOURCE | envelope
```

```text
pack SOURCE | envelope | unwrap == pack SOURCE
```

Each equality is byte equality.

## 12. Activation boundary

Bootstrap import, baseline acceptance, package establishment, and behavior-preserving decomposition retain the accepted omitted-`-o` behavior. Stdout-default activation occurs only in WP-10 after the compatibility gate passes. Future consumer migration occurs after a consumer-ready release and does not control activation inside DX Artifacts.
