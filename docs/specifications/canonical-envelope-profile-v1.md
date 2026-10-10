# Canonical envelope profile v1

## 1. Status

Accepted and active following WP-05.

## 2. Profile identity

```text
canonical-v1
```

A profile name identifies one immutable set of output rules. Any incompatible change requires a new profile name.

## 3. Transform stack

```text
verified DX carrier bytes
→ canonical single-entry ZIP
→ RFC 4648 Base64
→ DX envelope v1 framing
```

The transform accepts one verified DX carrier and produces one DX envelope.

## 4. Carrier entry

The ZIP archive contains exactly one regular-file entry.

The entry name:

- equals the envelope `filename` declaration;
- is a UTF-8 basename;
- ends in `.dx.txt`;
- contains no slash, backslash, NUL, control character, `.` segment, or `..` segment;
- defaults to `carrier.dx.txt`.

The entry payload is the exact carrier byte sequence. No text decoding or newline normalization occurs.

## 5. ZIP metadata

Canonical ZIP production uses:

```text
entry count                 1
compression method          DEFLATE
compression level           9
entry timestamp             1980-01-01 00:00:00
creator system              Unix
regular-file mode           0644
archive comment             empty
entry comment               empty
extra fields                empty
entry order                 the single carrier entry
```

The general-purpose flags must represent an unencrypted, non-streaming regular entry. The UTF-8 filename flag is set when required by the encoded filename.

Writers must know the complete carrier bytes before writing the ZIP entry so that the canonical archive does not depend on data-descriptor streaming behavior.

## 6. Compression determinism

The authoritative implementation and its accepted golden fixtures define the canonical DEFLATE output for `canonical-v1`.

A runtime or dependency change that changes golden ZIP bytes is incompatible with `canonical-v1` until one of these actions is accepted:

1. restore byte-identical output;
2. deliberately version the profile;
3. explicitly redefine canonical identity through a superseding decision.

Semantic equivalence of decompressed bytes is insufficient for canonical-profile conformance.

## 7. Base64 representation

Canonical Base64 uses:

```text
alphabet                    RFC 4648 standard alphabet
padding                     required
line width                  76 characters
payload indentation         none
blank payload lines         forbidden
line ending                 LF
final payload newline       exactly one before %%ENDPAYLOAD
```

The final Base64 line may contain fewer than 76 characters. Empty payloads are invalid.

## 8. Envelope framing

Directive order is fixed:

```text
%%DX-ENVELOPE
%%CARRIER
%%PAYLOAD
<Base64 payload>
%%ENDPAYLOAD
%%END
```

Attributes appear in the order specified by the envelope v1 grammar. One LF terminates every directive line. The complete envelope ends with one LF after `%%END`.

## 9. Digests and sizes

The profile uses SHA-256 expressed as 64 lowercase hexadecimal characters.

```text
carrier size        exact carrier byte count
carrier sha256      SHA-256 of exact carrier bytes
payload size        exact canonical ZIP byte count
payload sha256      SHA-256 of exact canonical ZIP bytes
```

Envelope-byte identity may be calculated by inspection or reporting but is not declared inside the envelope because self-declaration would be recursive.

## 10. Resource limits

Implementations expose policy-controlled upper bounds. The profile requires the limits to be checked but does not embed deployment-specific maximum values in canonical bytes.

Required limit categories:

- envelope input bytes;
- Base64 physical-line length;
- decoded ZIP bytes;
- extracted carrier bytes;
- compression ratio;
- ZIP entry count.

## 11. Canonical verification

Canonical verification reconstructs or independently checks all profile-controlled properties, including exact framing, attribute order, LF usage, Base64 wrapping, ZIP metadata, compressed bytes, sizes, and digests.

A structurally valid envelope that differs from these rules is noncanonical.

## 12. Error handling

Writers fail before publication when canonical bytes cannot be produced.

Readers distinguish:

- malformed envelope;
- integrity mismatch;
- unsafe archive;
- valid but noncanonical representation;
- invalid inner carrier;
- unsupported profile.
