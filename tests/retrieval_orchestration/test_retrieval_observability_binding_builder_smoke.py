from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_observability_binding,
)


def test_retrieval_observability_binding_builder_smoke() -> None:
    binding = build_retrieval_observability_binding()

    assert binding.observability_ready is True
    assert binding.trace_binding_ready is True
    assert binding.metrics_total_entries >= 1
    assert binding.router_binding_entries >= 1
    assert binding.route_request_ids
