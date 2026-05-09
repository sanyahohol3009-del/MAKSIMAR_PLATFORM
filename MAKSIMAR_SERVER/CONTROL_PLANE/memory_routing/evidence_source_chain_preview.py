from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.evidence_source_chain_builder import (
    build_evidence_source_chain_contract,
)


_EVIDENCE_SOURCE_CHAIN_FLOW = (
    "retrieval_evidence_pack",
    "source_binding",
    "provenance_binding",
    "trace_binding",
    "citation_gate",
    "conflict_gate",
    "dashboard_read_only_visibility",
    "evidence_source_chain_ready",
)


def build_evidence_source_chain_preview() -> Dict[str, object]:
    contract = build_evidence_source_chain_contract()

    return {
        "flow": _EVIDENCE_SOURCE_CHAIN_FLOW,
        "total_items": contract.total_items,
        "source_bound_items": contract.source_bound_items,
        "provenance_bound_items": contract.provenance_bound_items,
        "trace_bound_items": contract.trace_bound_items,
        "citation_required_items": contract.citation_required_items,
        "conflict_marked_items": contract.conflict_marked_items,
        "dashboard_visible_items": contract.dashboard_visible_items,
        "ready_items": contract.ready_items,
        "retrieval_phase_ready": contract.retrieval_phase_ready,
        "storage_phase_ready": contract.storage_phase_ready,
        "media_phase_ready": contract.media_phase_ready,
        "architecture_control_ready": contract.architecture_control_ready,
        "mgrep_blocked": contract.mgrep_blocked,
        "sqlite_vec_blocked": contract.sqlite_vec_blocked,
        "backend_execution_allowed": contract.backend_execution_allowed,
        "chain_ids": tuple(entry.chain_id for entry in contract.entries),
        "evidence_ids": tuple(entry.evidence_id for entry in contract.entries),
        "source_ids": tuple(entry.source_id for entry in contract.entries),
        "preview_ready": True,
        "phase_batch_ready": True,
    }
