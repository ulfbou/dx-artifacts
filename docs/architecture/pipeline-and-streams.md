# DX pipeline and streams

## 1. Principle

DX production is a composition of byte-preserving stages:

```text
source → construct → verify → transform → verify → publish
```

Integrated commands and explicit pipelines use the same logical stages.

## 2. Active stdout-first production

This section defines the active behavior governed by ADR-002 and activated by WP-10.

Artifact-producing commands follow:

```text
No -o supplied     → stdout
-o -               → stdout
-o FILE            → controlled filesystem publication
```

This applies to `pack`, `envelope`, and `unwrap`.

## 3. Explicit artifact input

The current CLI requires an `INPUT` operand for `envelope`, `unwrap`, and `verify`. Passing `-` selects stdin; passing a path selects filesystem input.

```text
INPUT -             → stdin
INPUT FILE          → filesystem input
```

`inspect` separately requires a carrier operand and accepts `-` for stdin. No current single-artifact command infers stdin from an omitted operand. `pack` differs because its normal source is workspace selection and its `SOURCE` operand defaults to the current directory.

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

The implementation has an internal check sink that consumes complete artifact bytes without publication. A future public `--check` mode may expose that sink; no `--check` CLI option is currently supported.

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

Bootstrap import, baseline acceptance, package establishment, and behavior-preserving decomposition retained the historical omitted-`-o` behavior. WP-10 passed its compatibility gate and activated stdout as the default artifact sink. Future consumer migration occurs after a consumer-ready release and does not control activation inside DX Artifacts.
