# ADR-001: Envelope is a separate format

## Status

Accepted and implemented.

## Context

A carrier represents workspace files and attributes. An envelope transports complete carrier bytes. Reusing `%%DX` for both layers would conflate grammars and version domains.

## Decision

The envelope uses `%%DX-ENVELOPE`. The carrier continues to use `%%DX`. Each format has independent versioning and parsing.

## Consequences

- Physical-content detection is unambiguous.
- Existing carriers remain independently readable.
- Envelope evolution does not renumber carrier versions.
- The envelope parser delegates verified inner bytes to the carrier parser.
- Envelope filenames are distinguishable from bare `.dx.txt` carriers.

## Rejected alternative

`%%DX v1.0.0 envelope="true"` is rejected because it overloads the carrier discriminator and makes an envelope version appear to be a carrier version.

## Verification obligations

- The first physical directive selects one format parser.
- A direct carrier remains readable without envelope wrapping.
- Envelope v1 contains exactly one supported carrier.
- Nested envelopes are rejected.
