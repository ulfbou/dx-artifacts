# DX CLI command semantics

## Status

Target contract. Bootstrap and behavior-preserving decomposition retain the accepted baseline CLI behavior. Stdout-default behavior becomes active only when WP-10 passes its compatibility gate.

## Command notation

`dx` is the canonical product command. `python -m dx_artifacts` is the equivalent module form. `python dx.py` is the standalone release form. The examples below use `dx`.

## 1. Normalization

CLI parsing produces immutable normalized option records before command execution. Applicability and contradictions are validated before artifact construction.

## 2. `pack`

```text
dx pack [SOURCE] [selection options] [--format carrier|envelope]
           [--envelope-profile canonical-v1]
           [--carrier-name NAME] [-o OUTPUT] [--report FILE]
```

Target defaults after WP-10 activation:

```text
SOURCE          .
format          carrier
output          stdout
```

Envelope options are rejected unless the effective format is `envelope`.

Carrier production and integrated envelope production share the same selection and carrier-serialization stage.

## 3. `envelope`

```text
dx envelope [INPUT] [--envelope-profile canonical-v1]
               [--carrier-name NAME] [-o OUTPUT] [--report FILE]
```

Target defaults after the applicable command and WP-10 gates pass:

```text
INPUT           stdin
output          stdout
profile         canonical-v1
carrier name    carrier.dx.txt
```

Input carrier verification precedes transformation.

## 4. `unwrap`

```text
dx unwrap [INPUT] [-o OUTPUT] [--report FILE]
```

After the applicable command and WP-10 gates pass, input defaults to stdin and output defaults to stdout. It performs integrity verification and emits exact carrier bytes.

## 5. `verify`

```text
dx verify [INPUT] [--policy structural|integrity|canonical]
             [--json]
```

Verification emits no artifact. Human diagnostics use stderr. `--json` writes one report document to stdout.

The default policy is `structural` for a direct carrier and `integrity` for an envelope because envelope validity depends on declared digests.

## 6. `capabilities`

```text
dx capabilities --json
```

Only implemented and conformance-gated features are advertised.

## 7. Target sink options

The following rules become active at WP-10:

- Omitted `-o` and `-o -` select stdout.
- `-o FILE` selects atomic filesystem publication.
- `--force` is valid only with `-o FILE`.
- Input and output resolving to the same filesystem object are rejected.
- Artifact and report paths resolving to the same object are rejected.

## 8. Diagnostics

Successful artifact production is silent by default. `--verbose` adds stderr diagnostics. `--quiet` suppresses non-error diagnostics.

No execution path writes diagnostics to artifact stdout.

## 9. Dry-run and check

`--dry-run` validates options and selection without claiming exact artifact identity.

`--check` constructs and verifies exact bytes through a check sink. It publishes no artifact and may produce an explicit operation report.

## 10. Backward-compatibility transition

Changing omitted `-o` from numbered-file output to stdout is a public CLI change. The implementation must introduce it through an accepted release decision, update help and tests, and provide an explicit replacement for any retained numbered-output convenience.
