from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_module_flow_builder import (
    build_final_memory_module_flow,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_retrieval_map_builder import (
    build_final_memory_retrieval_map,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_storage_map_builder import (
    build_final_memory_storage_map,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_summary_builder import (
    build_final_memory_summary,
)


def build_final_memory_preview() -> Dict[str, object]:
    storage = build_final_memory_storage_map()
    retrieval = build_final_memory_retrieval_map()
    flow = build_final_memory_module_flow()
    summary = build_final_memory_summary()

    preview_ready = (
        summary["summary_ready"] is True
        and storage["all_storage_nodes_visible"] is True
        and retrieval["all_retrieval_sources_visible"] is True
        and flow["all_registered_modules_visible"] is True
    )

    return {
        "preview_id": "final_memory_preview_001",
        "preview_ready": preview_ready,
        "summary": summary,
        "storage_nodes": storage["storage_nodes"],
        "retrieval_sources": retrieval["retrieval_sources"],
        "flow": flow["flow"],
        "dashboard_read_only": summary["dashboard_read_only"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
    }
