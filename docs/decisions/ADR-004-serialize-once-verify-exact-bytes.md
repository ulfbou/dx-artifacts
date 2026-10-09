# ADR-004: Serialize once and verify the exact bytes that are enveloped

## Status

Proposed.

## Context

Integrated envelope production needs a verified carrier and an envelope containing that carrier. Reconstructing the carrier after verification risks rereading changed workspace state.

## Decision

Integrated production performs:

```text
serialize carrier once
→ verify those exact bytes
→ envelope those exact bytes
→ verify envelope
→ publish final bytes
```

The intermediate carrier may use a binary spooled stream.

## Consequences

- The verified carrier is the enveloped carrier.
- Source files are not reread merely for envelope construction.
- Large artifacts can spill from memory to temporary storage.
- Verification and transformation accept reusable byte sources.

## Rejected alternative

Serializing, verifying, discarding, and serializing again is rejected because it duplicates work and weakens identity guarantees.

## Verification obligations

- Integrated and pipeline envelope production are byte-identical.
- Carrier digest covers the exact bytes stored in the ZIP entry.
- Source mutation after serialization cannot alter the enveloped carrier.
- Unwrap reproduces original carrier bytes exactly.
