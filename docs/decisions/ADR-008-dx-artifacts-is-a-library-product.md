# ADR-008: DX Artifacts is a library product

## Status

Accepted.

## Context

DX Artifacts was documented and packaged as both a Python library and a command-line product. That boundary caused the DX format identity, library distribution, reference command adapter, and potential DXS application to be treated as one product.

The repository must instead release one clearly bounded product. Reusable DX behavior belongs to a Python library. An independently supported command-line application has separate product, interface, compatibility, and release concerns.

## Decision

DX Artifacts is a Python library product.

```text
DX
    Artifact formats, semantics, profiles, and media types.

DX Artifacts
    The Python library product implemented by this repository.

dx-artifacts
    The Python distribution name.

dx_artifacts
    The Python import package.

python -m dx_artifacts
    A non-stable reference and conformance adapter.

DXS
    Reserved for a separate future CLI application that may consume
    the DX Artifacts library.
```

Release 0.1.0 installs no `dx` or `dxs` console command and publishes no standalone CLI as a supported product form.

The supported release boundary is the deliberately exported Python API. Public library operations are use-case-oriented, byte-exact, independent of `argparse`, and do not write to stdout or stderr or raise `SystemExit`.

The native `src/dx_artifacts` package is the continuing implementation authority. The reference adapter may perform argument parsing, rendering, and process-exit mapping, but it must not define artifact semantics independently.

DX carrier and envelope formats, their versions, profile identities, schemas, media types, and canonical bytes remain independent from the software release and are unchanged by this decision.

## Superseded decisions

This ADR supersedes only these parts of ADR-005:

- ownership and publication of a supported command-line product;
- ownership and publication of supported standalone distributions;
- consumer adoption through a standalone executable as a native library release form.

ADR-005 remains controlling for DX Artifacts as the authoritative home of generic DX specifications, implementation, conformance, fixtures, release evidence, and library releases.

This ADR supersedes only these parts of ADR-006:

- classification of DX Artifacts as a command-line product;
- the installed `dx` command as a supported interface;
- module execution as a stable interface;
- a stable CLI compatibility level owned by this library release.

ADR-006 remains controlling for separation between reusable package behavior and process adaptation, deliberate public API growth, inward dependency direction, and process termination only at adapter boundaries.

## Consequences

- The 0.1.0 release gate proves wheel, source distribution, public API, and format conformance.
- `python -m dx_artifacts` may remain for repository integration and conformance, but its syntax and rendering are not stable library contracts.
- Existing CLI behavior remains useful characterization evidence and may inform a future DXS product.
- The library distribution does not reserve or publish an executable name.
- A future DXS product owns command naming, help, configuration, shell behavior, exit mapping, and CLI compatibility.
- Root `dx.py` remains transitional implementation and provenance material until established behavior is migrated to the native package.
- `tests/baseline/accepted-dx.py` remains immutable historical evidence.

## Verification obligations

- Wheel and source distribution install no `dx` or `dxs` entry point.
- Supported imports are explicit and tested from installed artifacts.
- Library functions do not depend on CLI parser objects, stdout, stderr, process termination, or repository-root discovery.
- Current controlling documentation contains one consistent product identity map.
- Module execution is identified as a non-stable reference adapter wherever it is discussed as a current interface.
- No supported standalone CLI is advertised for 0.1.0.
- Carrier and canonical envelope golden artifacts remain byte-identical.
