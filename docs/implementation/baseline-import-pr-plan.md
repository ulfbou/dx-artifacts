# Baseline-import PR plan

## Identity

```text
branch  feat/import-accepted-dx-baseline
commit  feat: import and characterize the accepted DX baseline
PR      feat: import and characterize the accepted DX baseline
```

## Purpose

Convert the accepted root `dx.py` into native repository evidence: recorded provenance, exact byte identity, executable characterization, controlling fixtures, and a repeatable baseline gate.

## Scope

1. Preserve root `dx.py` byte-for-byte.
2. Add `tests/baseline/accepted-baseline.json` and identity verification.
3. Add pytest subprocess helpers and characterization suites.
4. Add byte-exact source and carrier fixtures with a generated manifest.
5. Characterize CLI entry, parsing, serialization, selection, pack, inspect, unpack/apply, diagnostics, and reachable exit categories.
6. Update controlling documentation from candidate/pending language to accepted-baseline language.
7. Retain Collab as later compatibility evidence.

## Exclusions

- no edits to `dx.py`;
- no `dx_artifacts` package extraction;
- no envelope reader or writer;
- no stdout-default activation;
- no diagnostic or exit-code redesign;
- no Collab-specific behavior in the generic core;
- no claim that internal functions are supported Python API.

## Commits

1. `feat: import and characterize the accepted DX baseline`
2. `docs: record acceptance of the DX bootstrap baseline`

## Concise PR checklist

- [ ] Root `dx.py` matches the accepted manifest.
- [ ] Golden carrier bytes and fixture manifest pass.
- [ ] Characterization tests pass on the supported development runtime.
- [ ] Current numbered-output behavior remains unchanged.
- [ ] Explicit `-o -`, parsing, inspection, unpack/apply, diagnostics, and reachable exit categories are covered.
- [ ] Baseline documentation says accepted, not pending candidate.
- [ ] Collab is compatibility evidence, not baseline approval.
- [ ] No package extraction, envelope behavior, or stdout-default activation is present.
- [ ] Repository validation and pytest gates return zero.
