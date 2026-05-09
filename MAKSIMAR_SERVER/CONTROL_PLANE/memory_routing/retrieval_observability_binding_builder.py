from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_observability_binding_models import (
    RetrievalObservabilityBinding,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_trace_builder import (
    build_retrieval_trace,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)


def build_retrieval_observability_binding() -> RetrievalObservabilityBinding:
    trace = build_retrieval_trace()
    metrics = build_memory_skill_metrics_contract()

    route_request_ids = tuple(
        entry.route_request_id
        for entry in metrics.entries
        if entry.route_request_id
    )

    return RetrievalObservabilityBinding(
        binding_id="retrieval_observability_binding_memory_skill_metrics",
        metrics_total_entries=metrics.total_entries,
        metrics_active_entries=metrics.active_entries,
        router_binding_entries=metrics.router_binding_entries,
        route_request_ids=route_request_ids,
        trace_binding_ready=trace.preview_trace_ready,
        observability_ready=(
            metrics.total_entries >= 1
            and metrics.router_binding_entries >= 1
            and trace.preview_trace_ready
        ),
    )
