# DX Artifacts documentation standards

## Status

Accepted repository standard.

## Authority

- `docs/README.md` is the documentation entry point.
- ADR-008 controls product identity and release forms.
- `docs/vision/dx-artifact-system.md` defines direction and non-goals.
- Roadmaps control outcome sequence without activating capabilities.
- Work-package documents retain planning and historical sequence.
- Accepted ADRs control their recorded decisions.
- Specifications are normative only according to their status.
- Avoid duplicating normative requirements; link to the controlling document.

## Requirements

- Write from inside the DX Artifacts repository.
- Describe DX Artifacts as a Python library product.
- Distinguish DX formats, the `dx-artifacts` distribution, the `dx_artifacts` package, the non-stable reference adapter, and future DXS.
- Describe Dx.Domain and Collab only as attributed source-evidence repositories or future consumers.
- Distinguish accepted baseline fact, implemented behavior, proposed contract, supported library API, future plan, and external compatibility evidence.
- Describe authoritative inputs, outputs, identities, and evidence.
- Avoid unsupported release or interface claims.
- Preserve qualifications when rewriting accepted content.
- Keep software release, carrier format, envelope format, profile, report-schema, and capability-schema identities separate.

## Tool documentation

- Do not document `dx` or `dxs` as an installed DX Artifacts command.
- Label `python -m dx_artifacts` as a non-stable reference and conformance adapter.
- Label root or historical `dx.py` references as transitional, bootstrap, or provenance references.
- Do not advertise a standalone CLI as a supported 0.1.0 library form.
- Command-oriented documents describe adapter behavior or historical characterization, not stable library API.
