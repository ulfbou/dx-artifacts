# DX artifact model

## 1. Purpose

This document defines the conceptual model shared by carrier construction, envelope transformation, verification, inspection, publication, and application.

## 2. Artifact

An artifact is a finite sequence of bytes with declared semantics.

An artifact descriptor contains:

- media type;
- format version;
- exact byte length;
- cryptographic digest;
- optional logical name.

Artifact identity refers to exact bytes unless a document explicitly discusses semantic equivalence.

## 3. Representation and transformation

A representation is one concrete byte encoding of an artifact or another representation.

```text
DX carrier bytes
→ canonical ZIP bytes
→ Base64 text
→ DX envelope bytes
```

A transform maps one representation to another under a versioned contract. A successful reverse transform must recover the declared inner bytes exactly.

## 4. Profile

A profile is a registered, versioned bundle of transform and canonicalization rules.

A profile can define:

- accepted input media type;
- output media type;
- archive structure;
- compression method and level;
- metadata normalization;
- encoding alphabet and line wrapping;
- digest algorithms;
- resource limits;
- verification obligations.

Profiles prevent arbitrary low-level option combinations from becoming accidental public contracts.

## 5. Identity layers

### 5.1 Semantic identity

Semantic identity describes what an artifact represents. For a carrier it includes transported paths, exact file bytes, entry attributes, and carrier semantics.

Semantic equivalence does not necessarily imply byte identity.

### 5.2 Artifact byte identity

Artifact byte identity is calculated over exact artifact bytes.

```text
carrier_sha256 = SHA-256(exact carrier bytes)
```

### 5.3 Representation identity

Representation identity is calculated over transformed bytes.

```text
compressed_sha256 = SHA-256(exact canonical ZIP bytes)
envelope_sha256   = SHA-256(exact envelope bytes)
```

A canonical profile must make representation identity reproducible from the same input bytes and effective options.

## 6. Logical names

A logical name identifies an artifact inside a containing representation.

A logical name:

- is independent of the output sink;
- must not be derived implicitly from `-o`;
- is not an extraction destination;
- must satisfy profile-specific safety rules.

Envelope v1 uses `carrier.dx.txt` as the default logical carrier name.

## 7. Media types

Stable internal identifiers support dispatch and reporting:

```text
application/vnd.dx.carrier
application/vnd.dx.envelope
application/vnd.dx.operation-report+json
application/vnd.dx.verification-report+json
```

Formal external registration is outside the current scope.

## 8. Source

A source provides workspace state or artifact bytes.

Initial source kinds:

- workspace selection;
- filesystem file;
- standard input.

A source does not define output naming or publication guarantees.

## 9. Sink

A sink receives complete artifact bytes.

Initial sink kinds:

- stdout;
- filesystem publication;
- check or discard.

The sink changes delivery guarantees, not artifact identity.

## 10. Report

A report describes an operation, verification result, or delivery result. It is not part of artifact stdout and does not alter artifact identity.

Reports may include execution-specific data such as destination paths or elapsed time because reports are not canonical artifacts unless separately specified.

## 11. Canonical and execution metadata

Canonical bytes exclude unstable execution metadata unless a specification explicitly requires it.

The following normally belong in reports rather than canonical artifacts:

- production time;
- hostname;
- absolute workspace path;
- destination path;
- process identifier;
- temporary-file location;
- elapsed time.

## 12. Completeness

Artifact production succeeds only when complete bytes have been constructed, required verification has passed, and the selected sink has accepted the delivery.

A temporary spool, prefix, or partially written stream is not a successfully delivered artifact.

## 13. Product and release identity

Artifact identities and product release identities are separate. Software release version, carrier format version, envelope format version, profile identity, report schema versions, and capability schema version evolve independently.

A package refactor or standalone distribution release does not alter carrier bytes or declarations merely because the software version changed. All supported distribution forms originate from DX Artifacts and prove the same applicable artifact contracts before advertisement. External consumer repositories pin a released form; they do not define artifact identity.
