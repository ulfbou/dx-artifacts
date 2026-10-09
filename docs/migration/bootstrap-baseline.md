# DX Artifacts bootstrap baseline

## Objective

Establish DX Artifacts' controlling implementation baseline from external source material before behavior-preserving decomposition or new product behavior begins.

## Mechanical process

1. Create the DX Artifacts repository with the controlling documentation and project metadata.
2. Import the Dx.Domain `scripts/release-gate/dx.py` candidate without behavioral rewriting.
3. Preserve a temporary compatibility entry point so candidate behavior remains executable.
4. Capture the candidate's software identity, CLI behavior, diagnostics, exit behavior, and carrier bytes.
5. Import applicable Dx.Domain tests and integration fixtures as attributed external evidence.
6. Import applicable Collab compatibility and regression evidence as attributed external evidence.
7. Run both applicable evidence sets against the candidate inside DX Artifacts.
8. Classify every difference.
9. Resolve all `REQUIRED_CORE`, `DEFECT`, and `UNRESOLVED` findings.
10. Record exact controlling golden DX v2.0.0 carrier bytes.
11. Declare the accepted DX Artifacts bootstrap baseline.
12. Begin structural extraction only after baseline acceptance.

## Difference classifications

```text
REQUIRED_CORE
    Must become native DX Artifacts behavior.
CONSUMER_ADAPTER
    Belongs in a future consumer repository or adapter.
LEGACY_COMPATIBILITY
    Preserved through an explicit compatibility layer.
HISTORICAL_ONLY
    Retained as provenance but not carried forward.
DEFECT
    Corrected through an explicitly scoped behavioral change.
UNRESOLVED
    Blocks baseline acceptance.
```

Every observed difference receives one classification and an evidence reference. `UNRESOLVED` blocks acceptance.

## Imported monolith

The initial implementation is an imported monolith containing carrier grammar, workspace selection, serialization, parsing, verification, filesystem publication, application, inspection, CLI parsing, diagnostics, and process adaptation.

DX Artifacts preserves it as historical and behavioral evidence. Later modularization changes code ownership and dependency direction without changing established carrier bytes or supported behavior unless a separately accepted change authorizes the difference.

## Bootstrap prohibitions

Bootstrap must not:

- combine import or extraction with envelope implementation;
- change omitted-`-o` behavior;
- rewrite diagnostics during structural extraction;
- absorb every Collab historical behavior into the native core;
- describe the candidate as controlling before cross-repository evidence passes;
- require future consumer migration before native DX Artifacts development may proceed.
