# DX error taxonomy

## 1. Principle

Errors are typed at the layer that detects them. CLI code maps typed failures to stable diagnostic codes and process exit categories.

## 2. Exit categories

```text
0   success
1   comparison or check found a defined negative result
2   invalid command usage
3   malformed or unsupported artifact
4   input or output I/O failure
5   output conflict or unsafe publication target
6   integrity, canonicality, or policy verification failure
7   empty selection
```

Envelope support reuses these categories rather than creating an exit code for every condition.

## 3. Stable diagnostic codes

Suggested codes:

```text
usage.invalid_option_combination
usage.option_not_applicable
artifact.unrecognized_format
artifact.unsupported_version
envelope.invalid_framing
envelope.invalid_attribute
envelope.invalid_base64
envelope.unsafe_archive
envelope.unsupported_profile
verification.size_mismatch
verification.digest_mismatch
verification.noncanonical
verification.policy_violation
carrier.invalid
io.read_failed
io.write_failed
output.exists
output.symlink
output.same_as_input
output.same_as_report
selection.empty
```

Codes are machine-oriented and stable. Messages may improve without changing code meaning.

## 4. Layer precedence

Report the earliest independently established failure. Do not report a digest mismatch when Base64 could not be decoded, or an invalid carrier when archive safety failed first.

## 5. Compound results

Verification may collect multiple findings only when continuing is safe and does not imply success at a blocked later layer.

Canonical checks may report several deviations after structural and integrity verification have passed.

## 6. JSON diagnostics

Machine-readable diagnostics contain:

```text
code
message
layer
path, when applicable
details, when stable and safe
```

They do not include tracebacks by default.

## 7. Exception boundaries

Internal programming errors are not converted into misleading operational diagnostics. Unexpected exceptions return failure and may include a traceback only under an explicit debugging mode.

## 8. Sensitive data

Diagnostics avoid including transported payload content, secrets, absolute paths unless operationally required, or unbounded hostile input excerpts.

Long malformed lines are represented through bounded previews plus complete length and, where useful, a digest.
