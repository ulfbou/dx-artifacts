# Accepted-baseline characterization matrix

## Identity

- `BI-001` root `dx.py` SHA-256 equals the accepted manifest.
- `BI-002` root `dx.py` byte size equals the accepted manifest.
- `BI-003` accepted status and Dx.Domain provenance are recorded.
- `BI-004` implementation diff contains no baseline modification.

## CLI entry

- `CLI-001` `--version` succeeds and reports the baseline identity.
- `CLI-002` `--help` succeeds.
- `CLI-003` no arguments preserve current dry-run behavior.
- `CLI-004` unknown command returns usage failure.
- `CLI-005` contradictory quiet and verbose options fail.
- `CLI-006` command-specific help succeeds for pack, unpack, apply, and inspect.

## Carrier parsing

- `CP-001` valid v2.0.0 parses.
- `CP-002` supported v1.3.1 parses.
- `CP-003` through `CP-018` cover missing or duplicate headers, unsupported versions, missing end, trailing content, missing or duplicate paths, unsupported attributes, invalid booleans, invalid Base64, unterminated blocks, unsafe paths, incompatible attributes, and negative newline counts.
- `CP-019` read-only metadata is retained.
- `CP-020` NOTE blocks are counted but are not transported files.

## Serialization and pack

- `CS-001` through `CS-014` cover empty text, terminal-newline variants, Unicode, CRLF, NUL, BOM, invalid UTF-8, directive-like text, read-only attributes, deterministic ordering, repeated production, and mixed content.
- `PK-001` explicit filesystem output succeeds.
- `PK-002` conflict without force returns the baseline conflict category.
- `PK-003` force replaces output.
- `PK-004` output symlink is rejected.
- `PK-005` explicit stdout emits carrier bytes only.
- `PK-006` records the historical bootstrap behavior in which omitted output preserved numbered filesystem output; WP-10 supersedes that default with stdout.
- `PK-007` numbering advances over existing carriers.
- `PK-008` through `PK-016` cover quiet, verbose, positional-output compatibility, conflicting output options, dry run, dry-run JSON, empty selection, self-exclusion, and exact golden output.

## Selection

`SL-001` through `SL-024` cover directory and file sources, path providers, only, scope, output exclusion, protected `.git`, unsafe include gating, hard and positive filters, force inclusion, Git ignore, `.dxignore`, defaults, binary policies, empty selection, symlinks, traversal, outside-root operands, and dry-run JSON evidence.

## Inspect

`IN-001` through `IN-015` cover summary, list, hashes, read-only entries, exact cat output, missing path, valid and invalid verification, JSON, conflicting modes, isolated compare behavior, extra files, and invalid cat-plus-JSON usage.

## Unpack and apply

`UA-001` through `UA-015` cover empty destinations, command equivalence, existing-file policies, force, contradictory policy, read-only entries, symlink and traversal rejection, dry-run text and JSON, no-op behavior, and exact binary and newline recovery.

## Exit categories

- `0` successful command behavior.
- `1` defined compare difference.
- `2` invalid usage.
- `3` malformed or unsupported carrier.
- `4` input or output I/O failure.
- `5` output conflict or unsafe target.
- `6` verification failure only if reachable through the accepted public CLI.
- `7` empty selection.

An unreachable category is documented as unreachable; tests must not invent unsupported behavior.

## Non-regression gate

`NG-001` through `NG-010` protect source identity, golden bytes, supported parsing, serialization, historical bootstrap omitted-output behavior, explicit stdout, diagnostic markers, exit categories, exact round-trip, and PR scope.
