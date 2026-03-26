from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CanonicalTraceIdentity:
    """Canonical trace identity entry."""

    trace_prefix: str
    identity_pattern: str
    source_layer: str


@dataclass(frozen=True, slots=True)
class CanonicalTraceIdentityContract:
    """Unified canonical trace identity contract."""

    total_trace_patterns: int
    traces: tuple[CanonicalTraceIdentity, ...]
