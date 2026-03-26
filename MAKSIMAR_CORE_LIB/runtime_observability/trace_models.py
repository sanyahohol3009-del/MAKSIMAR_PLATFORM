from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TraceContext:
    """Correlation context for one execution path."""

    trace_id: str
    span_id: str
    parent_span_id: str | None


@dataclass(frozen=True, slots=True)
class TraceContract:
    """Unified trace contract for observability."""

    total_spans: int
    root_trace_id: str
    spans: tuple[TraceContext, ...]
