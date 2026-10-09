from __future__ import annotations

from dx_artifacts.errors import InvalidCarrierError
from dx_artifacts.verification import (
    VerificationLayer,
    verify_structural,
)


def test_structural_verification_returns_typed_success():
    result = verify_structural(lambda: ("v2.0.0", 3))

    assert result.passed is True
    assert result.layer is VerificationLayer.STRUCTURAL
    assert result.value == ("v2.0.0", 3)
    assert result.findings == ()


def test_structural_verification_returns_typed_failure():
    def fail():
        raise InvalidCarrierError("missing %%END")

    result = verify_structural(fail)

    assert result.passed is False
    assert result.value is None
    assert len(result.findings) == 1
    assert result.findings[0].code == "carrier.invalid"
    assert result.findings[0].message == "missing %%END"
    assert result.findings[0].layer is VerificationLayer.STRUCTURAL
