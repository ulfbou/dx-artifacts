# DX verification and trust

## 1. Layered model

DX distinguishes verification layers:

```text
Parse
  ↓
Integrity
  ↓
Canonicality
  ↓
Policy
  ↓
Authenticity
  ↓
Application authorization
```

Success at one layer does not imply success at a later layer.

## 2. Parse verification

Parse verification proves recognized format, supported version, valid grammar, complete framing, allowed attributes, safe logical paths, unique required objects, valid encoding, and absence of forbidden trailing content.

## 3. Integrity verification

Integrity verification proves that recovered bytes match declared lengths and cryptographic digests.

Envelope v1 verifies:

```text
decoded ZIP size
SHA-256 of decoded ZIP bytes
extracted carrier size
SHA-256 of extracted carrier bytes
```

Integrity does not prove who created or approved the artifact.

## 4. Canonicality verification

Canonicality verification proves that a valid representation follows its selected profile.

Checks can include directive ordering, attribute ordering, Base64 wrapping and padding, ZIP timestamps, permissions, compression settings, entry naming, and absence of optional archive data.

A representation may be structurally valid yet noncanonical.

## 5. Policy verification

Policy verification applies environmental constraints such as:

- permitted carrier and envelope versions;
- permitted profiles;
- maximum encoded, decoded, and decompressed sizes;
- maximum compression ratio;
- allowed path prefixes;
- required read-only declarations;
- forbidden content classes;
- mandatory canonicality;
- future trusted signer identities.

Policy must be explicit and reportable.

## 6. Authenticity

Hashes establish byte identity and corruption detection, not authorship.

Future authenticity mechanisms may support detached signatures, embedded signature blocks, signed artifact identities, key identifiers, and provenance attestations. They require separate specifications.

## 7. Application authorization

A valid, canonical, and signed artifact may still be unauthorized for a destination.

Application authorization can consider destination policy, accepted paths, current workspace state, prior hashes, required signers, operation type, and read-only rules.

Authorization belongs at the application boundary.

## 8. Verification policies

Suggested policy names:

```text
structural
    Parse all supported layers.

integrity
    Parse and verify declared lengths and digests.

canonical
    Require integrity and canonical-profile compliance.

application
    Require canonical verification and destination-specific policy.
```

Authenticity may later extend these policies without redefining integrity.

## 9. Envelope verification order

```text
1. Parse envelope framing under configured limits.
2. Validate required declarations.
3. Decode Base64 strictly.
4. Verify compressed size and SHA-256.
5. Validate ZIP structure and resource bounds.
6. Read the one permitted carrier entry.
7. Verify carrier size and SHA-256.
8. Parse and verify the carrier.
9. Confirm declared and parsed carrier versions agree.
10. Verify canonical profile when required.
```

## 10. Failure classification

- Invalid syntax, framing, encoding, or unsafe archive structure is an invalid artifact.
- Digest mismatch or canonical-profile deviation is a verification failure.
- Environmental rule violation is a policy failure.
- Filesystem read or write failure is an I/O failure.
- Existing output without permitted replacement is a write conflict.

Diagnostics must identify the failed layer and must not claim later-layer success.
