"""Small supported Python API for DX Artifacts.

Only names re-exported by ``dx_artifacts`` are supported. CLI parser objects,
private modules, spool implementations, rendering helpers, and exception
wiring remain internal.
"""
from __future__ import annotations

from .capabilities import (
    Capabilities,
    current_capabilities,
    serialize_capabilities,
)
from .envelope import (
    CanonicalEnvelope,
    EnvelopeLimits,
    ParsedEnvelope,
    VerifiedEnvelope,
    build_canonical_envelope,
    parse_envelope,
    verify_canonical_envelope,
    verify_envelope,
)

__all__ = (
    "CanonicalEnvelope",
    "Capabilities",
    "EnvelopeLimits",
    "ParsedEnvelope",
    "VerifiedEnvelope",
    "build_canonical_envelope",
    "current_capabilities",
    "parse_envelope",
    "serialize_capabilities",
    "verify_canonical_envelope",
    "verify_envelope",
)
