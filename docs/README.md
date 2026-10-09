# DX Artifacts documentation

DX Artifacts is the authoritative product repository for DX carrier and envelope specifications, the Python implementation, supported interfaces, conformance evidence, releases, and standalone distributions.

DX evolves from a deterministic carrier codec into a system for constructing, transforming, transporting, verifying, inspecting, and safely applying workspace artifacts.

## Northern stars

### Product northern star

```text
DX provides a deterministic, stream-composable, policy-verifiable system
for constructing, transforming, transporting, inspecting, and safely
applying workspace artifacts.
```

### Architectural northern star

```text
Workspace state
    ↓
Selection and policy
    ↓
Canonical artifact
    ↓
Transform pipeline
    ↓
Integrity and authenticity
    ↓
Transport representation
    ↓
Explicit output sink
    ↓
Verification and controlled application
```

## Repository perspective

This documentation is written from inside DX Artifacts.

- DX Artifacts owns generic DX product behavior and release authority.
- The root `dx.py`, imported from the Dx.Domain release gate, is the accepted bootstrap implementation baseline. It is evidence preserved inside this repository, not continuing authority delegated to Dx.Domain.
- Applicable Collab behavior supplies external compatibility evidence evaluated against the accepted baseline; it does not reopen baseline selection.
- Dx.Domain and Collab are prospective consumer repositories after DX Artifacts publishes a consumer-ready release.
- pystd-suite is related but independently governed and neither owns nor supplies DX runtime code.

## Documentation map

### Direction

- [DX artifact system vision](vision/dx-artifact-system.md) defines the long-term destination, principles, capabilities, and non-goals.

### Provenance and migration

- [Provenance](provenance/README.md) records external implementation lineage and evidence sources.
- [Implementation lineage](provenance/implementation-lineage.md) records the relationship to Dx.Domain, Collab, and historical DXS work.
- [Bootstrap baseline](migration/bootstrap-baseline.md) defines import and baseline acceptance inside DX Artifacts.
- [Consumer transition](migration/consumer-transition.md) defines later adoption by prospective consumer repositories.

### Architecture

- [DX system architecture](architecture/system-architecture.md) defines components, boundaries, dependency direction, and production flows.
- [Artifact model](architecture/artifact-model.md) defines artifacts, representations, identities, sources, sinks, profiles, and reports.
- [Pipeline and streams](architecture/pipeline-and-streams.md) defines byte flow, publication, spooling, and channel semantics.
- [Repository and package boundaries](architecture/repository-and-package-boundaries.md) defines native DX Artifacts ownership and external consumer boundaries.
- [Verification and trust](architecture/verification-and-trust.md) defines verification layers.

### Specifications

- [Distribution and integration contract](specifications/distribution-and-integration-contract.md) defines the supported product forms and future consumer boundary.
- [Envelope v1](specifications/envelope-v1.md) defines the first transport envelope.
- [CLI output contract](specifications/cli-output-contract.md) defines the target stdout-first contract and its activation boundary.

### Decisions and delivery

- [Decision register](decisions/README.md) indexes architecture decisions.
- [Implementation work packages](implementation/implementation-work-packages.md) sequences bootstrap, decomposition, product evolution, release, and later consumer adoption.
- [Evolution roadmap](roadmap/evolution-roadmap.md) defines one controlling product sequence.
- [Implementation delivery roadmap](roadmap/implementation-delivery-roadmap.md) defines release-safe boundaries.

## Scope boundaries

```text
DX carrier
    Represents workspace files and their attributes.
DX envelope
    Carries the exact bytes of one artifact through a transport-safe representation.
Envelope profile
    Defines a deterministic sequence of transport transformations.
Output sink
    Receives complete artifact bytes.
Verification policy
    Defines which properties must be proven before an operation succeeds.
Application policy
    Defines when and how represented workspace changes may be committed.
```

An envelope does not replace the carrier format. Compression does not redefine carrier semantics. A filesystem output path does not define artifact identity. Integrity does not establish authenticity or application authorization.

## Bootstrap state and product authority

DX Artifacts is authoritative for its specifications, architecture, release policy, and accepted repository state.

The imported Dx.Domain implementation is the controlling bootstrap baseline. Its exact identity and observable behavior are preserved through the accepted manifest, golden carrier fixtures, and characterization tests. Collab differences are classified as compatibility evidence against that baseline; an unresolved generic obligation may block later extraction but does not revoke baseline acceptance by itself.

No documentation statement alone proves implementation behavior. Capabilities become supported only after the applicable conformance gate passes.

## Contract status

- Vision defines direction and principles.
- Architecture defines product boundaries and constraints.
- Specifications define proposed or accepted normative behavior according to their status.
- ADRs record decisions and their status.
- Roadmaps sequence work without activating capabilities.
- Bootstrap preserves observed carrier behavior and existing CLI defaults.
- Envelope behavior and stdout-default behavior remain inactive until their separately defined implementation and compatibility boundaries pass.
