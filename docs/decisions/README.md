# DX Artifacts architecture decision records

Architecture decision records capture decisions that constrain native implementation, public behavior, or product governance.

## States

```text
Proposed
Accepted
Superseded
Rejected
```

## Register

- [ADR-001: Envelope is a separate format](ADR-001-envelope-is-a-separate-format.md), Accepted and implemented.
- [ADR-002: Stdout is the default artifact output sink](ADR-002-stdout-is-the-default-output-sink.md), Accepted for the reference adapter and existing behavioral evidence.
- [ADR-003: Canonical profiles replace arbitrary low-level envelope combinations](ADR-003-canonical-profiles-over-low-level-options.md), Accepted and implemented.
- [ADR-004: Serialize once and verify exact bytes](ADR-004-serialize-once-verify-exact-bytes.md), Accepted and implemented.
- [ADR-005: DX Artifacts is the authoritative home](ADR-005-dx-artifacts-is-the-authoritative-home.md), Accepted and partially superseded by ADR-008.
- [ADR-006: Library core and CLI adapter](ADR-006-library-core-and-cli-adapter.md), Accepted and partially superseded by ADR-008.
- [ADR-007: Dx.Domain supplies the accepted bootstrap baseline](ADR-007-dx-domain-is-the-bootstrap-baseline.md), Accepted.
- [ADR-008: DX Artifacts is a library product](ADR-008-dx-artifacts-is-a-library-product.md), Accepted and controlling for product identity and release forms.

ADR-008 controls the library product boundary. ADR-007 controls accepted bootstrap provenance. Vision and roadmap material does not make a capability supported merely by describing it.
