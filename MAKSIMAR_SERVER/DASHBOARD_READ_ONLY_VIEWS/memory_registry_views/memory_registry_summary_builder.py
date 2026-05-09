from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_phase_readiness,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_phase_readiness,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_phase_readiness,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_global_registry_preview,
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)


def build_memory_registry_view_summary() -> Dict[str, object]:
    memory_registry = build_memory_registry_contract()
    global_registry = build_global_registry_preview()
    retrieval = build_retrieval_phase_readiness()
    storage = build_storage_registry_phase_readiness()
    media = build_media_memory_phase_readiness()
    metrics = build_memory_skill_metrics_contract()

    return {
        "memory_registry_total_entries": memory_registry.total_entries,
        "memory_registry_active_entries": memory_registry.active_entries,
        "global_registry_total_entries": int(global_registry["total_entries"]),
        "global_registry_dashboard_visible_entries": int(
            global_registry["dashboard_visible_entries"]
        ),
        "global_registry_retrieval_visible_entries": int(
            global_registry["retrieval_visible_entries"]
        ),
        "retrieval_selected_source_count": retrieval.selected_source_count,
        "retrieval_evidence_item_count": retrieval.evidence_item_count,
        "retrieval_phase_ready": retrieval.phase_ready,
        "storage_total_entries": storage.total_entries,
        "storage_dashboard_visible_entries": storage.dashboard_visible_entries,
        "media_total_records": media.total_records,
        "media_dashboard_visible_records": media.dashboard_visible_records,
        "metrics_total_entries": metrics.total_entries,
        "metrics_active_entries": metrics.active_entries,
        "read_only": True,
        "action_exposure_allowed": False,
        "display_orchestration_allowed": False,
        "summary_ready": True,
    }
