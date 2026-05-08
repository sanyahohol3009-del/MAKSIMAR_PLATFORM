from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.id_generation.canonical_id_generation import (
    CanonicalIdAllocationEntry,
    CanonicalIdGenerationContract,
    build_canonical_id_generation_contract,
)


_ID_GENERATION_FLOW: Tuple[str, ...] = (
    "module_manifest_schema",
    "canonical_id_generation",
    "collision_check",
    "registry_auto_enrollment",
    "dashboard_read_only_binding",
)


def _entry_to_preview(entry: CanonicalIdAllocationEntry) -> Dict[str, object]:
    """Build deterministic read-only preview for one canonical ID allocation."""
    return {
        "module_kind": entry.module_kind,
        "module_slug": entry.module_slug,
        "module_id": entry.module_id,
        "skill_id": entry.skill_id,
        "memory_tier_id": entry.memory_tier_id,
        "worker_id": entry.worker_id,
        "storage_node_id": entry.storage_node_id,
        "retrieval_source_id": entry.retrieval_source_id,
        "panel_ids": entry.panel_ids,
        "artifact_ref_prefix": entry.artifact_ref_prefix,
        "trace_id_prefix": entry.trace_id_prefix,
        "collision_free": entry.collision_free,
        "flow": _ID_GENERATION_FLOW,
    }


def build_canonical_id_flow_preview(
    contract: CanonicalIdGenerationContract | None = None,
) -> Dict[str, object]:
    """Build read-only flow preview for canonical ID generation.

    This preview does not write registry state and does not enroll modules.
    It only exposes deterministic allocation results and downstream flow.
    """
    selected_contract = contract or build_canonical_id_generation_contract()

    return {
        "flow": _ID_GENERATION_FLOW,
        "total_entries": selected_contract.total_entries,
        "total_skill_ids": selected_contract.total_skill_ids,
        "total_memory_tier_ids": selected_contract.total_memory_tier_ids,
        "total_worker_ids": selected_contract.total_worker_ids,
        "total_storage_node_ids": selected_contract.total_storage_node_ids,
        "total_retrieval_source_ids": selected_contract.total_retrieval_source_ids,
        "total_panel_ids": selected_contract.total_panel_ids,
        "entries": tuple(_entry_to_preview(entry) for entry in selected_contract.entries),
        "preview_ready": True,
    }
