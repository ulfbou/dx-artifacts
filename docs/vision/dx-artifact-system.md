# DX artifact system vision

## 1. Purpose

DX Artifacts exists to develop and release DX as a system for moving exact, inspectable, verifiable workspace state across boundaries without losing semantic meaning or byte fidelity.

The initial DX carrier solves a focused problem:

```text
Represent a set of workspace-relative files in one auditable text artifact.
```

The broader system solves a larger problem:

```text
Construct an exact artifact from governed source state, transform it into a
transport-safe representation, verify every boundary, deliver it to an
explicit sink, and apply it only under controlled policy.
```

## 2. Vision statement

DX becomes a deterministic artifact system with five primary capabilities:

1. Construct canonical artifacts from selected workspace state.
2. Transform artifacts into deterministic transport representations.
3. Verify structure, integrity, canonicality, policy compliance, and eventually authenticity.
4. Inspect all supported layers without requiring prior knowledge of the representation.
5. Apply represented workspace changes through an explicit, validated operation.

## 3. Northern-star principles

### 3.1 Exactness

Every artifact and transformation has precise byte semantics.

The system distinguishes:

- semantic content;
- canonical artifact representation;
- transformed representation;
- delivered bytes;
- filesystem effects.

### 3.2 Determinism

Given identical source bytes, logical paths, attributes, format versions, profiles, and effective options, canonical production emits byte-identical output.

Canonical output must not depend on:

- current time;
- machine identity;
- destination filename;
- output directory;
- absolute source path;
- current working directory;
- stdout versus filesystem output;
- unstable archive metadata.

### 3.3 Composability

Artifact-producing operations compose through byte streams.

```bash
dx pack SOURCE |
  dx envelope |
  consumer
```

Composition must not require user-managed temporary files. Integrated convenience commands must use the same logical stages as explicit pipelines.

### 3.4 Verifiability

The system proves properties at the boundary where they matter.

Examples include:

- carrier grammar before carrier consumption;
- payload digest before extraction;
- archive safety before reading an archive entry;
- inner carrier identity before reporting envelope validity;
- application preconditions before workspace mutation.

### 3.5 Safety

Parsing, decoding, decompression, extraction, publication, and application fail closed.

The system defends against:

- unsafe paths and path traversal;
- symlink substitution;
- archive bombs;
- unsupported archive objects;
- duplicate logical paths;
- malformed encodings;
- digest mismatches;
- partial filesystem publication;
- output self-reference;
- unintended overwrite;
- ambiguous version handling.

### 3.6 Separation of concerns

The system preserves these boundaries:

```text
Artifact meaning
Transport representation
Verification policy
Output destination
Application authority
```

No layer silently assumes the responsibilities of another.

### 3.7 Small public surface

The internal architecture may be highly composable, but the public CLI remains understandable.

Profiles encode stable bundles of low-level behavior. Normal users do not assemble arbitrary combinations of compression, encoding, archive metadata, hashing, and framing options.

## 4. System model

```text
Workspace state
    ↓
Selection and policy
    ↓
Canonical artifact
    ↓
Verification
    ↓
Transform pipeline
    ↓
Verification
    ↓
Explicit output sink
    ↓
Inspection or controlled application
```

A command may compose multiple stages, but each stage retains an independently testable contract.

## 5. Identity model

DX distinguishes three identities.

### 5.1 Semantic identity

Semantic identity describes what an artifact represents, including transported paths, file bytes, entry attributes, and operation semantics.

Semantic equivalence does not automatically mean byte identity.

### 5.2 Artifact byte identity

Artifact byte identity is calculated over exact canonical artifact bytes.

```text
carrier_sha256 = SHA-256(exact carrier bytes)
```

### 5.3 Representation identity

Representation identity is calculated over transformed bytes.

```text
compressed_sha256 = SHA-256(exact compressed bytes)
envelope_sha256   = SHA-256(exact envelope bytes)
```

A canonical profile requires identical input artifact bytes and effective options to produce identical representation bytes.

## 6. Intended capabilities

### 6.1 Near-term capabilities

- Produce bare DX v2.0.0 carriers.
- Produce a canonical text envelope containing one complete carrier.
- Use canonical ZIP compression and strict Base64 encoding for the first envelope profile.
- Read artifacts from stdin or files.
- Emit artifacts to stdout or an atomic filesystem sink.
- Recover the byte-exact carrier from an envelope.
- Inspect carrier and envelope layers.
- Verify structure, declared sizes, and cryptographic digests.
- Guarantee equivalence between integrated and composed production.

### 6.2 Medium-term capabilities

- Content-addressed artifact identity.
- Explicit machine-readable report sinks.
- Policy-driven verification.
- Capability discovery.
- Canonicality verification.
- Bounded decoding, decompression, and spooled production.
- Format-agnostic recursive inspection.
- Complete mutation planning before application.

### 6.3 Long-term possibilities

The architecture should leave room for:

- authenticity signatures;
- provenance attestations;
- manifest-indexed carriers;
- explicit delta artifacts with add, replace, delete, rename, and prior-state assertions;
- transactional application;
- content-addressed local storage;
- chunked or trailer-verified streaming envelopes;
- additional registered canonical profiles;
- additional artifact media types.

These possibilities remain non-normative until separately specified and accepted.

## 7. Envelope prototype as first transformation

The first envelope is intentionally narrow:

```text
DX carrier bytes
    ↓
Canonical ZIP containing exactly one .dx.txt entry
    ↓
Strict Base64
    ↓
DX envelope framing
```

The envelope:

- uses a distinct `%%DX-ENVELOPE` namespace;
- transports exactly one byte-exact carrier;
- records carrier and compressed-byte identities;
- is independently versioned from the carrier;
- is reversible without normalization or reinterpretation;
- does not establish authorship, trust, or application authorization.

The integrated form:

```bash
dx pack SOURCE --format envelope
```

must be defined as the same logical composition as:

```bash
dx pack SOURCE |
  dx envelope
```

The carrier is serialized once, verified, and those exact bytes are enveloped.

## 8. Explicit non-goals

DX is not intended to become:

- a general-purpose archive replacement;
- an arbitrary compression frontend;
- a package manager;
- a remote deployment protocol;
- a replacement for source control;
- a format where omission silently means deletion;
- an authorization system merely because it verifies hashes;
- a plugin platform before stable core contracts exist.

## 9. Architectural success condition

The vision is realized when DX can reliably perform this chain:

```text
Governed workspace state
→ deterministic canonical artifact
→ verified transform profile
→ exact transport representation
→ explicit publication sink
→ recursive inspection
→ policy verification
→ controlled application
→ machine-verifiable receipt
```

The system must reach that capability without collapsing its layers into one monolithic command or one overloaded file format.

## 10. Product authority and lineage

DX Artifacts natively owns generic specifications, implementation, supported interfaces, compatibility policy, conformance evidence, and distributions.

The initial implementation entered this repository from the current Dx.Domain release-gate monolith as external bootstrap source material and is accepted as the native controlling bootstrap baseline. Its exact identity and observable behavior are preserved through native evidence. Collab remains an external compatibility-evidence source evaluated against that baseline, while Dx.Domain and Collab remain prospective consumers. The historical .NET DXS repository contributes naming and product lineage but is not Python implementation authority.

Bootstrap authority precedes envelope implementation and activates no proposed capability.
