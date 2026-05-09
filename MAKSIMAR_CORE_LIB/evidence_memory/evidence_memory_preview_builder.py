from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.evidence_memory.evidence_memory_summary_builder import (
    build_evidence_memory_summary,
)
from MAKSIMAR_CORE_LIB.evidence_memory.evidence_pack_builder import (
    build_evidence_memory_contract,
)


_EVIDENCE_MEMORY_FLOW = (
    "source_event",
    "source_version_chain",
    "conflict_marker",
    "evidence_memory_record",
    "citation_required_gate",
    "knowledge_graph_projection_gate",
    "read_only_gate",
    "evidence_memory_ready",
)


def build_evidence_memory_preview() -> Dict[str, object]:
    evidence = build_evidence_memory_contract()
    summary = build_evidence_memory_summary()

    return {
        "flow": _EVIDENCE_MEMORY_FLOW,
        "total_records": evidence.total_records,
        "citation_required_records": evidence.citation_required_records,
        "source_bound_records": evidence.source_bound_records,
        "provenance_bound_records": evidence.provenance_bound_records,
        "trace_bound_records": evidence.trace_bound_records,
        "conflict_detected_records": evidence.conflict_detected_records,
        "memory_truth_records": evidence.memory_truth_records,
        "knowledge_graph_projection_records": (
            evidence.knowledge_graph_projection_records
        ),
        "read_only_records": evidence.read_only_records,
        "ready_records": evidence.ready_records,
        "evidence_ids": tuple(record.evidence_id for record in evidence.records),
        "source_event_ids": tuple(
            record.source_event_id for record in evidence.records
        ),
        "source_version_ids": tuple(
            record.source_version_id for record in evidence.records
        ),
        "artifact_refs": tuple(record.artifact_ref for record in evidence.records),
        "summary_ready": bool(summary["summary_ready"]),
        "preview_ready": True,
        "phase_batch_ready": bool(summary["summary_ready"]),
    }
