# Envelope v1 acceptance matrix

## 1. Purpose

This matrix maps envelope contracts to mandatory executable evidence. Every mandatory row must pass before capabilities advertise envelope v1 or `canonical-v1`.

## 2. Carrier preservation

```text
ID C01  Existing v2.0.0 carrier golden bytes remain unchanged.
ID C02  Existing readable carrier versions retain structural parsing.
ID C03  Binary, escaped-text, read-only, and trailing-newline entries round-trip.
ID C04  Carrier stdout and filesystem sink bytes are identical.
```

## 3. Envelope construction

```text
ID E01  One verified carrier produces one envelope.
ID E02  ZIP contains exactly one regular .dx.txt entry.
ID E03  ZIP metadata equals canonical-v1 constants.
ID E04  Base64 uses required alphabet, padding, LF, and 76-column wrapping.
ID E05  Declared sizes and SHA-256 values match exact bytes.
ID E06  Repeated production is byte-identical.
ID E07  Integrated and piped production are byte-identical.
```

## 4. Envelope reading and unwrap

```text
ID U01  Canonical envelope passes structural, integrity, and canonical policies.
ID U02  Unwrap returns exact original carrier bytes.
ID U03  Unwrap never extracts ZIP content to a directory.
ID U04  Declared carrier version must equal parsed carrier version.
```

## 5. Negative and adversarial cases

```text
ID N01  Malformed framing is rejected as an invalid artifact.
ID N02  Invalid Base64 is rejected before ZIP verification.
ID N03  ZIP size or digest mismatch is a verification failure.
ID N04  Multiple, traversal, absolute, symlink, encrypted, or nonregular entries are rejected.
ID N05  Carrier size or digest mismatch is a verification failure.
ID N06  Invalid inner carrier is reported after envelope integrity passes.
ID N07  Noncanonical but structurally valid representation fails canonical policy.
ID N08  Unsupported profile is rejected explicitly.
```

## 6. Resource boundaries

```text
ID R01  Envelope input limit is enforced.
ID R02  Base64 physical-line limit is enforced.
ID R03  Decoded ZIP limit is enforced.
ID R04  Extracted carrier limit is enforced.
ID R05  Compression-ratio limit is enforced.
ID R06  Entry-count limit is enforced before extraction.
```

## 7. CLI and publication

P01 and P03 are mandatory only when WP-10 activates stdout-default behavior. The remaining applicable publication checks gate their respective implementation boundaries.

```text
ID P01  After WP-10, omitted -o and -o - produce identical stdout bytes.
ID P02  -o FILE produces identical artifact bytes with atomic publication.
ID P03  --force is rejected for stdout.
ID P04  Same input and output object is rejected.
ID P05  Same artifact and report object is rejected.
ID P06  Artifact stdout contains no diagnostics.
ID P07  Broken pipe does not claim completed delivery.
ID P08  Requested report failure returns non-zero.
```

## 8. Capabilities and reports

```text
ID A01  Capabilities JSON conforms to its schema.
ID A02  Unsupported or ungated features are absent.
ID A03  Successful operation report records exact artifact identity.
ID A04  Failed delivery never reports delivery.completed=true.
ID A05  Report destination does not change artifact bytes.
```

## 9. Gate behavior

The release gate prints one explicit result per identifier, returns non-zero for any mandatory failure, and treats missing evidence as failure.

Capability advertisement is tested after the complete matrix and must reflect the passed implementation, not planned functionality.
