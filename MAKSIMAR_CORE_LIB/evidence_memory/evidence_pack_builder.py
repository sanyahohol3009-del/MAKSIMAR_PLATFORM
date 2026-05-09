from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory.conflict_marker_models import (
    ConflictMarkerContract,
    ConflictMarkerRecord,
)
from MAKSIMAR_CORE_LIB.evidence_memory.evidence_memory_models import (
    EvidenceMemoryContract,
    EvidenceMemoryRecord,
)
from MAKSIMAR_CORE_LIB.evidence_memory.source_event_models import (
    SourceEventContract,
    SourceEventRecord,
)
from MAKSIMAR_CORE_LIB.evidence_memory.source_version_chain_models import (
    SourceVersionChainContract,
    SourceVersionChainRecord,
)


_BASE_EVIDENCE_ROWS = (
    {
        "suffix": "history_ingestion",
        "source_id": "retrieval_source_history_ingestion",
        "source_layer": "history_ingestion",
        "artifact_ref": "artifact://retrieval/history_ingestion/preview",
        "summary": "Accepted history ingestion evidence source.",
    },
    {
        "suffix": "history_binding",
        "source_id": "retrieval_source_history_binding",
        "source_layer": "history_binding",
        "artifact_ref": "artifact://retrieval/history_binding/preview",
        "summary": "Accepted history binding evidence source.",
    },
    {
        "suffix": "storage_registry",
        "source_id": "retrieval_source_storage_registry",
        "source_layer": "storage_registry",
        "artifact_ref": "artifact://retrieval/storage_registry/preview",
        "summary": "Accepted storage registry evidence source.",
    },
    {
        "suffix": "media_memory",
        "source_id": "retrieval_source_media_memory",
        "source_layer": "media_memory",
        "artifact_ref": "artifact://retrieval/media_memory/preview",
        "summary": "Accepted media memory evidence source.",
    },
    {
        "suffix": "memory_registry",
        "source_id": "retrieval_source_memory_registry",
        "source_layer": "memory_registry",
        "artifact_ref": "artifact://retrieval/memory_registry/preview",
        "summary": "Accepted memory registry evidence source.",
    },
    {
        "suffix": "ai_router_binding",
        "source_id": "retrieval_source_ai_router_binding",
        "source_layer": "ai_router_binding",
        "artifact_ref": "artifact://retrieval/ai_router_binding/preview",
        "summary": "Accepted AI router binding evidence source.",
    },
)


def build_source_event_contract() -> SourceEventContract:
    events = tuple(
        SourceEventRecord(
            source_event_id=f"source_event_{row['suffix']}",
            source_id=str(row["source_id"]),
            source_layer=str(row["source_layer"]),
            source_event_ref=f"source_event://{row['suffix']}/v1",
            artifact_ref=str(row["artifact_ref"]),
            event_summary=str(row["summary"]),
            event_ready=True,
        )
        for row in _BASE_EVIDENCE_ROWS
    )

    return SourceEventContract(
        total_events=len(events),
        ready_events=sum(1 for event in events if event.event_ready),
        events=events,
    )


def build_source_version_chain_contract() -> SourceVersionChainContract:
    versions = tuple(
        SourceVersionChainRecord(
            source_version_id=f"source_version_{row['suffix']}",
            source_event_id=f"source_event_{row['suffix']}",
            source_version="v1",
            previous_source_version="",
            version_chain_ready=True,
        )
        for row in _BASE_EVIDENCE_ROWS
    )

    return SourceVersionChainContract(
        total_versions=len(versions),
        ready_versions=sum(
            1 for version in versions if version.version_chain_ready
        ),
        versions=versions,
    )


def build_conflict_marker_contract() -> ConflictMarkerContract:
    markers = tuple(
        ConflictMarkerRecord(
            conflict_marker_id=f"conflict_marker_{row['suffix']}",
            evidence_id=f"evidence_{row['suffix']}",
            conflict_state="none",
            conflict_marker="",
            conflict_detected=False,
            resolution_required=False,
            conflict_ready=True,
        )
        for row in _BASE_EVIDENCE_ROWS
    )

    return ConflictMarkerContract(
        total_markers=len(markers),
        conflict_detected_markers=sum(
            1 for marker in markers if marker.conflict_detected
        ),
        ready_markers=sum(1 for marker in markers if marker.conflict_ready),
        markers=markers,
    )


def build_evidence_memory_contract() -> EvidenceMemoryContract:
    source_events = build_source_event_contract()
    source_versions = build_source_version_chain_contract()
    conflict_markers = build_conflict_marker_contract()

    source_event_ids = {event.source_event_id for event in source_events.events}
    source_version_ids = {
        version.source_version_id for version in source_versions.versions
    }
    conflict_marker_ids = {
        marker.conflict_marker_id for marker in conflict_markers.markers
    }

    records = tuple(
        EvidenceMemoryRecord(
            evidence_id=f"evidence_{row['suffix']}",
            source_event_id=f"source_event_{row['suffix']}",
            source_version_id=f"source_version_{row['suffix']}",
            artifact_ref=str(row["artifact_ref"]),
            evidence_summary=str(row["summary"]),
            citation_required=True,
            source_bound=f"source_event_{row['suffix']}" in source_event_ids,
            provenance_bound=f"source_version_{row['suffix']}" in source_version_ids,
            trace_bound=True,
            conflict_marker_id=f"conflict_marker_{row['suffix']}",
            conflict_detected=(
                f"conflict_marker_{row['suffix']}" not in conflict_marker_ids
            ),
            memory_truth=True,
            knowledge_graph_projection_only=True,
            read_only=True,
            evidence_ready=True,
        )
        for row in _BASE_EVIDENCE_ROWS
    )

    return EvidenceMemoryContract(
        total_records=len(records),
        citation_required_records=sum(
            1 for record in records if record.citation_required
        ),
        source_bound_records=sum(1 for record in records if record.source_bound),
        provenance_bound_records=sum(
            1 for record in records if record.provenance_bound
        ),
        trace_bound_records=sum(1 for record in records if record.trace_bound),
        conflict_detected_records=sum(
            1 for record in records if record.conflict_detected
        ),
        memory_truth_records=sum(1 for record in records if record.memory_truth),
        knowledge_graph_projection_records=sum(
            1 for record in records if record.knowledge_graph_projection_only
        ),
        read_only_records=sum(1 for record in records if record.read_only),
        ready_records=sum(1 for record in records if record.evidence_ready),
        records=records,
    )
