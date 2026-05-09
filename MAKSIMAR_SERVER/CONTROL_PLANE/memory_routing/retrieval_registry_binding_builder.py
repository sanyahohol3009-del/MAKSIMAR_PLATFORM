from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.ai_router_binding import (
    build_ai_router_memory_skill_binding_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_preview_builder import (
    build_retrieval_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_registry_binding_models import (
    RetrievalRegistryBindingContract,
    RetrievalRegistryBindingEntry,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_global_registry_preview,
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)


def build_retrieval_registry_binding_contract() -> RetrievalRegistryBindingContract:
    retrieval_preview = build_retrieval_preview()
    selected_source_ids = {
        str(entry["source_id"]) for entry in retrieval_preview["selected_sources"]
    }

    memory_registry = build_memory_registry_contract()
    global_registry_preview = build_global_registry_preview()
    ai_router_binding = build_ai_router_memory_skill_binding_contract()
    memory_skill_metrics = build_memory_skill_metrics_contract()

    memory_registry_selected = "retrieval_source_memory_registry" in selected_source_ids
    ai_router_selected = "retrieval_source_ai_router_binding" in selected_source_ids

    entries = (
        RetrievalRegistryBindingEntry(
            binding_id="retrieval_registry_binding_memory_registry",
            component_kind="memory_registry",
            source_ref="MAKSIMAR_SERVER/MEMORY_REGISTRY",
            source_total_entries=memory_registry.total_entries,
            active_entries=memory_registry.active_entries,
            retrieval_visible_entries=memory_registry.active_entries,
            observability_visible_entries=memory_registry.active_entries,
            selected_by_retrieval=memory_registry_selected,
            binding_ready=memory_registry.total_entries >= 1 and memory_registry_selected,
        ),
        RetrievalRegistryBindingEntry(
            binding_id="retrieval_registry_binding_global_registry",
            component_kind="global_registry",
            source_ref="MAKSIMAR_SERVER/MEMORY_REGISTRY/global_registry",
            source_total_entries=int(global_registry_preview["total_entries"]),
            active_entries=int(global_registry_preview["total_entries"]),
            retrieval_visible_entries=int(global_registry_preview["retrieval_visible_entries"]),
            observability_visible_entries=int(global_registry_preview["observability_visible_entries"]),
            selected_by_retrieval=memory_registry_selected,
            binding_ready=int(global_registry_preview["total_entries"]) >= 1 and memory_registry_selected,
        ),
        RetrievalRegistryBindingEntry(
            binding_id="retrieval_registry_binding_ai_router",
            component_kind="ai_router_binding",
            source_ref="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            source_total_entries=ai_router_binding.total_entries,
            active_entries=ai_router_binding.active_entries,
            retrieval_visible_entries=ai_router_binding.active_entries,
            observability_visible_entries=ai_router_binding.explanation_ready_entries,
            selected_by_retrieval=ai_router_selected,
            binding_ready=ai_router_binding.total_entries >= 1 and ai_router_selected,
        ),
        RetrievalRegistryBindingEntry(
            binding_id="retrieval_registry_binding_memory_skill_metrics",
            component_kind="memory_skill_metrics",
            source_ref="MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics",
            source_total_entries=memory_skill_metrics.total_entries,
            active_entries=memory_skill_metrics.active_entries,
            retrieval_visible_entries=0,
            observability_visible_entries=memory_skill_metrics.total_entries,
            selected_by_retrieval=False,
            binding_ready=memory_skill_metrics.total_entries >= 1,
        ),
    )

    return RetrievalRegistryBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        selected_by_retrieval_bindings=sum(
            1 for entry in entries if entry.selected_by_retrieval
        ),
        retrieval_visible_total=sum(entry.retrieval_visible_entries for entry in entries),
        observability_visible_total=sum(
            entry.observability_visible_entries for entry in entries
        ),
        binding_ready=all(entry.binding_ready for entry in entries),
        entries=entries,
    )
