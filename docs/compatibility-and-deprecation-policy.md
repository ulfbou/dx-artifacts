# Compatibility and deprecation policy

## Status

Accepted for the first consumer-ready DX Artifacts release.

## Version domains

Software releases, carrier versions, envelope versions, canonical profiles,
operation-report schemas, capability schemas, and supported Python API
versions are independent identities. A software release does not implicitly
change any artifact-format identity.

## Stable interfaces

The installed `dx` command, `python -m dx_artifacts`, the generated standalone
`dx.py`, and names explicitly exported through `dx_artifacts.__all__` are
supported interfaces.

Private modules, CLI parser objects, internal classes, spool implementations,
rendering helpers, exception wiring, and generated standalone internals are
not supported interfaces.

## Compatibility

Patch releases preserve supported observable behavior and artifact bytes.
Minor releases may add backward-compatible commands, options, report fields,
capabilities, or supported API exports. Incompatible CLI, API, schema, carrier,
envelope, or profile changes require an explicitly versioned boundary.

Canonical-profile output must remain byte-identical for identical inputs and
effective options. An incompatible canonical representation requires a new
profile identity.

## Deprecation

A supported interface is deprecated before removal. Deprecation documentation
identifies the affected interface, replacement, first deprecated software
release, and earliest permitted removal release. Diagnostics must not
contaminate artifact stdout.

Security or safety defects may require accelerated removal. Such a change must
be explicit, evidence-backed, and recorded in release notes.

## Consumer pinning

Consumers pin a released form by software version and SHA-256, verify its
provenance, and run consumer-owned integration evidence. Generated standalone
artifacts are not edited directly.
