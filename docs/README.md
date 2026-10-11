# DX Artifacts documentation

DX Artifacts is the authoritative Python library product for constructing, parsing, transforming, verifying, inspecting, and safely applying DX artifacts.

## Product identity

```text
DX                  Artifact formats and semantics
dx-artifacts        Python distribution
dx_artifacts        Python import package
python -m dx_artifacts
                    Non-stable reference and conformance adapter
DXS                 Separate future CLI application
```

Release 0.1.0 installs no console command and publishes no supported standalone CLI. ADR-008 controls this boundary.

## Northern star

```text
Workspace state
    ↓
Selection and policy
    ↓
Canonical artifact
    ↓
Transform and verification
    ↓
Explicit output sink
    ↓
Controlled consumption or application
```

## Repository perspective

- DX Artifacts owns generic DX specifications, library implementation, supported Python API, conformance, fixtures, evidence, and library releases.
- `src/dx_artifacts` is the continuing implementation authority.
- Root `dx.py` is transitional implementation and provenance material.
- `tests/baseline/accepted-dx.py` is immutable historical evidence.
- Dx.Domain and Collab are source-evidence repositories and prospective consumers.
- pystd-suite is independently governed and does not supply DX runtime code.

## Documentation map

- [System vision](vision/dx-artifact-system.md)
- [Repository and package boundaries](architecture/repository-and-package-boundaries.md)
- [Artifact model](architecture/artifact-model.md)
- [System architecture](architecture/system-architecture.md)
- [Verification and trust](architecture/verification-and-trust.md)
- [Distribution and integration contract](specifications/distribution-and-integration-contract.md)
- [Compatibility and deprecation policy](compatibility-and-deprecation-policy.md)
- [Decision register](decisions/README.md)
- [Implementation work packages](implementation/implementation-work-packages.md)
- [Evolution roadmap](roadmap/evolution-roadmap.md)

## Contract status

Vision defines direction. Architecture defines constraints. Specifications define normative behavior according to their status. ADRs record decisions. Plans and work packages describe sequence and history without becoming product vocabulary. A feature is supported only when implementation, documentation, and applicable conformance evidence agree.
