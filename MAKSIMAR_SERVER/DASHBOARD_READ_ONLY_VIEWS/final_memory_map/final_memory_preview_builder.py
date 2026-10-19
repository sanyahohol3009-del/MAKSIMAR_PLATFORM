from __future__ import annotations

from typing import Dict
from dataclasses import asdict

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
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_graph_builder import build_final_memory_graph
    federation = build_jarvis_live_memory_federation_status()
    graph = build_final_memory_graph()
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import _read_recent_local_chat_records, _session_turn_log_path
    latest_trace = next((record["artifact"]["retrieval_trace"] for record in reversed(_read_recent_local_chat_records(limit=64))
                         if isinstance(record.get("artifact"), dict) and isinstance(record["artifact"].get("retrieval_trace"), dict)), None)

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
        "payload_version": "final_memory_map.live.v1",
        "overview": federation,
        "graph": asdict(graph),
        "layers": federation["surfaces"],
        "storage": tuple(surface for surface in federation["surfaces"] if surface["classification"] in {"CANONICAL_STORE", "CHILD_BACKEND"}),
        "backends": tuple(surface for surface in federation["surfaces"] if surface["classification"] in {"CHILD_BACKEND", "LEGACY"}),
        "mempalace": next(surface["health"] for surface in federation["surfaces"] if surface["surface_id"] == "mempalace_search"),
        "experience": {"owner": "CanonicalSessionContextStore", "store_surface": "local_chat_memory", "projection": "canonical_experience_projection", "separate_store": False},
        "evidence": {"owner": "EvidenceBundle/ExecutionReceipt", "journal": str(_session_turn_log_path()), "store_owner": "CanonicalSessionContextStore", "store_surface": "local_chat_memory", "authority": "original execution receipts"},
        "health": {"mempalace_status": federation["mempalace_status"], "disabled_surfaces": federation["disabled_memory_surfaces"],
                   "canonical_session": federation["canonical_session_health"], "read_only": True},
        "latest_retrieval_trace": {"available": latest_trace is not None, "trace": latest_trace,
                                   "owner": "CanonicalSessionContextStore", "selection": "latest persisted retrieval in bounded 64-turn window"},
        "dashboard_read_only": summary["dashboard_read_only"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
    }
