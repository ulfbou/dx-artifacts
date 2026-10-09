# DX envelope algorithms

## 1. Construction preconditions

Envelope construction accepts one complete carrier byte source, a registered profile, and a validated logical carrier name.

The carrier must pass required structural verification before transformation.

## 2. Canonical construction

```text
1. Rewind the carrier source.
2. Stream carrier bytes through SHA-256 and count exact bytes.
3. Rewind the carrier source.
4. Create a canonical single-entry ZIP in a binary spool.
5. Write the carrier bytes once into the configured ZIP entry.
6. Finalize the ZIP.
7. Rewind and verify ZIP metadata against canonical-v1.
8. Calculate ZIP size and SHA-256.
9. Write envelope header declarations in canonical order.
10. Base64-encode ZIP bytes using canonical line wrapping.
11. Write %%ENDPAYLOAD and %%END with required LF endings.
12. Parse and canonically verify the complete envelope spool.
13. Publish only after verification passes.
```

The carrier is not regenerated from workspace state during these steps.

## 3. Parsing

```text
1. Read envelope input under the configured maximum size.
2. Require the exact envelope discriminator.
3. Parse directives in required order.
4. Reject missing, duplicate, unknown, or malformed attributes.
5. Validate logical filename and numeric fields before payload decoding.
6. Collect Base64 physical lines under line and total-size limits.
7. Require %%ENDPAYLOAD and %%END.
8. Reject forbidden content after logical end.
```

The parser retains declared metadata separately from decoded bytes.

## 4. Integrity verification

```text
1. Strictly decode Base64 into a bounded binary spool.
2. Compare decoded size with the payload declaration.
3. Compare decoded SHA-256 with the payload declaration.
4. Inspect ZIP metadata without filesystem extraction.
5. Enforce entry count, kind, name, encryption, compression, and limits.
6. Read the sole entry into a bounded carrier spool.
7. Compare carrier size and SHA-256 with the carrier declaration.
8. Parse the carrier from the exact extracted bytes.
9. Compare parsed carrier version with the declared version.
```

A failure stops later-layer success reporting.

## 5. Canonical verification

Canonical verification additionally proves:

- exact directive and attribute order;
- LF-only envelope framing;
- canonical Base64 padding and line width;
- canonical ZIP timestamp, platform, permissions, comments, fields, flags, compression method, and compressed bytes;
- exact canonical reserialization equality when reconstruction is used.

A valid but noncanonical envelope remains readable only where policy permits it. It is never advertised as `canonical-v1` compliant.

## 6. Unwrap

Unwrap performs parse and integrity verification, then copies exact extracted carrier bytes to the selected sink.

It never reparses and reserializes the carrier for output. Carrier parsing is verification only.

## 7. Resource safety

Bound checks precede allocation or expansion wherever practical. ZIP entries are read directly and are never extracted to a directory.

Compression-ratio checks use declared and observed sizes and fail before unbounded carrier materialization.

## 8. Publication

The final envelope or unwrapped carrier is published from a verified spool.

Filesystem publication is atomic under the sink contract. Stdout publication emits artifact bytes only and treats broken-pipe delivery as incomplete.
