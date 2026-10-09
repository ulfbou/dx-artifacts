# DX Artifacts bootstrap baseline

## Objective

Preserve and characterize DX Artifacts' accepted controlling bootstrap implementation before behavior-preserving decomposition or new product behavior begins.

## Mechanical process

1. Create the DX Artifacts repository with controlling documentation and project metadata.
2. Import the Dx.Domain `scripts/release-gate/dx.py` without behavioral rewriting.
3. Accept the imported root `dx.py` as the controlling bootstrap implementation baseline and record its exact provenance, byte size, and SHA-256.
4. Capture its CLI behavior, diagnostics, exit behavior, selection semantics, carrier bytes, and application behavior through native characterization tests.
5. Establish exact controlling golden DX v2.0.0 carrier bytes and manifests.
6. Import applicable Collab compatibility and regression evidence as attributed external evidence.
7. Run that evidence against the accepted baseline and classify every difference.
8. Resolve every compatibility finding that could change accepted generic behavior before the affected structural extraction proceeds.
9. Begin behavior-preserving extraction only after the baseline identity and applicable characterization gates pass.

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
    Blocks the affected compatibility obligation or later extraction when generic behavior is unclear.
```

Every observed compatibility difference receives one classification and an evidence reference. `UNRESOLVED` blocks the affected compatibility obligation or extraction boundary; it does not reopen accepted baseline selection by itself.

## Imported monolith

The initial implementation is an imported monolith containing carrier grammar, workspace selection, serialization, parsing, verification, filesystem publication, application, inspection, CLI parsing, diagnostics, and process adaptation.

DX Artifacts preserves it as historical and behavioral evidence. Later modularization changes code ownership and dependency direction without changing established carrier bytes or supported behavior unless a separately accepted change authorizes the difference.

## Bootstrap prohibitions

Bootstrap must not:

- combine import or extraction with envelope implementation;
- change omitted-`-o` behavior;
- rewrite diagnostics during structural extraction;
- absorb every Collab historical behavior into the native core;
- modify the accepted baseline while claiming behavior-preserving import or characterization;
- require future consumer migration before native DX Artifacts development may proceed.
