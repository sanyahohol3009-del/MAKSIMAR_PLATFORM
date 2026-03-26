from __future__ import annotations

import uuid

from MAKSIMAR_CORE_LIB.execution_observability.trace_models import (
    ExecutionTrace,
    ExecutionTraceContract,
)


def _trace_id() -> str:
    """Generate trace identifier."""
    return uuid.uuid4().hex


def build_execution_trace_contract() -> ExecutionTraceContract:
    """Build unified execution trace contract."""

    traces = (
        ExecutionTrace(
            trace_id=_trace_id(),
            source_layer="execution_control",
            correlated_incident="queue_pressure_incident",
        ),
        ExecutionTrace(
            trace_id=_trace_id(),
            source_layer="execution_control",
            correlated_incident="lease_conflict_incident",
        ),
    )

    return ExecutionTraceContract(
        total_traces=len(traces),
        traces=traces,
    )
