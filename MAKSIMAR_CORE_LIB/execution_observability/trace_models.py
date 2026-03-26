from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionTrace:
    """Canonical execution trace reference."""

    trace_id: str
    source_layer: str
    correlated_incident: str


@dataclass(frozen=True, slots=True)
class ExecutionTraceContract:
    """Unified execution trace contract."""

    total_traces: int
    traces: tuple[ExecutionTrace, ...]
