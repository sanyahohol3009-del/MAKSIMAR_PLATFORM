from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_observability_binding_builder import (
    build_retrieval_observability_binding,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_preview_builder import (
    build_retrieval_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_registry_binding_builder import (
    build_retrieval_registry_binding_contract,
)


_BATCH2_FLOW = (
    "retrieval_preview",
    "memory_registry_binding",
    "global_registry_binding",
    "ai_router_binding",
    "memory_skill_metrics_binding",
    "observability_preview",
)


def build_retrieval_batch2_preview() -> Dict[str, object]:
    retrieval_preview = build_retrieval_preview()
    registry_binding = build_retrieval_registry_binding_contract()
    observability_binding = build_retrieval_observability_binding()

    return {
        "flow": _BATCH2_FLOW,
        "retrieval_preview_ready": retrieval_preview["preview_ready"],
        "retrieval_route_ready": retrieval_preview["route_ready"],
        "registry_total_bindings": registry_binding.total_bindings,
        "registry_ready_bindings": registry_binding.ready_bindings,
        "selected_by_retrieval_bindings": registry_binding.selected_by_retrieval_bindings,
        "registry_binding_ready": registry_binding.binding_ready,
        "observability_metrics_total_entries": observability_binding.metrics_total_entries,
        "observability_router_binding_entries": observability_binding.router_binding_entries,
        "observability_ready": observability_binding.observability_ready,
        "trace_binding_ready": observability_binding.trace_binding_ready,
        "batch2_ready": (
            bool(retrieval_preview["preview_ready"])
            and bool(retrieval_preview["route_ready"])
            and registry_binding.binding_ready
            and observability_binding.observability_ready
            and observability_binding.trace_binding_ready
        ),
        "preview_ready": True,
    }
