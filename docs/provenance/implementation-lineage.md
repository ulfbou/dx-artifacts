# DX implementation lineage

## External source lineage

Before DX Artifacts was established, DX carrier functionality was independently maintained in Dx.Domain and Collab.

- Dx.Domain carries `scripts/release-gate/dx.py` because its release gate produces and verifies repository-local carrier handoffs.
- Collab uses DX in collaboration, evidence, compatibility, and delivery workflows.
- The historical .NET DXS repository influenced naming and product lineage but is not the Python implementation source or authority.

The independent implementations created split historical implementation authority outside DX Artifacts.

## Accepted bootstrap baseline

DX Artifacts imported the current Dx.Domain release-gate implementation and accepted the resulting root `dx.py` as its controlling bootstrap implementation baseline. The accepted manifest records its source identity, byte size, and SHA-256, while characterization tests and golden carrier fixtures preserve observable behavior.

This acceptance records provenance and controlling implementation state without claiming that the Dx.Domain copy was historically superior to every independently maintained implementation.

Collab remains a required external compatibility-evidence source. Its historical entry points and local behavior are classified against the accepted baseline and are not automatically promoted into the DX Artifacts core. An unresolved generic compatibility obligation may block behavior-preserving extraction, but Collab evidence does not reopen or revoke baseline selection by itself.

## Continuing authority

DX Artifacts alone owns continuing generic product evolution. Dx.Domain and Collab remain external repositories and may later adopt a released DX Artifacts distribution as consumers. They retain their repository-specific orchestration, policies, adapters, and integration tests.
