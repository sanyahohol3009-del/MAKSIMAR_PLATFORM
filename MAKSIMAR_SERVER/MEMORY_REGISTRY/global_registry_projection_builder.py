from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import build_canonical_id_generation_contract
from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import (
    GlobalRegistryProjectionContract,
    GlobalRegistryProjectionEntry,
    MemoryComponentProjection,
)


_GLOBAL_REGISTRY_FLOW = (
    "module_manifest",
    "canonical_id_generation",
    "registry_projection",
    "dashboard_read_only_visibility",
)


def _append_entry(
    entries: list[GlobalRegistryProjectionEntry],
    *,
    entry_kind: str,
    registry_id: str,
    module_slug: str,
    module_id: str,
    source_layer: str,
    dashboard_visible: bool,
    retrieval_visible: bool,
    observability_visible: bool,
) -> None:
    entries.append(
        GlobalRegistryProjectionEntry(
            entry_kind=entry_kind,  # type: ignore[arg-type]
            registry_id=registry_id,
            module_slug=module_slug,
            module_id=module_id,
            source_layer=source_layer,
            dashboard_visible=dashboard_visible,
            retrieval_visible=retrieval_visible,
            observability_visible=observability_visible,
            flow_stages=_GLOBAL_REGISTRY_FLOW,
        )
    )


def build_global_registry_projection_contract() -> GlobalRegistryProjectionContract:
    """Build read-only global registry projection from canonical ID allocations."""

    id_contract = build_canonical_id_generation_contract()
    entries: list[GlobalRegistryProjectionEntry] = []

    for allocation in id_contract.entries:
        _append_entry(
            entries,
            entry_kind="module",
            registry_id=allocation.module_id,
            module_slug=allocation.module_slug,
            module_id=allocation.module_id,
            source_layer="id_generation",
            dashboard_visible=bool(allocation.panel_ids),
            retrieval_visible=bool(allocation.retrieval_source_id),
            observability_visible=True,
        )

        if allocation.skill_id:
            _append_entry(
                entries,
                entry_kind="skill",
                registry_id=allocation.skill_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="skill_adapter_registry",
                dashboard_visible=bool(allocation.panel_ids),
                retrieval_visible=bool(allocation.retrieval_source_id),
                observability_visible=True,
            )

        if allocation.memory_tier_id:
            _append_entry(
                entries,
                entry_kind="memory_tier",
                registry_id=allocation.memory_tier_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="memory_registry",
                dashboard_visible=bool(allocation.panel_ids),
                retrieval_visible=bool(allocation.retrieval_source_id),
                observability_visible=True,
            )

        if allocation.worker_id:
            _append_entry(
                entries,
                entry_kind="worker",
                registry_id=allocation.worker_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="skill_adapter_registry",
                dashboard_visible=False,
                retrieval_visible=False,
                observability_visible=True,
            )

        if allocation.storage_node_id:
            _append_entry(
                entries,
                entry_kind="storage_node",
                registry_id=allocation.storage_node_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="storage_binding",
                dashboard_visible=True,
                retrieval_visible=bool(allocation.retrieval_source_id),
                observability_visible=True,
            )

        if allocation.retrieval_source_id:
            _append_entry(
                entries,
                entry_kind="retrieval_source",
                registry_id=allocation.retrieval_source_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="retrieval_binding",
                dashboard_visible=True,
                retrieval_visible=True,
                observability_visible=True,
            )

        for panel_id in allocation.panel_ids:
            _append_entry(
                entries,
                entry_kind="dashboard_view",
                registry_id=panel_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="dashboard_binding",
                dashboard_visible=True,
                retrieval_visible=False,
                observability_visible=True,
            )

    return GlobalRegistryProjectionContract(
        total_entries=len(entries),
        dashboard_visible_entries=sum(1 for entry in entries if entry.dashboard_visible),
        retrieval_visible_entries=sum(1 for entry in entries if entry.retrieval_visible),
        observability_visible_entries=sum(
            1 for entry in entries if entry.observability_visible
        ),
        entries=tuple(entries),
    )


# Current local source classifications reconciled 2026-10-16.
# Metadata only: never capability enrollment, runtime readiness or write authority.
# Original discovery/source proofs remain retained in the audit, not read at runtime.
_MEMORY_COMPONENT_CLASSIFICATIONS = (
    ('existing_dbcd3beec3b1c0c2', 'build_archive_manifest_write_payload / build_normalized_history_write_payload', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/archive_manifest_writer.py', 8),
    ('existing_d450eef468780c18', 'build_attachment_linkage_result / build_message_attachment_linkage_result', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/attachment_linkage_builder.py', 6),
    ('existing_b51bc5b738999b87', 'resolve_incremental_import', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/fingerprint_models.py', 15),
    ('existing_718c4175ee781eaa', 'read_unified_extraction / build_extracted_document_from_source', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/adapter_base.py', 15),
    ('existing_be3d8ec43ab5ae68', 'build_jarvis_history_context / build_minimal_memory_object', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/jarvis_history_context_reader.py', 10),
    ('existing_728ce5c9cbc5bbb5', 'read_archive_source_from_path', 'FEDERATED_SOURCE', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/history_boundary_models.py', 10),
    ('existing_863bebdb2666f749', 'segment_chat_document / build_memory_relations / build_history_completion_state', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/__init__.py', 36),
    ('existing_daf6a4033c56978f', 'build_incremental_live_import_result / build_import_session_write_payload', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/incremental_live_import_builder.py', 6),
    ('existing_953ff472d589a252', 'build_history_track_canonical_mapping / build_history_store_acceptance_result', 'LEGACY', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/canonical_mapping.py', 8),
    ('existing_22cf4ec97cb39420', 'run_jarvis_history_query / JarvisHistoryQuery', 'CANONICAL_OWNER', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/jarvis_history_query_reader.py', 2),
    ('existing_fbd2dd023eea754a', 'execute_live_import_write', 'CHILD_BACKEND', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/live_import_session_builder.py', 9),
    ('existing_3fc199cda934e8b5', 'build_portable_storage_reference / build_relocated_absolute_path', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_ingestion/storage_layout_builders.py', 9),
    ('existing_c6134fe6ea805223', 'Existing artifact routing metadata/preview family', 'READ_MODEL', 'MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/__init__.py', 11),
    ('existing_e410b60b9f92d1bb', 'Existing historical Mempalace integration/report contracts', 'READ_MODEL', 'MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters/__init__.py', 18),
    ('existing_5083c5238febe27b', 'Existing media artifact metadata contracts', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/media_memory/__init__.py', 14),
    ('existing_67b33137a8862769', 'Existing core artifact-reference and payload-envelope contract family', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/payload_builders.py', 8),
    ('existing_7dde78255d15af41', 'Existing retrieval metadata projection contracts', 'READ_MODEL', 'MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/__init__.py', 24),
    ('existing_f3bbd718f5fd9da7', 'Existing retrieval provider contracts and availability read model', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/retrieval_backend/__init__.py', 18),
    ('existing_0bd781d74f0bc552', 'Existing storage reference registry contracts', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/storage_registry/__init__.py', 14),
    ('existing_bff397c40a552b56', 'Existing core data-plane reference/registry/model family', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/data_plane/__init__.py', 38),
    ('existing_4738a7ea4e8f281d', 'MAKSIMAR_CORE_LIB.memory_engine.history_binding', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/history_binding/__init__.py', 7),
    ('existing_25fe63a128b20e08', 'MAKSIMAR_CORE_LIB.memory_engine.self_readability', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/self_readability/__init__.py', 7),
    ('existing_e051d18421667a69', 'MAKSIMAR_CORE_LIB.memory_engine.foundation_inspector', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/foundation_inspector/__init__.py', 5),
    ('existing_b95d4b632c68636e', 'MAKSIMAR_CORE_LIB.memory_engine.drift_detection', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/drift_detection/__init__.py', 7),
    ('existing_9e709a8ce1840f29', 'MAKSIMAR_CORE_LIB.memory_policy', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_policy/__init__.py', 10),
    ('existing_670a563def08b635', 'MAKSIMAR_CORE_LIB.evidence_memory', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/evidence_memory/__init__.py', 8),
    ('existing_e5f3dffe0f035803', 'MAKSIMAR_CORE_LIB.project_artifact_memory', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/project_artifact_memory/__init__.py', 8),
    ('existing_b600aef722b098b0', 'MAKSIMAR_SERVER.MEMORY_ACCEPTANCE', 'READ_MODEL', 'MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/__init__.py', 8),
    ('existing_18dc2178422783a5', 'MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION', 'READ_MODEL', 'MAKSIMAR_SERVER/MEMORY_CONFLICT_RESOLUTION/__init__.py', 5),
    ('existing_f7bd7488a347cf8d', 'MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE', 'READ_MODEL', 'MAKSIMAR_SERVER/MEMORY_PROMOTION_PIPELINE/__init__.py', 6),
    ('existing_d84a939e2b01b211', 'MAKSIMAR_SERVER.MEMORY_SYNC', 'READ_MODEL', 'MAKSIMAR_SERVER/MEMORY_SYNC/__init__.py', 30),
    ('existing_fb65917aabaedaee', 'MAKSIMAR_SERVER.MEMORY_REGISTRY', 'READ_MODEL', 'MAKSIMAR_SERVER/MEMORY_REGISTRY/__init__.py', 6),
    ('existing_3caa93dc12eece09', 'MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views', 'READ_MODEL', 'MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/memory_registry_views/__init__.py', 6),
    ('existing_86c2e94bb81f103e', 'MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map', 'READ_MODEL', 'MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS/final_memory_map/__init__.py', 9),
    ('existing_44b8a9c2b677f3b7', 'MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation', 'READ_MODEL', 'MAKSIMAR_SERVER/DISPLAY_ORCHESTRATION/memory_presentation/__init__.py', 9),
    ('existing_6b8a114b3c11a973', 'MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics', 'READ_MODEL', 'MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/__init__.py', 26),
    ('existing_845561baae44ea2e', 'ANDROID_SHELL.memory_adapter', 'READ_MODEL', 'ANDROID_SHELL/memory_adapter/android_app_memory_store.py', 9),
    ('existing_fc2a71aa0a28360e', 'IOS_SHELL.memory_adapter', 'READ_MODEL', 'IOS_SHELL/memory_adapter/ios_app_memory_store.py', 9),
    ('existing_699ed17b31dc9341', 'shared_mobile_core.app_memory', 'READ_MODEL', 'shared_mobile_core/app_memory/__init__.py', 5),
    ('existing_b4c69b16d760f9f3', 'shared_mobile_core.chat_memory', 'READ_MODEL', 'shared_mobile_core/chat_memory/__init__.py', 5),
    ('existing_2203befe5e33452c', 'shared_mobile_core.p2p_mesh_network', 'READ_MODEL', 'shared_mobile_core/p2p_mesh_network/__init__.py', 9),
    ('existing_0b08c59dfab02965', 'MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME', 'READ_MODEL', 'MAKSIMAR_SERVER/MOBILE_SYNC_RUNTIME/__init__.py', 8),
    ('existing_51899d2ed3da2b57', 'MAKSIMAR_CORE.contracts.memory', 'READ_MODEL', 'MAKSIMAR_CORE/contracts/memory/__init__.py', 1),
    ('existing_fe9aaa644edaeef8', 'MAKSIMAR_CORE.contracts.knowledge', 'READ_MODEL', 'MAKSIMAR_CORE/contracts/knowledge/__init__.py', 1),
    ('existing_2e082a3b6ed492b7', 'Existing canonical ingress / turn capture', 'CANONICAL_OWNER', 'CONTROL_PLANE/api_server.py', 2),
    ('existing_4c9ad6ded804174a', 'CanonicalSessionContextStore', 'CANONICAL_OWNER', 'MAKSIMAR_SERVER/AI_ORCHESTRATION/session_memory_store.py', 1),
    ('existing_f449215fcec7d80a', 'Existing native event journal writer', 'CANONICAL_OWNER', 'MAKSIMAR_CORE_LIB/event_bus/__init__.py', 7),
    ('existing_382b413d9c15c227', 'Existing native incident journal writer', 'CANONICAL_OWNER', 'CORE_ROOT/incident_history.py', 1),
    ('existing_ab10c8b6a1cd5a35', 'ExistingMemoryRetrievalAdapter', 'CANONICAL_OWNER', 'MAKSIMAR_SERVER/AI_ORCHESTRATION/memory_retrieval_adapter.py', 1),
    ('existing_abf23319aa27d62f', 'Existing FinalBrain publication owner', 'CANONICAL_OWNER', 'MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py', 8),
    ('existing_c493e69c9156502a', 'Existing DeveloperExperience / LearningBundle qualification', 'CANONICAL_OWNER', 'MAKSIMAR_SERVER/CLIENT_LEARNING_INPUT/__init__.py', 7),
    ('existing_c70eaa81c4e8b14a', 'Existing shared memory context / live federation projection', 'READ_MODEL', 'MAKSIMAR_SERVER/AI_ORCHESTRATION/memory_context_sources.py', 3),
    ('existing_ea3b28c09ff61bdf', 'CanonicalSessionContextStore', 'CANONICAL_STORE', '/home/aleksandr/MAKSIMAR_RUNTIME/jarvis_live/session_memory/jarvis_live_terminal_turns.jsonl', 0),
    ('existing_fa01cf35980a8337', 'ExistingMemoryRetrievalAdapter', 'CHILD_BACKEND', '/home/aleksandr/.mempalace/chroma.sqlite3', 0),
    ('existing_f29b323e1f7bfe1f', 'MAKSIMAR_CORE_LIB.event_bus.event_writer.append_event_record', 'CANONICAL_STORE', '/home/aleksandr/MAKSIMAR_PLATFORM/EVENT_BUS/event_journal.jsonl', 0),
    ('existing_a782384f9c99884b', 'CORE_ROOT.incident_history.write_incident_record', 'CANONICAL_STORE', '/home/aleksandr/MAKSIMAR_PLATFORM/RUNTIME/state/incident_history.jsonl', 0),
    ('existing_90fdb69cd6bbe5d0', 'MAKSIMAR_CORE_LIB.enterprise_memory_domains', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/enterprise_memory_domains/__init__.py', 10),
    ('existing_2bb37af586c014ec', 'MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION', 'READ_MODEL', 'MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION/__init__.py', 35),
    ('existing_0dd218a0a914f48f', 'MAKSIMAR_CORE_LIB.memory_engine', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/memory_engine/__init__.py', 7),
    ('existing_45746a6f0de44602', 'MAKSIMAR_CORE_LIB.knowledge_engine', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/knowledge_engine/__init__.py', 7),
    ('existing_oob_foundation_presentation', 'foundation_truth_consistency_contract.build_foundation_truth_consistency_contract', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/oob_dashboard/display_assignment_registry_contract.py', 212),
    ('existing_model_provenance_read_model', 'build_model_provenance_service_read_model / ModelProvenanceContract', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/ai_orchestration/model_provenance_contract.py', 2),
    ('existing_mobile_memory_status_presentation', 'MobileMemoryStatusReadModel / build_mobile_memory_status_preview_payload', 'READ_MODEL', 'MAKSIMAR_CORE_LIB/mobile_bridge/mobile_memory_status_read_model.py', 2),
    ('existing_architecture_memory_dependency_presentation', 'build_memory_dependency_summary', 'READ_MODEL', 'MAKSIMAR_SERVER/architecture_map_runtime/domain_cube_memory_locator.py', 5),
    ('existing_frontend_memory_knowledge_preview', 'Existing frontend memoryKnowledgeShellReadModel and exposure registry metadata', 'READ_MODEL', 'frontend/react_flow_preview/src/memoryKnowledgeExposureRegistry.ts', 3),
    ('existing_dcce9c291225fcab', 'build_ai_router_memory_skill_binding_contract', 'READ_MODEL', 'MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding/__init__.py', 3),
    ('existing_d8c9e67634058398', 'operator_shell_read_model.event_projection / foundation_projection', 'READ_MODEL', 'MAKSIMAR_SERVER/OBSERVABILITY/operator_shell_read_model.py', 1),
)


def build_memory_component_inventory_projection() -> tuple[MemoryComponentProjection, ...]:
    """Project classified source owners without altering enrolled tier IDs."""
    entries = tuple(MemoryComponentProjection(*row) for row in _MEMORY_COMPONENT_CLASSIFICATIONS)
    identities = tuple(entry.component_id for entry in entries)
    if len(set(identities)) != len(identities):
        raise ValueError("duplicate memory component identity")
    return entries
