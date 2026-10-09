"""Typed structural-verification results.

This module records verification outcomes. It does not render diagnostics,
terminate a process, mutate workspace state, or redefine carrier grammar.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, TypeVar

from .errors import Diagnostic, DxError


T = TypeVar("T")


class VerificationLayer(str, Enum):
    """Layer at which a verification result was established."""

    STRUCTURAL = "structural"


@dataclass(frozen=True)
class VerificationFinding:
    """One typed finding produced during verification."""

    code: str
    message: str
    layer: VerificationLayer


@dataclass(frozen=True)
class VerificationResult(Generic[T]):
    """Typed result of one verification operation."""

    layer: VerificationLayer
    passed: bool
    value: T | None
    findings: tuple[VerificationFinding, ...]

    @classmethod
    def success(
        cls,
        value: T,
    ) -> "VerificationResult[T]":
        return cls(
            layer=VerificationLayer.STRUCTURAL,
            passed=True,
            value=value,
            findings=(),
        )

    @classmethod
    def failure(
        cls,
        finding: VerificationFinding,
    ) -> "VerificationResult[T]":
        return cls(
            layer=VerificationLayer.STRUCTURAL,
            passed=False,
            value=None,
            findings=(finding,),
        )


def verify_structural(
    operation: Callable[[], T],
) -> VerificationResult[T]:
    """Run one structural parser operation and retain typed findings."""

    try:
        return VerificationResult.success(operation())
    except DxError as exc:
        diagnostic: Diagnostic = exc.diagnostic()
        return VerificationResult.failure(
            VerificationFinding(
                code=diagnostic.code,
                message=diagnostic.message,
                layer=VerificationLayer.STRUCTURAL,
            )
        )
