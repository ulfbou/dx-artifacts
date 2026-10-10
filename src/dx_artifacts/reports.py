"""Operation-report contracts and explicit JSON report publication."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ReportError(OSError):
    """An explicitly requested operation report could not be published."""


@dataclass(frozen=True)
class ArtifactIdentity:
    media_type: str
    format_version: str
    size: int
    sha256: str

    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        *,
        media_type: str,
        format_version: str,
    ) -> "ArtifactIdentity":
        return cls(
            media_type=media_type,
            format_version=format_version,
            size=len(data),
            sha256=hashlib.sha256(data).hexdigest(),
        )

    def to_json(self) -> dict[str, object]:
        return {
            "media_type": self.media_type,
            "format_version": self.format_version,
            "size": self.size,
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class VerificationEvidence:
    policy: str
    passed: bool
    layer: str

    def to_json(self) -> dict[str, object]:
        return {
            "policy": self.policy,
            "passed": self.passed,
            "layer": self.layer,
        }


@dataclass(frozen=True)
class DeliveryEvidence:
    sink: str
    completed: bool
    bytes_written: int
    destination: str | None

    def to_json(self) -> dict[str, object]:
        return {
            "sink": self.sink,
            "completed": self.completed,
            "bytes_written": self.bytes_written,
            "destination": self.destination,
        }


@dataclass(frozen=True)
class OperationReport:
    command: str
    success: bool
    artifact: ArtifactIdentity | None
    representation: tuple[ArtifactIdentity, ...]
    verification: tuple[VerificationEvidence, ...]
    delivery: DeliveryEvidence
    errors: tuple[dict[str, str], ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "command": self.command,
            "success": self.success,
            "artifact": (
                self.artifact.to_json()
                if self.artifact is not None
                else None
            ),
            "representations": [
                item.to_json()
                for item in self.representation
            ],
            "verification": [
                item.to_json()
                for item in self.verification
            ],
            "delivery": self.delivery.to_json(),
            "errors": list(self.errors),
        }


def serialize_report(report: OperationReport) -> bytes:
    return (
        json.dumps(
            report.to_json(),
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")


def publish_report(
    report: OperationReport,
    destination: Path,
) -> None:
    if destination.is_symlink():
        raise ReportError(
            f"refusing to replace report symlink: {destination}"
        )

    parent = destination.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        resolved = parent.resolve() / destination.name
    except OSError as exc:
        raise ReportError(
            f"cannot prepare report destination: {exc}"
        ) from exc

    if resolved.is_symlink():
        raise ReportError(
            f"refusing to replace report symlink: {destination}"
        )

    fd: int | None = None
    temporary: Path | None = None

    try:
        fd, temporary_name = tempfile.mkstemp(
            prefix=resolved.name + ".tmp.",
            dir=resolved.parent,
        )
        temporary = Path(temporary_name)

        with os.fdopen(fd, "wb") as stream:
            fd = None
            stream.write(serialize_report(report))
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(temporary, resolved)
        temporary = None
    except OSError as exc:
        raise ReportError(
            f"cannot publish operation report: {exc}"
        ) from exc
    finally:
        if fd is not None:
            os.close(fd)
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
