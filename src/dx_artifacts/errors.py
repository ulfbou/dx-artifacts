"""Typed operational failures and stable process exit categories."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ExitCategory(IntEnum):
    """Stable process exit categories preserved from the accepted baseline."""

    SUCCESS = 0
    NEGATIVE_RESULT = 1
    USAGE = 2
    INVALID_ARTIFACT = 3
    IO = 4
    WRITE_CONFLICT = 5
    VERIFICATION = 6
    EMPTY_SELECTION = 7


@dataclass(frozen=True)
class Diagnostic:
    """Internal machine-oriented diagnostic representation."""

    code: str
    message: str
    layer: str


class DxError(ValueError):
    """Base class for expected operational failures."""

    exit_code = int(ExitCategory.USAGE)
    diagnostic_code = "usage.invalid"
    layer = "usage"

    def diagnostic(self) -> Diagnostic:
        return Diagnostic(
            code=self.diagnostic_code,
            message=str(self),
            layer=self.layer,
        )


class UsageError(DxError):
    exit_code = int(ExitCategory.USAGE)
    diagnostic_code = "usage.invalid"
    layer = "usage"


class InvalidCarrierError(DxError):
    exit_code = int(ExitCategory.INVALID_ARTIFACT)
    diagnostic_code = "carrier.invalid"
    layer = "carrier"


class IOErrorDx(DxError):
    exit_code = int(ExitCategory.IO)
    diagnostic_code = "io.failed"
    layer = "io"


class WriteConflictError(DxError):
    exit_code = int(ExitCategory.WRITE_CONFLICT)
    diagnostic_code = "output.conflict"
    layer = "output"


class VerifyError(DxError):
    exit_code = int(ExitCategory.VERIFICATION)
    diagnostic_code = "verification.failed"
    layer = "verification"


class EmptySelectionError(DxError):
    exit_code = int(ExitCategory.EMPTY_SELECTION)
    diagnostic_code = "selection.empty"
    layer = "selection"
