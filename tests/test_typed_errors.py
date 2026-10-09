from __future__ import annotations

import pytest

from dx_artifacts.errors import (
    DxError,
    EmptySelectionError,
    ExitCategory,
    IOErrorDx,
    InvalidCarrierError,
    UsageError,
    VerifyError,
    WriteConflictError,
)


@pytest.mark.parametrize(
    ("error_type", "exit_category", "code", "layer"),
    [
        (
            UsageError,
            ExitCategory.USAGE,
            "usage.invalid",
            "usage",
        ),
        (
            InvalidCarrierError,
            ExitCategory.INVALID_ARTIFACT,
            "carrier.invalid",
            "carrier",
        ),
        (
            IOErrorDx,
            ExitCategory.IO,
            "io.failed",
            "io",
        ),
        (
            WriteConflictError,
            ExitCategory.WRITE_CONFLICT,
            "output.conflict",
            "output",
        ),
        (
            VerifyError,
            ExitCategory.VERIFICATION,
            "verification.failed",
            "verification",
        ),
        (
            EmptySelectionError,
            ExitCategory.EMPTY_SELECTION,
            "selection.empty",
            "selection",
        ),
    ],
)
def test_operational_failures_have_stable_typed_metadata(
    error_type: type[DxError],
    exit_category: ExitCategory,
    code: str,
    layer: str,
):
    error = error_type("observed message")

    assert error.exit_code == int(exit_category)
    assert error.diagnostic_code == code
    assert error.layer == layer
    assert error.diagnostic().message == "observed message"
