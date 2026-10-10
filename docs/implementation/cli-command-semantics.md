# DX CLI command semantics

## Status

Accepted contract. Stdout-default behavior is active following WP-10.

## Command notation

The currently implemented repository entry point is `python dx.py`. The `dx` console command, `python -m dx_artifacts`, a supported Python API, and a generated standalone release artifact remain WP-11 distribution forms and are not current interfaces. Command examples use `dx` as contract notation for the future canonical product command unless a current invocation is being demonstrated.

## 1. Normalization

CLI parsing produces immutable normalized option records before command execution. Applicability and contradictions are validated before artifact construction.

## 2. `pack`

```text
dx pack [SOURCE] [selection options] [--format carrier|envelope]
           [--envelope-profile canonical-v1]
           [--carrier-name NAME] [-o OUTPUT] [--report FILE]
```

Active defaults:

```text
SOURCE          .
format          carrier
output          stdout
```

Envelope options are rejected unless the effective format is `envelope`.

Carrier production and integrated envelope production share the same selection and carrier-serialization stage.

## 3. `envelope`

```text
dx envelope INPUT [--envelope-profile canonical-v1]
               [--carrier-name NAME] [-o OUTPUT] [--report FILE]
```

Active defaults:

```text
INPUT           required; `-` selects stdin
output          stdout
profile         canonical-v1
carrier name    carrier.dx.txt
```

Input carrier verification precedes transformation.

## 4. `unwrap`

```text
dx unwrap INPUT [-o OUTPUT] [--report FILE]
```

Input is required; `-` selects stdin. Output defaults to stdout. Unwrap performs integrity verification and emits exact carrier bytes.

## 5. `verify`

```text
dx verify INPUT [--policy structural|integrity|canonical]
             [--json]
```

Verification emits no artifact. Human diagnostics use stderr. `--json` writes one report document to stdout.

The default policy is `structural` for a direct carrier and `integrity` for an envelope because envelope validity depends on declared digests.

## 6. `capabilities`

```text
dx capabilities --json
```

Only implemented and conformance-gated features are advertised.

## 7. Active sink options

The following rules are active:

- Omitted `-o` and `-o -` select stdout.
- `-o FILE` selects atomic filesystem publication.
- `--force` is valid only with `-o FILE`.
- Input and output resolving to the same filesystem object are rejected.
- Artifact and report paths resolving to the same object are rejected.

## 8. Diagnostics

Artifact stdout contains artifact bytes only. Stdout publication is silent on stderr by default. Successful filesystem publication writes a completion summary to stderr by default. For `pack -q -o FILE`, stdout contains the output path; for other current artifact-producing commands, `--quiet` suppresses the completion summary. `--verbose` currently adds per-file write diagnostics for `unpack` and `apply`; it does not promise expanded diagnostics for every command.

No artifact-producing execution path mixes diagnostics with artifact bytes on stdout.

## 9. Dry-run and internal check sink

`--dry-run` validates options and selection without claiming exact artifact identity.

The implementation has an internal check sink that consumes complete artifact bytes without publication. No public `--check` CLI option is currently implemented.
## 10. Backward-compatibility transition

WP-10 changed omitted `-o` from numbered-file output to stdout through ADR-002. Help, tests, and capability discovery record the active behavior. Controlled filesystem publication remains available through explicit `-o FILE`.
