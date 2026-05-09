from __future__ import annotations

import re
from dataclasses import dataclass


_EVIDENCE_ID_PATTERN = re.compile(r"^evidence_[a-z][a-z0-9_]*$")
_SOURCE_ID_PATTERN = re.compile(r"^retrieval_source_[a-z][a-z0-9_]*$")


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


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalEvidenceItem:
    evidence_id: str
    source_id: str
    source_event_ref: str
    artifact_ref: str
    source_version: str
    summary: str
    citation_required: bool
    conflict_marker: str

    def __post_init__(self) -> None:
        evidence_id = _ensure_non_empty_str(self.evidence_id, "evidence_id")
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_event_ref = _ensure_non_empty_str(
            self.source_event_ref,
            "source_event_ref",
        )
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")
        source_version = _ensure_non_empty_str(self.source_version, "source_version")
        summary = _ensure_non_empty_str(self.summary, "summary")
        conflict_marker = self.conflict_marker.strip() if isinstance(self.conflict_marker, str) else ""

        if not _EVIDENCE_ID_PATTERN.fullmatch(evidence_id):
            raise ValueError(f"Invalid evidence_id: {evidence_id}")
        if not _SOURCE_ID_PATTERN.fullmatch(source_id):
            raise ValueError(f"Invalid source_id: {source_id}")

        _ensure_bool(self.citation_required, "citation_required")
        if not self.citation_required:
            raise ValueError("citation_required must be True")

        object.__setattr__(self, "evidence_id", evidence_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_event_ref", source_event_ref)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "source_version", source_version)
        object.__setattr__(self, "summary", summary)
        object.__setattr__(self, "conflict_marker", conflict_marker)


@dataclass(frozen=True, slots=True)
class RetrievalEvidencePack:
    request_id: str
    total_items: int
    citation_required_items: int
    conflict_marked_items: int
    evidence_items: tuple[RetrievalEvidenceItem, ...]

    def __post_init__(self) -> None:
        request_id = _ensure_non_empty_str(self.request_id, "request_id")
        total_items = _ensure_non_negative_int(self.total_items, "total_items")
        citation_required_items = _ensure_non_negative_int(
            self.citation_required_items,
            "citation_required_items",
        )
        conflict_marked_items = _ensure_non_negative_int(
            self.conflict_marked_items,
            "conflict_marked_items",
        )

        if total_items != len(self.evidence_items):
            raise ValueError("total_items must match evidence_items length")
        if total_items <= 0:
            raise ValueError("evidence pack must contain at least one item")
        if citation_required_items != sum(
            1 for item in self.evidence_items if item.citation_required
        ):
            raise ValueError("citation_required_items must match computed count")
        if conflict_marked_items != sum(
            1 for item in self.evidence_items if item.conflict_marker
        ):
            raise ValueError("conflict_marked_items must match computed count")

        evidence_ids = tuple(item.evidence_id for item in self.evidence_items)
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("duplicate evidence_id values detected")

        object.__setattr__(self, "request_id", request_id)
        object.__setattr__(self, "total_items", total_items)
        object.__setattr__(self, "citation_required_items", citation_required_items)
        object.__setattr__(self, "conflict_marked_items", conflict_marked_items)
