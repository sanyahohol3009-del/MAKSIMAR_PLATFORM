from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_preview_builder import (
    build_final_memory_preview,
)


def build_final_memory_acceptance() -> Dict[str, object]:
    preview = build_final_memory_preview()

    acceptance_ready = (
        preview["preview_ready"] is True
        and preview["dashboard_read_only"] is True
        and preview["canonical_write_allowed"] is False
        and preview["runtime_mutation_allowed"] is False
    )

    return {
        "acceptance_id": "phase_5_2_final_memory_map_acceptance_001",
        "acceptance_ready": acceptance_ready,
        "project_fully_visible_in_memory": acceptance_ready,
        "all_registered_modules_visible": preview["summary"]["all_registered_modules_visible"],
        "all_storage_nodes_visible": preview["summary"]["all_storage_nodes_visible"],
        "all_retrieval_sources_visible": preview["summary"]["all_retrieval_sources_visible"],
        "dashboard_read_only": preview["dashboard_read_only"],
        "canonical_write_allowed": preview["canonical_write_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
    }
