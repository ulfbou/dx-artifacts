# DX release-gate evidence contract

## 1. Purpose

The release gate turns conformance claims into explicit, machine-checkable evidence and prevents unsupported capability advertisement.

## 2. Evidence record

Each mandatory check emits one record containing:

```text
identifier
status
contract reference
fixture or test reference
observed result
expected result
diagnostic code, when failed
```

Statuses are `pass`, `fail`, or `blocked`. `blocked` is non-success.

## 3. Gate inputs

The gate declares exact inputs:

- implementation under test;
- controlling carrier fixtures;
- envelope fixtures;
- capability schema;
- supported runtime identity;
- effective resource-limit policy.

Missing inputs fail the gate.

## 4. Required evidence groups

```text
carrier-preservation
envelope-construction
envelope-reading
negative-and-adversarial
resource-boundaries
CLI-and-publication
reports
capability-truthfulness
```

Every acceptance-matrix identifier belongs to exactly one group.

## 5. Artifact evidence

For every produced golden artifact, evidence includes exact byte size and SHA-256. Byte comparison is mandatory where canonical identity is claimed.

Semantic round-trip alone is insufficient for canonical output.

## 6. Capability truthfulness

The gate invokes capability discovery only after functional groups pass.

The advertised set must equal the conformance-gated set. Missing supported capabilities and advertised unsupported capabilities both fail the gate.

## 7. Failure behavior

The gate returns non-zero when any mandatory check fails or is blocked. It must not collapse multiple required checks into one ambiguous summary.

A human-readable summary may accompany evidence but does not replace individual machine-readable results.

## 8. Carrier-production boundary

A deliverable carrier containing implementation changes is produced only after:

- semantic non-regression passes;
- all applicable acceptance identifiers pass;
- exact changed-path scope is proven;
- required reports are complete;
- no mandatory result is blocked.

## 9. Evidence retention

The gate output may be retained as a release artifact or operation report. Retention does not make execution metadata part of canonical carrier or envelope bytes.

## 10. Accepted-baseline evidence

The baseline gate records:

- exact accepted source provenance, byte size, and SHA-256;
- accepted status for root `dx.py`;
- native characterization results for CLI, parsing, selection, serialization, inspection, unpacking, application, diagnostics, and reachable exit categories;
- exact controlling DX v2.0.0 golden carrier identities;
- one classification and evidence reference for every imported compatibility difference.

Missing identity evidence, characterization failure, or unexplained golden-byte drift fails the baseline-preservation gate. An `UNRESOLVED` compatibility finding fails the affected compatibility or extraction gate when generic behavior is unclear; it does not revoke the accepted baseline by itself. Later native distribution gates prove console, module, supported API, and standalone forms against applicable contracts. External consumer repositories separately verify pinned releases by version, digest, and consumer integration evidence.
