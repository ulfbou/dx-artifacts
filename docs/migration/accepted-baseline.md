# Accepted bootstrap baseline

## Decision

The root `dx.py` transported by `dx.py.dx.txt` from `Dx.Domain/scripts/release-gate/dx.py` is the accepted DX Artifacts bootstrap implementation baseline.

Baseline selection is closed. Collab evidence is evaluated against this baseline as compatibility evidence; it does not reopen baseline selection.

## Recorded identity

The repository gate calculates and verifies the authoritative identity from root `dx.py`. The initial accepted source identity represented by this batch is:

```text
path    dx.py
bytes   63888
sha256  f0d9b82ee7ab35e1374262ba2191198b3b13ea18559fb96e227f701dc763e13a
```

## Preservation boundary

The baseline-import PR must:

- commit root `dx.py` without changing its bytes;
- record provenance and identity mechanically;
- add native pytest characterization;
- establish controlling carrier fixtures;
- preserve current omitted-output, diagnostics, and exit behavior;
- keep Collab findings classified as compatibility evidence.

It must not perform package extraction, envelope implementation, diagnostic redesign, command renaming, or stdout-default activation.

## Compatibility classifications

`REQUIRED_CORE`, `CONSUMER_ADAPTER`, `LEGACY_COMPATIBILITY`, `HISTORICAL_ONLY`, `DEFECT`, and `UNRESOLVED` remain available. A Collab finding blocks extraction only when it identifies an unresolved obligation that could change accepted generic behavior. It does not revoke the accepted baseline by itself.
