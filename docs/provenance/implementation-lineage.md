# DX implementation lineage

## External source lineage

Before DX Artifacts was established, DX carrier functionality was independently maintained in Dx.Domain and Collab.

- Dx.Domain carries `scripts/release-gate/dx.py` because its release gate produces and verifies repository-local carrier handoffs.
- Collab uses DX in collaboration, evidence, compatibility, and delivery workflows.
- The historical .NET DXS repository influenced naming and product lineage but is not the Python implementation source or authority.

The independent implementations created split historical implementation authority outside DX Artifacts.

## Bootstrap candidate

DX Artifacts imports the current Dx.Domain release-gate implementation as its bootstrap candidate because it is believed to represent the latest current implementation.

That assessment is not a claim of proven superiority. The candidate becomes DX Artifacts' controlling implementation baseline only after:

- its observable behavior is captured;
- current DX v2.0.0 carrier bytes are preserved;
- applicable Dx.Domain integration evidence passes;
- applicable Collab codec and compatibility evidence passes;
- every difference is classified and required findings are resolved.

Collab is therefore a required external compatibility-evidence source. Its historical entry points and local behavior are not automatically promoted into the DX Artifacts core.

## Continuing authority

After baseline acceptance, DX Artifacts alone owns continuing generic product evolution. Dx.Domain and Collab remain external repositories and may later adopt a released DX Artifacts distribution as consumers. They retain their repository-specific orchestration, policies, adapters, and integration tests.
