from __future__ import annotations

import re
from dataclasses import dataclass


_EVIDENCE_ID_PATTERN = re.compile(r"^evidence_[a-z][a-z0-9_]*$")
_SOURCE_EVENT_ID_PATTERN = re.compile(r"^source_event_[a-z][a-z0-9_]*$")
_SOURCE_VERSION_ID_PATTERN = re.compile(r"^source_version_[a-z][a-z0-9_]*$")
_CONFLICT_MARKER_ID_PATTERN = re.compile(r"^conflict_marker_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class EvidenceMemoryRecord:
    evidence_id: str
    source_event_id: str
    source_version_id: str
    artifact_ref: str
    evidence_summary: str
    citation_required: bool
    source_bound: bool
    provenance_bound: bool
    trace_bound: bool
    conflict_marker_id: str
    conflict_detected: bool
    memory_truth: bool
    knowledge_graph_projection_only: bool
    read_only: bool
    evidence_ready: bool

    def __post_init__(self) -> None:
        evidence_id = _ensure_non_empty_str(self.evidence_id, "evidence_id")
        source_event_id = _ensure_non_empty_str(
            self.source_event_id,
            "source_event_id",
        )
        source_version_id = _ensure_non_empty_str(
            self.source_version_id,
            "source_version_id",
        )
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")
        evidence_summary = _ensure_non_empty_str(
            self.evidence_summary,
            "evidence_summary",
        )
        conflict_marker_id = _ensure_non_empty_str(
            self.conflict_marker_id,
            "conflict_marker_id",
        )

        if not _EVIDENCE_ID_PATTERN.fullmatch(evidence_id):
            raise ValueError(f"Invalid evidence_id: {evidence_id}")
        if not _SOURCE_EVENT_ID_PATTERN.fullmatch(source_event_id):
            raise ValueError(f"Invalid source_event_id: {source_event_id}")
        if not _SOURCE_VERSION_ID_PATTERN.fullmatch(source_version_id):
            raise ValueError(f"Invalid source_version_id: {source_version_id}")
        if not _CONFLICT_MARKER_ID_PATTERN.fullmatch(conflict_marker_id):
            raise ValueError(f"Invalid conflict_marker_id: {conflict_marker_id}")
        if not artifact_ref.startswith("artifact://"):
            raise ValueError("artifact_ref must start with artifact://")

        for field_name in (
            "citation_required",
            "source_bound",
            "provenance_bound",
            "trace_bound",
            "conflict_detected",
            "memory_truth",
            "knowledge_graph_projection_only",
            "read_only",
            "evidence_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.citation_required:
            raise ValueError("citation_required must be True")
        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.provenance_bound:
            raise ValueError("provenance_bound must be True")
        if not self.trace_bound:
            raise ValueError("trace_bound must be True")
        if self.conflict_detected:
            raise ValueError("conflict_detected must be False in Batch 3")
        if not self.memory_truth:
            raise ValueError("evidence memory must be memory_truth")
        if not self.knowledge_graph_projection_only:
            raise ValueError("knowledge graph must remain projection-only")
        if not self.read_only:
            raise ValueError("evidence memory canonical layer must be read-only")
        if not self.evidence_ready:
            raise ValueError("evidence_ready must be True")

        object.__setattr__(self, "evidence_id", evidence_id)
        object.__setattr__(self, "source_event_id", source_event_id)
        object.__setattr__(self, "source_version_id", source_version_id)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "evidence_summary", evidence_summary)
        object.__setattr__(self, "conflict_marker_id", conflict_marker_id)


@dataclass(frozen=True, slots=True)
class EvidenceMemoryContract:
    total_records: int
    citation_required_records: int
    source_bound_records: int
    provenance_bound_records: int
    trace_bound_records: int
    conflict_detected_records: int
    memory_truth_records: int
    knowledge_graph_projection_records: int
    read_only_records: int
    ready_records: int
    records: tuple[EvidenceMemoryRecord, ...]

    def __post_init__(self) -> None:
        if self.total_records != len(self.records):
            raise ValueError("total_records must match records length")
        if self.total_records <= 0:
            raise ValueError("total_records must be >= 1")

        computed = {
            "citation_required_records": sum(
                1 for record in self.records if record.citation_required
            ),
            "source_bound_records": sum(
                1 for record in self.records if record.source_bound
            ),
            "provenance_bound_records": sum(
                1 for record in self.records if record.provenance_bound
            ),
            "trace_bound_records": sum(
                1 for record in self.records if record.trace_bound
            ),
            "conflict_detected_records": sum(
                1 for record in self.records if record.conflict_detected
            ),
            "memory_truth_records": sum(
                1 for record in self.records if record.memory_truth
            ),
            "knowledge_graph_projection_records": sum(
                1 for record in self.records if record.knowledge_graph_projection_only
            ),
            "read_only_records": sum(1 for record in self.records if record.read_only),
            "ready_records": sum(1 for record in self.records if record.evidence_ready),
        }

        for field_name, value in computed.items():
            if getattr(self, field_name) != value:
                raise ValueError(f"{field_name} must match computed count")

        if self.citation_required_records != self.total_records:
            raise ValueError("all evidence records must require citation")
        if self.source_bound_records != self.total_records:
            raise ValueError("all evidence records must be source-bound")
        if self.provenance_bound_records != self.total_records:
            raise ValueError("all evidence records must be provenance-bound")
        if self.trace_bound_records != self.total_records:
            raise ValueError("all evidence records must be trace-bound")
        if self.conflict_detected_records != 0:
            raise ValueError("conflict_detected_records must be 0")
        if self.memory_truth_records != self.total_records:
            raise ValueError("all evidence records must be memory truth")
        if self.knowledge_graph_projection_records != self.total_records:
            raise ValueError("all records must mark knowledge graph as projection-only")
        if self.read_only_records != self.total_records:
            raise ValueError("all evidence records must be read-only")
        if self.ready_records != self.total_records:
            raise ValueError("all evidence records must be ready")

        evidence_ids = tuple(record.evidence_id for record in self.records)
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("duplicate evidence_id values detected")
