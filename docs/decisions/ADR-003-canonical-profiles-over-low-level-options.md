# ADR-003: Canonical profiles replace arbitrary low-level envelope combinations

## Status

Accepted and implemented by WP-05.

## Context

Envelope bytes depend on archive structure, compression, metadata, Base64 formatting, hashing, and framing. Independent public flags would create a combinatorial compatibility surface and weaken reproducibility.

## Decision

Envelope behavior is selected through a registered, versioned profile. The first profile is `canonical-v1`.

The profile defines archive structure, metadata normalization, compression, encoding, line wrapping, digests, resource limits, and canonical verification.

## Consequences

- Canonical output can be reproducible.
- Public CLI surface remains small.
- Capability discovery and policy can refer to stable profile names.
- Future profiles do not silently alter `canonical-v1`.

## Rejected alternative

Normal v1 production will not expose arbitrary independent compression, compression-level, Base64-width, archive-time, and digest flags.

## Verification obligations

- Unsupported profiles fail explicitly.
- Profile behavior is covered by golden bytes.
- Canonical verification checks all profile-controlled behavior.
- A profile name is never reused for changed output rules.
