from __future__ import annotations

import re
from dataclasses import dataclass


_CHAIN_ID_PATTERN = re.compile(r"^evidence_chain_[a-z][a-z0-9_]*$")
_EVIDENCE_ID_PATTERN = re.compile(r"^evidence_[a-z][a-z0-9_]*$")
_SOURCE_ID_PATTERN = re.compile(r"^retrieval_source_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class EvidenceSourceChainEntry:
    chain_id: str
    evidence_id: str
    source_id: str
    source_layer: str
    artifact_ref: str
    citation_required: bool
    conflict_marker: str
    source_bound: bool
    provenance_bound: bool
    trace_bound: bool
    dashboard_visible: bool
    chain_ready: bool

    def __post_init__(self) -> None:
        chain_id = _ensure_non_empty_str(self.chain_id, "chain_id")
        evidence_id = _ensure_non_empty_str(self.evidence_id, "evidence_id")
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_layer = _ensure_non_empty_str(self.source_layer, "source_layer")
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")

        if not _CHAIN_ID_PATTERN.fullmatch(chain_id):
            raise ValueError(f"Invalid chain_id: {chain_id}")
        if not _EVIDENCE_ID_PATTERN.fullmatch(evidence_id):
            raise ValueError(f"Invalid evidence_id: {evidence_id}")
        if not _SOURCE_ID_PATTERN.fullmatch(source_id):
            raise ValueError(f"Invalid source_id: {source_id}")
        if not artifact_ref.startswith("artifact://"):
            raise ValueError("artifact_ref must start with artifact://")

        for field_name in (
            "citation_required",
            "source_bound",
            "provenance_bound",
            "trace_bound",
            "dashboard_visible",
            "chain_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.citation_required:
            raise ValueError("citation_required must be True")
        if self.conflict_marker:
            raise ValueError("conflict_marker must be empty in PHASE 2.1 Batch 1")
        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.provenance_bound:
            raise ValueError("provenance_bound must be True")
        if not self.trace_bound:
            raise ValueError("trace_bound must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.chain_ready:
            raise ValueError("chain_ready must be True")

        object.__setattr__(self, "chain_id", chain_id)
        object.__setattr__(self, "evidence_id", evidence_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_layer", source_layer)
        object.__setattr__(self, "artifact_ref", artifact_ref)


@dataclass(frozen=True, slots=True)
class EvidenceSourceChainContract:
    total_items: int
    source_bound_items: int
    provenance_bound_items: int
    trace_bound_items: int
    citation_required_items: int
    conflict_marked_items: int
    dashboard_visible_items: int
    ready_items: int
    retrieval_phase_ready: bool
    storage_phase_ready: bool
    media_phase_ready: bool
    architecture_control_ready: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    entries: tuple[EvidenceSourceChainEntry, ...]

    def __post_init__(self) -> None:
        total_items = _ensure_non_negative_int(self.total_items, "total_items")
        source_bound_items = _ensure_non_negative_int(
            self.source_bound_items,
            "source_bound_items",
        )
        provenance_bound_items = _ensure_non_negative_int(
            self.provenance_bound_items,
            "provenance_bound_items",
        )
        trace_bound_items = _ensure_non_negative_int(
            self.trace_bound_items,
            "trace_bound_items",
        )
        citation_required_items = _ensure_non_negative_int(
            self.citation_required_items,
            "citation_required_items",
        )
        conflict_marked_items = _ensure_non_negative_int(
            self.conflict_marked_items,
            "conflict_marked_items",
        )
        dashboard_visible_items = _ensure_non_negative_int(
            self.dashboard_visible_items,
            "dashboard_visible_items",
        )
        ready_items = _ensure_non_negative_int(self.ready_items, "ready_items")

        if total_items != len(self.entries):
            raise ValueError("total_items must match entries length")
        if total_items <= 0:
            raise ValueError("total_items must be >= 1")

        computed_source_bound = sum(1 for entry in self.entries if entry.source_bound)
        computed_provenance_bound = sum(
            1 for entry in self.entries if entry.provenance_bound
        )
        computed_trace_bound = sum(1 for entry in self.entries if entry.trace_bound)
        computed_citation_required = sum(
            1 for entry in self.entries if entry.citation_required
        )
        computed_conflict_marked = sum(
            1 for entry in self.entries if entry.conflict_marker
        )
        computed_dashboard_visible = sum(
            1 for entry in self.entries if entry.dashboard_visible
        )
        computed_ready = sum(1 for entry in self.entries if entry.chain_ready)

        if source_bound_items != computed_source_bound:
            raise ValueError("source_bound_items must match computed count")
        if provenance_bound_items != computed_provenance_bound:
            raise ValueError("provenance_bound_items must match computed count")
        if trace_bound_items != computed_trace_bound:
            raise ValueError("trace_bound_items must match computed count")
        if citation_required_items != computed_citation_required:
            raise ValueError("citation_required_items must match computed count")
        if conflict_marked_items != computed_conflict_marked:
            raise ValueError("conflict_marked_items must match computed count")
        if dashboard_visible_items != computed_dashboard_visible:
            raise ValueError("dashboard_visible_items must match computed count")
        if ready_items != computed_ready:
            raise ValueError("ready_items must match computed count")

        for field_name in (
            "retrieval_phase_ready",
            "storage_phase_ready",
            "media_phase_ready",
            "architecture_control_ready",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if source_bound_items != total_items:
            raise ValueError("all evidence items must be source-bound")
        if provenance_bound_items != total_items:
            raise ValueError("all evidence items must be provenance-bound")
        if trace_bound_items != total_items:
            raise ValueError("all evidence items must be trace-bound")
        if citation_required_items != total_items:
            raise ValueError("all evidence items must require citation")
        if conflict_marked_items != 0:
            raise ValueError("conflict_marked_items must be 0 in Batch 1")
        if dashboard_visible_items != total_items:
            raise ValueError("all evidence items must be dashboard-visible")
        if ready_items != total_items:
            raise ValueError("all evidence source chains must be ready")

        if not self.retrieval_phase_ready:
            raise ValueError("retrieval_phase_ready must be True")
        if not self.storage_phase_ready:
            raise ValueError("storage_phase_ready must be True")
        if not self.media_phase_ready:
            raise ValueError("media_phase_ready must be True")
        if not self.architecture_control_ready:
            raise ValueError("architecture_control_ready must be True")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")

        chain_ids = tuple(entry.chain_id for entry in self.entries)
        evidence_ids = tuple(entry.evidence_id for entry in self.entries)

        if len(set(chain_ids)) != len(chain_ids):
            raise ValueError("duplicate chain_id values detected")
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError("duplicate evidence_id values detected")

        object.__setattr__(self, "total_items", total_items)
        object.__setattr__(self, "source_bound_items", source_bound_items)
        object.__setattr__(self, "provenance_bound_items", provenance_bound_items)
        object.__setattr__(self, "trace_bound_items", trace_bound_items)
        object.__setattr__(self, "citation_required_items", citation_required_items)
        object.__setattr__(self, "conflict_marked_items", conflict_marked_items)
        object.__setattr__(self, "dashboard_visible_items", dashboard_visible_items)
        object.__setattr__(self, "ready_items", ready_items)
