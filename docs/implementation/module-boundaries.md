# DX implementation module boundaries

## 1. Objective

Extract the accepted bootstrap implementation into native `dx_artifacts` modules around exact artifact bytes, reusable transformations, verification policies, and explicit sinks while preserving accepted carrier behavior.

## 2. Target modules

```text
src/dx_artifacts/
├── errors.py
├── model.py
├── carrier.py
├── envelope.py
├── profiles.py
├── verification.py
├── sources.py
├── sinks.py
├── reports.py
├── selection.py
├── application.py
└── cli.py
```

DX Artifacts may generate a standalone `dx.py` release artifact. The native module tree remains the source authority; the generated standalone artifact is not edited directly.

## 3. Ownership

### `errors.py`

Owns typed operational failures, stable error codes, exit categories, and diagnostic serialization. It does not print.

### `model.py`

Owns immutable artifact descriptors, layer identities, verification results, delivery results, and normalized option records.

### `carrier.py`

Owns DX carrier parsing and canonical carrier serialization. It accepts and returns byte-oriented sources or spools. It does not select workspace files or publish output.

### `envelope.py`

Owns envelope framing, strict parsing, Base64 processing, safe ZIP inspection, exact unwrap, and delegation to profile verification.

### `profiles.py`

Owns immutable registered profile definitions. `canonical-v1` is represented as data and focused functions rather than scattered constants.

### `verification.py`

Owns structural, integrity, canonical, and policy orchestration. It never mutates the workspace.

### `sources.py`

Owns stdin and filesystem artifact sources plus bounded stream readers.

### `sinks.py`

Owns stdout, atomic filesystem, and check sinks. It does not construct artifacts.

### `reports.py`

Owns operation-report schemas and explicit report publication. Reports are independent of artifact sinks.

### `selection.py`

Owns existing candidate discovery, path policy, ignore evaluation, content classification, and selection reports.

### `application.py`

Owns destination planning and workspace mutation. Envelope decoding is not application.

### `cli.py`

Owns argument parsing, option applicability, command orchestration, and mapping typed failures to diagnostics and exit status.

## 4. Dependency rules

```text
cli
→ use-case orchestration
→ carrier, envelope, verification, reports
→ model and profiles
→ sources and sinks
→ platform adapters
```

Forbidden dependencies:

- `carrier` to `cli`;
- `envelope` to `selection`;
- `profiles` to filesystem destinations;
- `sinks` to carrier or envelope grammar;
- `reports` into artifact byte serialization;
- `application` from inspection-only paths.

## 5. Byte ownership

Carrier serialization produces a seekable binary artifact source. Envelope transformation consumes that exact source. Digests are calculated over bytes, not pre-encoding strings.

Text framing uses UTF-8 and LF only where the relevant format specification requires it.

## 6. Incremental native extraction

1. Introduce binary spool and sink abstractions behind existing pack behavior.
2. Route current carrier serialization through the spool without changing golden carrier bytes.
3. Extract typed verification results and typed failures.
4. Implement envelope and profile modules.
5. Add standalone commands.
6. Add integrated `pack --format envelope` through the same functions.
7. Advertise capabilities only after conformance passes.

Each step preserves current carrier fixtures and CLI behavior except where a separately accepted CLI change intentionally supersedes it.

## 7. Package boundary and refactoring states

Target modules live under the import package `dx_artifacts`; their presence does not establish public imports. Only explicitly exported API is supported. CLI parser objects, private module paths, parser classes, spool implementations, exception wiring, and rendering helpers remain internal.

Refactoring proceeds through four transparent states:

```text
Imported monolith
    Exact bootstrap source with preserved behavior.
Transitional package
    Monolith runs behind package and CLI entry points.
Extracted architecture
    Responsibilities move into focused modules without contract changes.
Evolved product
    Envelope and stdout-default behavior arrive through separately gated changes.
```

Only process entry points terminate the process. Reusable package functions return typed results or statuses.
