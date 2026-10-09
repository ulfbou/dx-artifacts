# DX capabilities contract

## Status

Proposed target contract. Capability output is unavailable until its implementation and conformance gates pass.

## 1. Purpose

Automation must discover supported formats and policies without parsing help text or assuming all DX Artifacts distributions are equivalent.

## 2. Command

```text
dx capabilities --json
```

The command writes one UTF-8 JSON document to stdout and diagnostics to stderr.

## 3. Stability

The capabilities document has its own integer `schema_version`. Additive fields may be introduced within a schema version. Removing or changing field meaning requires a new schema version.

Array ordering is deterministic.

## 4. Required shape

```json
{
  "schema_version": 1,
  "tool": {
    "name": "dx-artifacts",
    "software_version": "unreleased"
  },
  "carrier": {
    "read_versions": ["v1.3.1", "v2.0.0"],
    "write_version": "v2.0.0"
  },
  "envelope": {
    "read_versions": ["v1.0.0"],
    "write_version": "v1.0.0",
    "profiles": ["canonical-v1"]
  },
  "verification_policies": [
    "structural",
    "integrity",
    "canonical"
  ],
  "digests": ["sha256"],
  "commands": [
    "pack",
    "envelope",
    "unwrap",
    "inspect",
    "verify",
    "capabilities"
  ]
}
```

Values in this example are target-state examples. `unreleased` identifies the pre-release documentation state and is not a release version. A released implementation reports its actual software release version. Carrier, envelope, profile, report-schema, and capability-schema identities remain independent. Implementations report only capabilities they actually provide.

## 5. Truthfulness requirement

A capability is advertised only when the corresponding operation is available and passes its conformance gate.

Planned, experimental, disabled, or partially implemented behavior must not appear as supported unless the schema explicitly models that status.

## 6. Carrier capability semantics

`read_versions` lists carrier versions accepted by the active parser. `write_version` identifies the only version emitted by default for newly produced carriers.

## 7. Envelope capability semantics

`read_versions` and `write_version` refer to envelope format versions, not enclosed carrier versions.

`profiles` lists registered envelope profiles accepted by the implementation. Profile order is lexical.

## 8. Verification capability semantics

A listed policy means the implementation can execute the complete policy, produce correct failure status, and report the failed layer.

## 9. Exit behavior

- Exit zero means a complete valid capabilities document was written.
- Non-zero means no successful capability report was produced.
- Human prose never precedes or follows JSON on stdout.
