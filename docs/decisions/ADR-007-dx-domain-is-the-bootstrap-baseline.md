# ADR-007: Dx.Domain supplies the bootstrap baseline candidate

## Status

Accepted.

## Context

DX Artifacts requires external source material to bootstrap without a clean-room rewrite. Dx.Domain supplies the implementation candidate; Dx.Domain and Collab supply independently maintained evidence.

## Decision

DX Artifacts imports the current Dx.Domain `scripts/release-gate/dx.py` as its bootstrap implementation candidate because it is believed to represent the latest current implementation.

It is accepted as the controlling implementation only after its existing behavior is captured, current DX v2.0.0 carrier bytes are preserved, applicable Dx.Domain release-gate integration passes, applicable Collab codec and compatibility evidence passes, and every difference is classified rather than silently merged.

Difference classifications are `REQUIRED_CORE`, `CONSUMER_ADAPTER`, `LEGACY_COMPATIBILITY`, `HISTORICAL_ONLY`, `DEFECT`, and `UNRESOLVED`. Any `UNRESOLVED` finding blocks controlling-baseline acceptance.

## Consequences

- Candidate selection is transparent without claiming unexecuted superiority.
- Collab remains required compatibility evidence.
- Consumer-specific behavior is not automatically absorbed into the core.
- Structural extraction starts only after baseline acceptance.

## Verification obligations

- Applicable evidence from both consumers runs against the candidate.
- Exact controlling carrier bytes are recorded.
- Every difference has one documented classification.
- Required core and defect findings are resolved.
- No unresolved finding remains when the baseline is declared.
