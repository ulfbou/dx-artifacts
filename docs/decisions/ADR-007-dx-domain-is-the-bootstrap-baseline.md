# ADR-007: Dx.Domain supplies the accepted bootstrap baseline

## Status

Accepted.

## Context

DX Artifacts required external source material to bootstrap without a clean-room rewrite. Dx.Domain supplied the imported implementation, while Collab remains an independently maintained compatibility-evidence source.

## Decision

DX Artifacts accepts the root `dx.py` imported from Dx.Domain `scripts/release-gate/dx.py` as its controlling bootstrap implementation baseline. Its source provenance, exact byte identity, observable behavior, and controlling golden carrier bytes are recorded and mechanically verified.

Applicable Collab codec and compatibility evidence is evaluated against the accepted baseline. Differences are classified rather than silently merged as `REQUIRED_CORE`, `CONSUMER_ADAPTER`, `LEGACY_COMPATIBILITY`, `HISTORICAL_ONLY`, `DEFECT`, or `UNRESOLVED`. An `UNRESOLVED` generic obligation blocks the affected compatibility or extraction boundary; it does not reopen baseline selection by itself.

## Consequences

- Accepted provenance is transparent without claiming historical superiority.
- Collab remains required compatibility evidence evaluated against the baseline.
- Consumer-specific behavior is not automatically absorbed into the core.
- Structural extraction starts only after baseline identity and applicable characterization gates pass.

## Verification obligations

- The accepted root `dx.py` matches its recorded provenance, byte size, and SHA-256.
- Exact controlling carrier bytes are recorded and reproducible.
- Native characterization covers applicable observable baseline behavior.
- Every imported compatibility difference has one documented classification.
- No unresolved generic obligation remains when the affected extraction boundary begins.
