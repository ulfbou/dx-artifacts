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

- [ADR-001: Envelope is a separate format](ADR-001-envelope-is-a-separate-format.md), Proposed.
- [ADR-002: Stdout is the default artifact output sink](ADR-002-stdout-is-the-default-output-sink.md), Accepted and activated by WP-10.
- [ADR-003: Canonical profiles replace arbitrary low-level envelope combinations](ADR-003-canonical-profiles-over-low-level-options.md), Proposed.
- [ADR-004: Serialize once and verify exact bytes](ADR-004-serialize-once-verify-exact-bytes.md), Proposed.
- [ADR-005: DX Artifacts is the authoritative home](ADR-005-dx-artifacts-is-the-authoritative-home.md), Accepted.
- [ADR-006: Library core and CLI adapter](ADR-006-library-core-and-cli-adapter.md), Accepted.
- [ADR-007: Dx.Domain supplies the accepted bootstrap baseline](ADR-007-dx-domain-is-the-bootstrap-baseline.md), Accepted.

ADR-007 records the accepted baseline and its preservation obligations. Collab remains compatibility evidence evaluated against that baseline and does not reopen baseline selection.

Vision and roadmap material does not become implemented or supported merely by appearing in documentation.
