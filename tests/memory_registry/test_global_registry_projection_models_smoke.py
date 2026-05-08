from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import (
    GlobalRegistryProjectionEntry,
)


def test_global_registry_projection_models_smoke() -> None:
    entry = GlobalRegistryProjectionEntry(
        entry_kind="storage_node",
        registry_id="storage_node_project_architecture",
        module_slug="project_architecture",
        module_id="module_memory_tier_project_architecture",
        source_layer="storage_binding",
        dashboard_visible=True,
        retrieval_visible=True,
        observability_visible=True,
        flow_stages=(
            "module_manifest",
            "canonical_id_generation",
            "registry_projection",
        ),
    )

    assert entry.registry_id == "storage_node_project_architecture"
    assert entry.dashboard_visible is True
