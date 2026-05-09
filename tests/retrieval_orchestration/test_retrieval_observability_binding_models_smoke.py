from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    RetrievalObservabilityBinding,
)


def test_retrieval_observability_binding_models_smoke() -> None:
    binding = RetrievalObservabilityBinding(
        binding_id="retrieval_observability_binding_memory_skill_metrics",
        metrics_total_entries=3,
        metrics_active_entries=3,
        router_binding_entries=1,
        route_request_ids=("route_architecture_decision_001",),
        trace_binding_ready=True,
        observability_ready=True,
    )

    assert binding.trace_binding_ready is True
    assert binding.observability_ready is True
