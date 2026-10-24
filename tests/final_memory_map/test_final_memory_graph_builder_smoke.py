from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_graph


def test_final_memory_graph_builder_smoke() -> None:
    graph = build_final_memory_graph()
    node_ids = {node.node_id for node in graph.nodes}

    assert "memory_self_readability" in node_ids
    assert "memory_drift_detection" in node_ids
    assert "mempalace_read_only_adapter" in node_ids
    assert "final_memory_dashboard" in node_ids


def test_shared_inventory_owner_is_preserved_without_fallback_authority():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources import _build_memory_surface_inventory
    surfaces = _build_memory_surface_inventory()
    nodes = {node.node_id: node for node in build_final_memory_graph().nodes}
    assert any("owner" not in surface for surface in surfaces)
    for surface in surfaces:
        node = nodes[surface["surface_id"]]
        assert node.owner == surface.get("owner", "")
        assert node.storage_path == surface["path"]
        assert node.classification == surface["classification"]
        assert node.runtime_status == surface["runtime_status"]
        assert node.writer == surface.get("writer", "")
        assert node.logical_roles == tuple(surface.get("logical_roles", ()))


def test_classified_components_do_not_promote_surface_inventory_or_physical_counts():
    from pathlib import Path
    from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_builder import build_memory_component_inventory_projection
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_storage_map_builder import build_final_memory_storage_map
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources import _build_memory_surface_inventory
    graph = build_final_memory_graph()
    components = build_memory_component_inventory_projection()
    nodes = {node.node_id: node for node in graph.nodes}
    assert graph.logical_components == components
    assert len({item.component_id for item in components}) == len(components)
    for item in components:
        node = nodes[item.component_id]
        assert node.owner == item.owner
        assert node.classification == item.classification
        assert node.runtime_status == "SOURCE_CLASSIFICATION_ONLY_NOT_LIVE_ACCEPTANCE"
        assert node.storage_path == ""
    surfaces = _build_memory_surface_inventory()
    physical_paths = {surface["path"] for surface in surfaces
                      if surface["classification"] in {"CANONICAL_STORE", "CHILD_BACKEND"}
                      and Path(surface["path"]).is_absolute()
                      and Path(surface["path"]).exists()}
    assert build_final_memory_storage_map()["physical_store_count"] == len(physical_paths)
    assert graph.inventory_coverage == "REGISTERED_NATIVE_SURFACES_ONLY"
    assert graph.whole_organism_inventory_complete is False


def test_component_projection_rejects_duplicate_identity_and_unknown_classification(monkeypatch):
    import pytest
    from MAKSIMAR_SERVER.MEMORY_REGISTRY import global_registry_projection_builder as builder
    from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import MemoryComponentProjection
    original = builder._MEMORY_COMPONENT_CLASSIFICATIONS
    monkeypatch.setattr(builder, "_MEMORY_COMPONENT_CLASSIFICATIONS", (original[0], original[0]))
    with pytest.raises(ValueError, match="duplicate memory component identity"):
        builder.build_memory_component_inventory_projection()
    with pytest.raises(ValueError, match="unknown memory component classification"):
        MemoryComponentProjection("component", "owner", "LIVE_VERIFIED", "source", 1)


def test_source_classification_does_not_enroll_query_sources_or_registered_modules():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources import _build_memory_surface_inventory
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_retrieval_map_builder import build_final_memory_retrieval_map
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_module_flow_builder import build_final_memory_module_flow
    graph = build_final_memory_graph()
    component_ids = {item.component_id for item in graph.logical_components}
    registered = {item["surface_id"] for item in _build_memory_surface_inventory()}
    retrieval = build_final_memory_retrieval_map()
    flow = build_final_memory_module_flow()
    assert not component_ids.intersection(retrieval["retrieval_sources"])
    assert set(retrieval["retrieval_sources"]) == registered
    assert retrieval["retrieval_source_count"] == len(registered)
    assert flow["registered_module_count"] == len(registered)
    assert flow["logical_component_count"] == len(component_ids)
