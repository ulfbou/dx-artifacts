# DX Artifacts implementation work packages

## 1. Purpose

This plan sequences bootstrap, behavior-preserving decomposition, product evolution, consumer-ready release, and later external adoption. Every work package leaves DX Artifacts in a testable state.

## 2. Global rules

Every work package must preserve established carrier semantics unless its scope explicitly changes them, compare candidate behavior with controlling state, test every changed contract, avoid unsupported capability claims, and stop when mandatory evidence is missing.

## 3. WP-00A: Bootstrap the new repository

### Scope

- Establish DX Artifacts project metadata and controlling documentation.
- Establish native repository, distribution, package, console, module, and standalone identities.
- Record external provenance and future consumer boundaries.
- Add no implementation or envelope behavior.

### Acceptance

- Documentation consistently speaks from the DX Artifacts repository viewpoint.
- Dx.Domain and Collab appear only as attributed sources and prospective external consumers.
- No grammar or CLI behavior changes.

## 4. WP-00B: Import the bootstrap candidate

### Scope

- Import Dx.Domain `scripts/release-gate/dx.py` without semantic rewriting.
- Preserve a temporary compatibility entry point.
- Capture candidate software, CLI, diagnostics, exit, and carrier behavior.
- Establish package and module invocation around the imported behavior.

### Exclusions

No envelope implementation, stdout-default activation, diagnostic rewrite, or structural decomposition.

## 5. WP-00C: Accept the cross-repository baseline

### Scope

- Import applicable Dx.Domain evidence.
- Import applicable Collab evidence.
- Run both against the candidate inside DX Artifacts.
- Classify every difference.
- Establish controlling golden fixtures.

### Acceptance

- Every difference is classified.
- `REQUIRED_CORE` and `DEFECT` findings are resolved.
- No `UNRESOLVED` finding remains.
- Exact controlling DX v2.0.0 carrier bytes are recorded.

## 6. WP-01: Binary artifact spool

Introduce a seekable binary spool, route carrier serialization through exact UTF-8 bytes, preserve controlling carrier bytes, and keep accepted CLI defaults unchanged.

## 7. WP-02: Explicit artifact sinks

Add stdout, atomic filesystem, and check sinks while keeping publication policy outside carrier construction and preserving accepted conflict and symlink behavior.

## 8. WP-03: Typed verification and errors

Add structural verification results, stable error codes, and layer classification while preserving accepted exit behavior.

## 9. WP-04: Envelope parser and integrity verifier

Implement bounded envelope parsing, strict Base64 decoding, safe ZIP validation, integrity verification, and exact carrier recovery. Do not advertise a canonical writer.

## 10. WP-05: Canonical envelope writer

Implement `canonical-v1`, verify produced bytes before publication, preserve exact inner carrier bytes, and gate output with golden fixtures.

## 11. WP-06: Standalone envelope commands

Add `envelope`, `unwrap`, and `verify` orchestration through native package functions and supported CLI adapters.

## 12. WP-07: Integrated pack transformation

Add `pack --format envelope` using one verified carrier serialization and prove exact equality with explicit composition.

## 13. WP-08: Report contracts

Add operation-report sinks and exact artifact, representation, verification, and delivery evidence.

## 14. WP-09: Capability discovery

Add truthful `capabilities --json` output that advertises only conformance-gated behavior.

## 15. WP-10: Stdout-default compatibility activation

Change omitted output for artifact-producing commands to stdout only after the compatibility decision, help, migration guidance, and acceptance evidence pass. Preserve `-o FILE` publication.

## 16. WP-11: Consumer-ready distribution

### Scope

- Produce versioned installable and standalone forms from one source identity.
- Record release provenance, generation procedure, digests, and conformance results.
- Prove console, module, supported API, and standalone behavior where applicable.
- Publish compatibility and deprecation policy required for consumer adoption.

### Acceptance

- Each advertised form passes its applicable gate.
- The standalone artifact is mechanically traceable to the source release.
- Release identities remain separate from carrier, envelope, profile, and schema identities.

## 17. WP-12: External consumer adoption

### Scope

- Support independent Dx.Domain and Collab adoption of a pinned consumer-ready release.
- Keep repository-specific orchestration and policy in each consumer.
- Record version, digest, acquisition, integration evidence, rollback, and former-copy disposition.

### Boundary

WP-12 is downstream external integration. It does not block WP-01 through WP-11 and does not transfer native product ownership out of DX Artifacts.

## 18. Stop conditions

Stop the active package when controlling behavior cannot be reproduced, a golden fixture changes outside scope, required evidence is unavailable, deterministic output cannot be maintained, or ambiguity affects bytes, safety, or compatibility.
