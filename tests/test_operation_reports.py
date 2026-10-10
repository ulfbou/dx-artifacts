from __future__ import annotations

import hashlib
import json

import pytest

from dx_artifacts.reports import (
    ArtifactIdentity,
    DeliveryEvidence,
    OperationReport,
    ReportError,
    VerificationEvidence,
    publish_report,
    serialize_report,
)


def test_report_serialization_is_deterministic():
    artifact = ArtifactIdentity.from_bytes(
        b"artifact",
        media_type="application/example",
        format_version="v1",
    )
    report = OperationReport(
        command="example",
        success=True,
        artifact=artifact,
        representation=(),
        verification=(
            VerificationEvidence(
                policy="structural",
                passed=True,
                layer="example",
            ),
        ),
        delivery=DeliveryEvidence(
            sink="stdout",
            completed=True,
            bytes_written=8,
            destination=None,
        ),
    )

    first = serialize_report(report)
    second = serialize_report(report)

    assert first == second
    assert first.endswith(b"\n")

    payload = json.loads(first)
    assert payload["artifact"]["size"] == 8
    assert payload["artifact"]["sha256"] == (
        hashlib.sha256(b"artifact").hexdigest()
    )


def test_report_publication_is_atomic(tmp_path):
    output = tmp_path / "operation.json"
    report = OperationReport(
        command="example",
        success=True,
        artifact=None,
        representation=(),
        verification=(),
        delivery=DeliveryEvidence(
            sink="check",
            completed=True,
            bytes_written=0,
            destination=None,
        ),
    )

    publish_report(report, output)

    assert json.loads(
        output.read_text(encoding="utf-8")
    )["success"] is True
    assert list(
        tmp_path.glob(output.name + ".tmp.*")
    ) == []


def test_report_publication_rejects_symlink(tmp_path):
    target = tmp_path / "target.json"
    target.write_text("original", encoding="utf-8")
    output = tmp_path / "operation.json"

    try:
        output.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("symlinks unavailable")

    report = OperationReport(
        command="example",
        success=True,
        artifact=None,
        representation=(),
        verification=(),
        delivery=DeliveryEvidence(
            sink="check",
            completed=True,
            bytes_written=0,
            destination=None,
        ),
    )

    with pytest.raises(ReportError):
        publish_report(report, output)

    assert target.read_text(encoding="utf-8") == (
        "original"
    )
