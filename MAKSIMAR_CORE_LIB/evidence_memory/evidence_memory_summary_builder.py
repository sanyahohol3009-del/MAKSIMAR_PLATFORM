from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.evidence_memory.evidence_pack_builder import (
    build_conflict_marker_contract,
    build_evidence_memory_contract,
    build_source_event_contract,
    build_source_version_chain_contract,
)


def build_evidence_memory_summary() -> Dict[str, object]:
    evidence = build_evidence_memory_contract()
    source_events = build_source_event_contract()
    source_versions = build_source_version_chain_contract()
    conflict_markers = build_conflict_marker_contract()

    return {
        "total_records": evidence.total_records,
        "source_event_records": source_events.total_events,
        "source_version_records": source_versions.total_versions,
        "conflict_marker_records": conflict_markers.total_markers,
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
        "summary_ready": (
            evidence.ready_records == evidence.total_records
            and source_events.ready_events == source_events.total_events
            and source_versions.ready_versions == source_versions.total_versions
            and conflict_markers.ready_markers == conflict_markers.total_markers
            and evidence.conflict_detected_records == 0
        ),
    }
