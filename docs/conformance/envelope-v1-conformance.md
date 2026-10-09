# Envelope v1 conformance plan

## 1. Purpose

This plan defines evidence required before envelope v1 and `canonical-v1` are advertised as supported.

## 2. Fixture classes

### 2.1 Carrier fixtures

The suite includes carriers containing:

- empty text file;
- UTF-8 text;
- multiple trailing newlines;
- directive-like text requiring carrier escaping;
- binary entry represented through carrier-level Base64;
- read-only entry;
- multiple deterministically ordered paths;
- non-ASCII logical file content.

### 2.2 Envelope fixtures

For every accepted carrier fixture, store:

- exact carrier bytes;
- exact canonical ZIP bytes;
- exact Base64 payload lines;
- exact envelope bytes;
- expected sizes and SHA-256 values.

## 3. Golden invariants

The suite proves:

```text
envelope(carrier) == golden envelope bytes
unwrap(golden envelope) == carrier bytes
verify(golden envelope, canonical) succeeds
```

Repeated production and stdout versus filesystem publication produce byte-identical output.

## 4. Composition invariants

```text
pack SOURCE --format envelope == pack SOURCE | envelope
```

```text
pack SOURCE | envelope | unwrap == pack SOURCE
```

The comparisons use exact bytes.

## 5. Structural negative cases

Reject:

- missing or duplicate envelope header;
- unsupported envelope version;
- missing or duplicate carrier declaration;
- missing or duplicate payload declaration;
- missing `%%ENDPAYLOAD` or `%%END`;
- unexpected directives;
- forbidden content after logical end;
- invalid or duplicate attributes;
- unsafe logical carrier name;
- nested envelope payload.

## 6. Encoding negative cases

Reject or mark noncanonical as specified:

- invalid Base64 alphabet;
- missing padding;
- spaces or indentation;
- blank payload lines;
- incorrect line width;
- CRLF where canonical LF is required;
- empty payload.

## 7. ZIP safety cases

Reject archives with:

- zero or multiple entries;
- directory entries;
- absolute or traversal names;
- slash-containing names when a basename is required;
- symlink or nonregular objects;
- encrypted entries;
- archive or entry comments;
- unexpected extra fields;
- unsupported compression;
- trailing or concatenated archive data;
- local and central directory disagreement.

## 8. Integrity cases

Reject independently corrupted:

- Base64 payload bytes;
- declared ZIP size;
- declared ZIP SHA-256;
- ZIP entry bytes;
- declared carrier size;
- declared carrier SHA-256;
- declared carrier version.

Diagnostics identify the failing layer.

## 9. Resource-boundary cases

Exercise values immediately below, at, and above configured limits for:

- envelope size;
- Base64 line length;
- decoded ZIP size;
- carrier size;
- compression ratio;
- entry count.

Limit failures occur before unbounded materialization or filesystem extraction.

## 10. Publication cases

Prove:

- stdout contains artifact bytes only;
- stderr diagnostics do not alter stdout;
- `-o FILE` uses safe replacement behavior;
- output conflicts require explicit replacement policy;
- `--force` is rejected for stdout;
- input-output identity is rejected;
- broken pipes do not produce an unhandled traceback or successful-delivery claim.

## 11. Capability gating

`capabilities --json` must not advertise envelope v1, `canonical-v1`, or canonical verification until all mandatory conformance cases pass in the supported runtime.

## 12. Release evidence

The release gate emits explicit pass or fail diagnostics for each fixture class, invariant, safety case, resource boundary, and publication contract. Any missing evidence or unresolved ambiguity fails the gate.
