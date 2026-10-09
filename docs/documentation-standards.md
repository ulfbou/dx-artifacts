# DX Artifacts documentation standards

## Status

Accepted repository standard.

## Authority

- `docs/README.md` is the documentation entry point.
- `docs/vision/dx-artifact-system.md` defines product direction and non-goals.
- `docs/roadmap/evolution-roadmap.md` controls product sequence.
- `docs/roadmap/implementation-delivery-roadmap.md` controls delivery boundaries.
- `docs/implementation/implementation-work-packages.md` defines work-package scope and gates.
- Accepted ADRs control their recorded decisions.
- Specifications are normative only according to their explicit status and activation boundary.
- Avoid duplicating normative requirements; link to the controlling document.

## Requirements

- Write from inside the DX Artifacts repository.
- Describe Dx.Domain and Collab only as attributed source-evidence repositories or future consumers.
- Distinguish accepted baseline fact, implemented behavior, proposed contract, activated capability, future plan, and external compatibility evidence.
- Describe authoritative inputs, outputs, identities, and evidence.
- Keep commands copyable and paths repository-relative.
- Avoid placeholder success claims and unsupported implementation claims.
- Record limitations, explicit exclusions, and activation boundaries.
- Preserve qualifications when rewriting accepted content.
- Keep software release, carrier format, envelope format, profile, report-schema, and capability-schema identities separate.

## Tool documentation

- Document `dx` as the canonical product command after that distribution exists.
- Label `python -m dx_artifacts` as module execution and `python dx.py` as standalone execution.
- Label imported or historical `dx.py` references as provenance or bootstrap references.
- Document only conformance-gated commands and fields as supported current behavior.
- State byte, determinism, mutation, filesystem, network, resource, diagnostic, and error boundaries.
