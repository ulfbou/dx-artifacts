# DX operation report contract

## Status

Accepted and active following WP-08.

## 1. Purpose

Operation reports provide machine-readable evidence without contaminating artifact streams or changing artifact identity.

## 2. Report sink

Artifact-producing commands may accept:

```text
--report FILE
```

The report is written only after the operation reaches its defined reporting boundary. Artifact stdout remains artifact-only.

A report path resolving to the artifact output path is rejected.

## 3. Schema

Reports use UTF-8 JSON and an integer `schema_version`.

A version 1 report contains:

```json
{
  "schema_version": 1,
  "command": "pack",
  "success": true,
  "artifact": {
    "media_type": "application/vnd.dx.carrier",
    "format_version": "v2.0.0",
    "size": 1234,
    "sha256": "<64 lowercase hexadecimal characters>"
  },
  "representations": [],
  "verification": [
    {
      "policy": "structural",
      "passed": true,
      "layer": "carrier"
    }
  ],
  "delivery": {
    "sink": "filesystem",
    "completed": true,
    "bytes_written": 1234,
    "destination": "artifact.dx.txt"
  },
  "errors": []
}
```

## 4. Artifact and representation

`artifact` describes the exact bytes delivered by the selected artifact sink. A carrier-producing operation records the carrier; envelope production records the envelope; unwrap records the recovered carrier.

`representations` is an array of exact intermediate or enclosed representations evidenced by the operation. Current envelope production records the inner carrier and canonical ZIP representation. Current unwrap reports the input envelope as a representation.

Reports do not duplicate transported file content.

## 5. Delivery semantics

`delivery.completed` is true only when the selected sink accepted complete bytes.

For a check sink, the sink is `check` and completion means complete construction and verification, not external publication.

For stdout, a broken pipe prevents successful completed delivery.

## 6. Verification evidence

The report names the applied policy and records failures by layer. A later-layer success must not be reported when an earlier layer failed.

## 7. Errors

The `errors` array contains structured error objects with stable codes and human-readable messages. Paths, when included, use workspace-relative or explicitly labeled filesystem forms. A successful version 1 report contains an empty `errors` array.

## 8. Failure reports

Whether a failure report is emitted is controlled by the command contract. A failure report must never claim a completed artifact delivery.

Report-writing failure does not silently convert an unreported operation into a fully successful reported operation. The command returns non-zero when an explicitly requested report cannot be published.

## 9. Determinism boundary

Reports may contain execution and sink information and are not canonical artifact bytes. Artifact digests remain independent of report content and report destination.
