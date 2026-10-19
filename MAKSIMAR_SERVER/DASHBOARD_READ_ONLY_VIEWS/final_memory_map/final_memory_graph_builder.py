from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_map_models import (
    FinalMemoryMap,
    FinalMemoryMapEdge,
    FinalMemoryMapNode,
)


def build_final_memory_graph() -> FinalMemoryMap:
    nodes = (
        FinalMemoryMapNode(
            node_id="memory_self_readability",
            label="JARVIS Memory Self-Readability",
            node_kind="memory_layer",
            source_path="MAKSIMAR_CORE_LIB/memory_engine/self_readability",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
        FinalMemoryMapNode(
            node_id="memory_drift_detection",
            label="Memory Drift / Contradiction Candidates",
            node_kind="memory_layer",
            source_path="MAKSIMAR_CORE_LIB/memory_engine/drift_detection",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
        FinalMemoryMapNode(
            node_id="mempalace_read_only_adapter",
            label="MemPalace Read-only Subordinate Backend",
            node_kind="backend_adapter",
            source_path="MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
        FinalMemoryMapNode(
            node_id="memory_sync",
            label="Shell / Client / Multi-node Memory Sync",
            node_kind="governance_layer",
            source_path="MAKSIMAR_SERVER/MEMORY_SYNC",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
        FinalMemoryMapNode(
            node_id="project_artifact_memory",
            label="Project Artifact Memory",
            node_kind="evidence_layer",
            source_path="MAKSIMAR_CORE_LIB/project_artifact_memory",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
        FinalMemoryMapNode(
            node_id="enterprise_regulatory_memory",
            label="Enterprise Regulatory Memory",
            node_kind="governance_layer",
            source_path="MAKSIMAR_CORE_LIB/enterprise_memory_domains",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
        FinalMemoryMapNode(
            node_id="final_memory_dashboard",
            label="Final Dashboard Memory Map",
            node_kind="dashboard_view",
            source_path="MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/final_memory_map",
            read_only=True,
            dashboard_visible=True,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            node_ready=True,
        ),
    )

    edges = (
        FinalMemoryMapEdge(
            edge_id="edge_self_read_to_dashboard",
            from_node_id="memory_self_readability",
            to_node_id="final_memory_dashboard",
            relation="explains_source_usage",
            read_only_relation=True,
            edge_ready=True,
        ),
        FinalMemoryMapEdge(
            edge_id="edge_drift_to_dashboard",
            from_node_id="memory_drift_detection",
            to_node_id="final_memory_dashboard",
            relation="exposes_contradiction_candidates",
            read_only_relation=True,
            edge_ready=True,
        ),
        FinalMemoryMapEdge(
            edge_id="edge_mempalace_to_dashboard",
            from_node_id="mempalace_read_only_adapter",
            to_node_id="final_memory_dashboard",
            relation="exposes_subordinate_backend_status",
            read_only_relation=True,
            edge_ready=True,
        ),
        FinalMemoryMapEdge(
            edge_id="edge_sync_to_dashboard",
            from_node_id="memory_sync",
            to_node_id="final_memory_dashboard",
            relation="exposes_node_memory_consistency",
            read_only_relation=True,
            edge_ready=True,
        ),
        FinalMemoryMapEdge(
            edge_id="edge_artifact_to_dashboard",
            from_node_id="project_artifact_memory",
            to_node_id="final_memory_dashboard",
            relation="exposes_artifact_memory_visibility",
            read_only_relation=True,
            edge_ready=True,
        ),
        FinalMemoryMapEdge(
            edge_id="edge_regulatory_to_dashboard",
            from_node_id="enterprise_regulatory_memory",
            to_node_id="final_memory_dashboard",
            relation="exposes_regulatory_memory_visibility",
            read_only_relation=True,
            edge_ready=True,
        ),
    )

    # One inventory supplies both JARVIS self-readability and this existing map.
    # node_ready validates a graph definition; runtime_status reports live truth.
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources import _build_memory_surface_inventory
    surfaces = _build_memory_surface_inventory()
    nodes += tuple(FinalMemoryMapNode(
        node_id=surface["surface_id"], label=surface["type"],
        node_kind="backend_adapter" if surface["classification"] == "CHILD_BACKEND" else "memory_layer",
        source_path=surface["path"], read_only=True, dashboard_visible=True,
        canonical_write_allowed=False, runtime_mutation_allowed=False, node_ready=True,
        classification=surface["classification"], runtime_status=surface["runtime_status"],
        owner=surface.get("owner", ""), storage_path=surface["path"],
        persistence=surface.get("persistence", "read-model projection"),
        writer=surface.get("writer", ""), write_scope=surface.get("write_scope", ""),
        canonical_store_surface=surface.get("canonical_store_surface", ""),
        logical_roles=tuple(surface.get("logical_roles", ())),
    ) for surface in surfaces)
    edges += tuple(FinalMemoryMapEdge(
        edge_id="surface_" + surface["surface_id"] + "_to_dashboard",
        from_node_id=surface["surface_id"], to_node_id="final_memory_dashboard",
        relation="shared_existing_memory_surface_readback", read_only_relation=True, edge_ready=True,
    ) for surface in surfaces)
    edges += (FinalMemoryMapEdge(
        edge_id="history_reads_canonical_session_store", from_node_id="runtime_history_store",
        to_node_id="local_chat_memory", relation="reads_same_canonical_append_only_store",
        read_only_relation=True, edge_ready=True,
    ),)
    from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_builder import build_memory_component_inventory_projection
    components = build_memory_component_inventory_projection()
    # Source classification nodes do not masquerade as additional stores or
    # enrolled retrieval surfaces. No decorative runtime edges are fabricated.
    nodes += tuple(FinalMemoryMapNode(
        node_id=component.component_id,
        label=component.owner + " [" + component.classification + "]",
        node_kind="governance_layer", source_path=component.source_path,
        read_only=True, dashboard_visible=True, canonical_write_allowed=False,
        runtime_mutation_allowed=False, node_ready=True,
        classification=component.classification,
        runtime_status="SOURCE_CLASSIFICATION_ONLY_NOT_LIVE_ACCEPTANCE",
        owner=component.owner,
        persistence="Source classification metadata; physical backing remains in observed registered surfaces",
    ) for component in components)
    return FinalMemoryMap(
        map_id="final_dashboard_memory_map_001",
        logical_components=components,
        registered_surface_ids=tuple(surface["surface_id"] for surface in surfaces),
        nodes=nodes,
        edges=edges,
        all_registered_modules_visible=True,
        all_storage_nodes_visible=True,
        all_retrieval_sources_visible=True,
        dashboard_read_only=True,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        map_ready=True,
    )
