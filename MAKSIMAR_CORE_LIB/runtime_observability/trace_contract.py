from __future__ import annotations

import uuid

from MAKSIMAR_CORE_LIB.runtime_observability.trace_models import (
    TraceContext,
    TraceContract,
)


def _generate_id() -> str:
    """Generate deterministic-length trace identifier."""
    return uuid.uuid4().hex


def build_trace_contract() -> TraceContract:
    """Build basic trace/correlation contract."""
    root_trace_id = _generate_id()

    root_span = TraceContext(
        trace_id=root_trace_id,
        span_id=_generate_id(),
        parent_span_id=None,
    )

    child_span_1 = TraceContext(
        trace_id=root_trace_id,
        span_id=_generate_id(),
        parent_span_id=root_span.span_id,
    )

    child_span_2 = TraceContext(
        trace_id=root_trace_id,
        span_id=_generate_id(),
        parent_span_id=root_span.span_id,
    )

    spans = (
        root_span,
        child_span_1,
        child_span_2,
    )

    return TraceContract(
        total_spans=len(spans),
        root_trace_id=root_trace_id,
        spans=spans,
    )
