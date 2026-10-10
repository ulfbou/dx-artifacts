# DX envelope v1

## 1. Status

Accepted and active following WP-06 and WP-07.

## 2. Purpose

A DX envelope transports the exact bytes of one DX carrier through a text-safe, integrity-verifiable representation. It does not alter carrier semantics.

## 3. Format discriminator

The envelope uses a distinct namespace:

```text
%%DX-ENVELOPE
```

The carrier continues to use `%%DX`. Envelope and carrier versions are independent.

## 4. Prototype grammar

```text
%%DX-ENVELOPE v1.0.0 profile="canonical-v1"
%%CARRIER filename="carrier.dx.txt" version="v2.0.0" size="45678" sha256="<64 lowercase hexadecimal characters>"
%%PAYLOAD media_type="application/zip" encoding="base64" size="12345" sha256="<64 lowercase hexadecimal characters>"
<canonical Base64 payload>
%%ENDPAYLOAD
%%END
```

## 5. Envelope rules

- Version is `v1.0.0`.
- Profile is `canonical-v1`.
- Exactly one carrier declaration is required.
- Exactly one payload is required.
- `%%END` is required.
- Non-whitespace data after `%%END` is forbidden.
- Nested envelopes are forbidden.

## 6. Carrier declaration

- `filename` is the logical ZIP-entry name.
- It is a basename ending in `.dx.txt`.
- The default is `carrier.dx.txt`.
- It contains no slash, backslash, control character, `.` segment, or `..` segment.
- `version` declares the expected parsed carrier version.
- `size` is the exact carrier byte length.
- `sha256` is calculated over exact carrier bytes.

The logical name is independent of the output filename.

## 7. Payload declaration

- `media_type` is `application/zip`.
- `encoding` is `base64`.
- `size` is the exact decoded ZIP byte length.
- `sha256` is calculated over exact decoded ZIP bytes.

## 8. Canonical Base64

The representation uses:

- RFC 4648 standard alphabet;
- required padding;
- 76 characters per line except the final payload line;
- no indentation or surrounding spaces;
- no blank lines inside the payload;
- one newline before `%%ENDPAYLOAD`;
- strict decoding.

Noncanonical but decodable Base64 is rejected by canonical verification.

## 9. Canonical ZIP profile

The archive:

- contains exactly one regular-file entry;
- uses the declared logical carrier name exactly;
- contains the complete carrier bytes exactly;
- contains no directory, symlink, device, or encrypted entry;
- contains no archive or entry comment;
- uses fixed timestamp, permission, platform, compression, and extra-field rules;
- contains no trailing or concatenated archive data.

The exact canonical timestamp, permissions, compression method, compression level, platform identifier, and allowed fields must be locked by golden fixtures before `canonical-v1` is accepted as stable.

## 10. Resource safety

A decoder rejects input that exceeds configured limits for:

- envelope bytes;
- decoded ZIP bytes;
- extracted carrier bytes;
- compression ratio;
- Base64 physical-line length.

Inspection and unwrap read the permitted ZIP entry directly after validation. They do not extract the envelope archive into a directory.

## 11. Verification sequence

```text
parse envelope
→ strict Base64 decode
→ verify ZIP size and digest
→ validate canonical single-entry ZIP
→ read exact carrier bytes
→ verify carrier size and digest
→ parse and verify carrier
→ compare declared and parsed carrier version
→ verify canonical serialization when required
```

## 12. Unsupported features

Envelope v1 does not support:

- encryption;
- signatures;
- multiple carriers;
- detached payloads;
- nested envelopes;
- arbitrary transform combinations.

## 13. Filename convention

Recommended delivered envelope filenames end in:

```text
.dx.envelope.txt
```

Enclosed carriers continue to end in `.dx.txt`. Physical content, not filename alone, determines format.

## 14. Round-trip invariant

For carrier bytes `C`:

```text
unwrap(envelope(C)) == C
```

No newline normalization, text rewriting, or carrier regeneration occurs during unwrap.
