# DX Artifacts public roadmap

## Purpose

DX Artifacts is evolving from a deterministic carrier utility into a verifiable artifact system for constructing, transporting, inspecting, and safely applying exact workspace state.

This roadmap communicates intended product outcomes. It does not claim that a capability is implemented, verified, supported, released, or available merely because it appears here. A capability becomes supported only after its governing decisions, contracts, implementation, and conformance evidence agree.

## Strategic objectives

DX Artifacts aims to:

1. Preserve exact workspace content and established carrier behavior.
2. Produce deterministic transport representations that recover the original artifact byte-for-byte.
3. Verify structure, integrity, canonicality, and policy at explicit boundaries.
4. Support composable command-line workflows without mixing artifacts, diagnostics, and reports.
5. Publish installable and standalone forms from one authoritative source.
6. Keep generic product behavior separate from repository-specific orchestration and policy.
7. Apply represented workspace changes only through explicit, validated operations.

## Roadmap principles

- **Evidence before claims.** Documentation and roadmap placement do not prove implementation behavior.
- **Exact bytes are controlling evidence.** Semantic equivalence is insufficient where canonical identity is claimed.
- **Compatibility changes are explicit.** Established behavior is preserved unless a separately accepted and verified decision changes it.
- **Capabilities are independently gated.** Reading, writing, reporting, publishing, and applying do not become supported as one undifferentiated feature.
- **Safety fails closed.** Malformed, unsafe, unverifiable, or resource-exhausting input must not proceed as successful.
- **One product authority.** DX Artifacts owns generic specifications, implementation, conformance, and releases. Consumer-specific policy remains with consumers.
- **Sequence is not schedule.** This roadmap communicates outcomes and dependency order, not delivery dates.

## Horizon 1: Reliable carriers

### Outcome

A verified foundation for producing, inspecting, and applying deterministic DX carriers without losing exact file content or established behavior.

### Focus

- Preserve and characterize existing carrier behavior.
- Strengthen deterministic production and byte-exact fixtures.
- Establish one native package and CLI architecture.
- Separate construction, verification, publication, inspection, and application.
- Maintain predictable diagnostics and failure categories.
- Classify relevant external compatibility evidence before affected behavior is extracted.

### Completion signal

Supported carrier behavior is represented by passing conformance evidence, established carrier bytes are protected against unintended drift, and the native product boundary preserves verified contracts.

## Horizon 2: Verifiable transport envelopes

### Outcome

A text-safe transport representation that encloses one complete DX carrier, verifies its integrity, and recovers the original carrier bytes exactly.

### Focus

- Introduce envelope parsing independently from carrier parsing.
- Enforce bounded input, decoding, decompression, and archive inspection.
- Reject unsafe archive structures without extracting them to a directory.
- Verify declared byte lengths and cryptographic digests.
- Recover the enclosed carrier without normalization or reserialization.
- Add deterministic production through a versioned canonical profile.
- Protect canonical output with golden fixtures.

### Completion signal

DX can safely read, verify, produce, and unwrap the supported envelope format; repeated canonical production is byte-identical; and unwrap reproduces the original carrier exactly.

## Horizon 3: Composable workflows

### Outcome

DX operations compose through standard streams while preserving artifact bytes and clear publication guarantees.

### Focus

- Accept artifact input from files or standard input where applicable.
- Emit artifact bytes to standard output or a controlled filesystem sink.
- Keep artifact stdout free from diagnostics and reports.
- Provide standalone envelope and unwrap operations.
- Provide integrated carrier-to-envelope production.
- Guarantee byte equality between integrated and explicitly composed workflows.
- Treat incomplete downstream delivery as unsuccessful.

### Completion signal

Integrated and piped operations are mechanically proven equivalent, and artifact channels remain uncontaminated.

## Horizon 4: Automation and transparent evidence

### Outcome

Automation can determine what DX supports and obtain structured evidence about production, verification, and delivery.

### Focus

- Add machine-readable operation reports.
- Record exact artifact and representation identities.
- Distinguish construction, verification, and completed delivery.
- Add deterministic capability discovery.
- Advertise only implemented and conformance-gated behavior.
- Keep reports separate from canonical artifact bytes.
- Produce explicit evidence for every mandatory release-gate obligation.

### Completion signal

Automation can consume stable reports and capability data without parsing human-readable help or diagnostics, and unsupported behavior is absent from advertised capabilities.

## Horizon 5: Supported distribution

### Outcome

DX is available through versioned product forms originating from one source authority.

### Focus

- Publish an installable command-line product.
- Support module execution.
- Define a small, explicit Python API.
- Produce a traceable standalone artifact.
- Record release provenance, identities, digests, and generation procedures.
- Apply compatibility and deprecation policies consistently.
- Verify each advertised product form against applicable contracts.

### Completion signal

Every advertised distribution form is traceable to one source release and passes its applicable behavior, packaging, provenance, and conformance gates.

## Horizon 6: Independent consumer adoption

### Outcome

External repositories can adopt a pinned DX Artifacts release while retaining their own orchestration, policy, adapters, and integration evidence.

### Focus

- Support independent consumer transitions.
- Record pinned versions and artifact identities.
- Verify consumer integration against the pinned release.
- Define coexistence and rollback.
- Prevent vendored copies from becoming independent generic implementations.
- Correct generic defects in DX Artifacts rather than consumer forks.

### Completion signal

A consumer transition is complete only for the consumer whose integration evidence passes. One consumer's migration neither proves nor blocks another's.

## Future exploration

Potential future capabilities include:

- controlled mutation planning;
- explicit preconditions;
- transactional application;
- machine-verifiable receipts;
- provenance attestations;
- authenticity signatures;
- explicit delta artifacts;
- content-addressed storage;
- chunked transport;
- additional canonical profiles;
- additional artifact types.

These are architectural possibilities, not delivery commitments. They remain non-normative until separately specified and accepted.

## Summary

```text
Reliable carriers
→ Verifiable transport envelopes
→ Composable workflows
→ Automation and transparent evidence
→ Supported distribution
→ Independent consumer adoption
→ Controlled application and trust
```
