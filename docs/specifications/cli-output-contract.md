# DX CLI output contract

## Status

Accepted and active following WP-10.

## Command notation

`dx` is the canonical product command. Equivalent module and standalone forms are governed by the distribution and integration contract.

## 1. Artifact-producing commands

```text
pack
envelope
unwrap
```

These commands follow:

```text
No -o supplied     → stdout
-o -               → stdout
-o FILE            → controlled filesystem publication
```

## 2. Pack

```text
dx pack [SOURCE] [OPTIONS]
```

Active defaults:

```text
SOURCE                  .
output format           carrier
output sink             stdout
```

`pack --format envelope` composes carrier construction and envelope transformation.

## 3. Envelope

```text
dx envelope [INPUT] [OPTIONS]
```

Active defaults:

```text
INPUT                   stdin
output sink             stdout
profile                 canonical-v1
logical carrier name    carrier.dx.txt
```

## 4. Unwrap

```text
dx unwrap [INPUT] [OPTIONS]
```

Active defaults:

```text
INPUT                   stdin
output sink             stdout
```

Unwrap writes exact enclosed carrier bytes.

## 5. Output independence

`-o` selects a sink. It does not change artifact bytes, profile behavior, or logical carrier naming.

## 6. Force

`--force` is valid only with `-o FILE`. It is rejected for omitted `-o` and `-o -` because stdout has no DX-controlled conflict policy.

## 7. Format and profile

`pack` supports:

```text
--format carrier
--format envelope
```

Default is `carrier`.

Envelope production supports:

```text
--envelope-profile canonical-v1
--carrier-name NAME
```

Envelope-specific options are invalid with carrier output.

## 8. Carrier-name validation

The logical carrier name:

- is a basename;
- ends in `.dx.txt`;
- contains no slash, backslash, or control character;
- is not `.` or `..`;
- is independent of the output path.

## 9. Diagnostics and reports

Successful artifact production is silent by default.

```text
stdout      artifact bytes
stderr      warnings and errors
--verbose   expanded diagnostics on stderr
--quiet     errors only
```

Machine-readable reports require an explicit report sink and never share artifact stdout.

## 10. Dry-run and check

`--dry-run` produces no artifact and reports planned selection, effective options, and sink behavior. It does not report exact final hashes unless exact bytes were constructed.

A future `--check` constructs and verifies exact bytes internally but publishes nothing.

## 11. No-argument behavior

Recommended behavior:

```text
dx                       show top-level help
dx pack                  pack current directory to stdout
```

## 12. Input-output collision

A filesystem input and filesystem output resolving to the same object are rejected for `envelope` and `unwrap`. Envelope v1 provides no in-place mode.

## 13. Option applicability

Carrier-selection options apply only to `pack`. Envelope-profile options apply only to `envelope` and `pack --format envelope`. Sink options apply to artifact-producing commands.

Irrelevant options are rejected rather than ignored.

## 14. Equivalence contracts

Under identical effective options and stable source state:

```text
pack SOURCE == pack SOURCE -o -
```

```text
pack SOURCE --format envelope == pack SOURCE | envelope
```

```text
pack SOURCE | envelope | unwrap == pack SOURCE
```

Each equality is byte equality.
