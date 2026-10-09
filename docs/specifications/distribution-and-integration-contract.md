# DX Artifacts distribution and integration contract

## Status

Proposed product-boundary contract. It changes no carrier or envelope grammar.

## Native supported forms

```text
Installed CLI
    dx ...
Module execution
    python -m dx_artifacts ...
Supported Python API
    import dx_artifacts
Standalone release artifact
    python dx.py ...
```

All supported forms are produced by DX Artifacts from one source authority. A form is advertised only after applicable conformance passes.

## Command notation

DX Artifacts documentation uses `dx` as the canonical product command once the console distribution is available.

`python -m dx_artifacts` is the equivalent module form. `python dx.py` identifies the standalone release artifact. References to a source repository's historical `dx.py` are explicitly labeled as bootstrap or provenance references rather than product command notation.

## Interface stability

The CLI is the broad interoperability boundary. The Python API is small and explicitly exported. Other modules and classes are internal.

Consumers must not depend on CLI parser objects, private modules, internal parser classes, concrete spool implementations, internal exception wiring, or rendering helpers.

Reusable package operations return typed values, results, or statuses. Only process entry points translate status into process termination.

## Standalone artifact

The standalone `dx.py` is generated or assembled from the same released source identity as the package and CLI. Its release evidence records software version, source release identity, SHA-256, generation procedure, and applicable conformance results.

A consumer pins and verifies the artifact and must not edit it directly.

## Independent identities

- software release version;
- DX carrier format version;
- DX envelope format version;
- canonical profile identity;
- operation and verification report schema versions;
- capability schema version.

A software refactor or package release does not change a format declaration merely because the software version changed.

## Consumer-ready release

A release is consumer-ready only when its advertised distribution forms pass applicable behavior, packaging, provenance, and conformance gates. Consumer-specific orchestration remains outside DX Artifacts and is verified by the relevant consumer repository.
