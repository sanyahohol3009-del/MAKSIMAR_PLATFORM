from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    RetrievalRegistryBindingEntry,
)


def test_retrieval_registry_binding_models_smoke() -> None:
    entry = RetrievalRegistryBindingEntry(
        binding_id="retrieval_registry_binding_memory_registry",
        component_kind="memory_registry",
        source_ref="MAKSIMAR_SERVER/MEMORY_REGISTRY",
        source_total_entries=3,
        active_entries=3,
        retrieval_visible_entries=3,
        observability_visible_entries=3,
        selected_by_retrieval=True,
        binding_ready=True,
    )

    assert entry.binding_ready is True
    assert entry.selected_by_retrieval is True
