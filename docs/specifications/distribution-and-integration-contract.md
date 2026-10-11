# DX Artifacts distribution and integration contract

## Status

Accepted under ADR-008 for the DX Artifacts 0.1.0 library release. It changes no carrier or envelope grammar.

## Supported product forms

```text
Wheel distribution
    Installable dx-artifacts library.

Source distribution
    Buildable dx-artifacts library source distribution.

Supported Python API
    import dx_artifacts
```

Each advertised form is produced from one package source authority and must pass applicable packaging, API, format, provenance, and conformance gates.

## Excluded product forms

Release 0.1.0:

- installs no `dx` console command;
- installs no `dxs` console command;
- publishes no standalone CLI as a supported product form;
- does not treat `python -m dx_artifacts` as a stable interface.

Module execution may remain as a non-stable reference and conformance adapter. DXS is reserved for a separate future CLI application.

## Interface stability

The supported Python API is small and explicitly exported. Other modules and classes are internal. Consumers must not depend on CLI parser objects, private modules, internal parser classes, concrete spool implementations, internal exception wiring, or rendering helpers.

Reusable package operations return values, immutable results, or typed failures. They do not render process output or terminate a process.

## Independent identities

- software release version;
- DX carrier format version;
- DX envelope format version;
- canonical profile identity;
- operation and verification report schema versions;
- capability schema version.

A library refactor or package release does not change a format declaration merely because the software version changed.

## Release readiness

A release is ready only when wheel and source distribution, supported API, carrier and envelope preservation, metadata, documentation, and evidence gates pass. Consumer-specific orchestration remains outside DX Artifacts and is verified by the relevant consumer.
