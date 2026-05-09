from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ConflictBindingStatus = Literal["resolved_review_ready"]

_CONFLICT_BINDING_ID_PATTERN = re.compile(r"^conflict_binding_[a-z][a-z0-9_]*$")
_CONFLICT_CASE_ID_PATTERN = re.compile(r"^conflict_[a-z][a-z0-9_]*$")


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


def safe_id_suffix(value: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("id suffix must be non-empty")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return suffix


@dataclass(frozen=True, slots=True)
class ConflictBindingEntry:
    conflict_binding_id: str
    conflict_case_id: str
    module_slug: str
    memory_tier_id: str
    governance_binding_id: str
    incoming_event_id: str
    existing_record_id: str
    resolved_record_id: str
    archived_record_id: str
    conflict_marker_id: str
    resolution_strategy: str
    resolution_status: str
    evidence_records: int
    evidence_bound: bool
    governance_bound: bool
    proposal_generated: bool
    approval_required: bool
    approval_granted: bool
    conflict_marker_present: bool
    version_incremented: bool
    resolution_recorded: bool
    memory_truth_required: bool
    knowledge_graph_projection_only: bool
    read_only: bool
    binding_status: ConflictBindingStatus
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        conflict_binding_id = _ensure_non_empty_str(
            self.conflict_binding_id,
            "conflict_binding_id",
        )
        conflict_case_id = _ensure_non_empty_str(
            self.conflict_case_id,
            "conflict_case_id",
        )
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        memory_tier_id = _ensure_non_empty_str(self.memory_tier_id, "memory_tier_id")
        governance_binding_id = _ensure_non_empty_str(
            self.governance_binding_id,
            "governance_binding_id",
        )
        incoming_event_id = _ensure_non_empty_str(
            self.incoming_event_id,
            "incoming_event_id",
        )
        existing_record_id = _ensure_non_empty_str(
            self.existing_record_id,
            "existing_record_id",
        )
        resolved_record_id = _ensure_non_empty_str(
            self.resolved_record_id,
            "resolved_record_id",
        )
        archived_record_id = _ensure_non_empty_str(
            self.archived_record_id,
            "archived_record_id",
        )
        conflict_marker_id = _ensure_non_empty_str(
            self.conflict_marker_id,
            "conflict_marker_id",
        )
        resolution_strategy = _ensure_non_empty_str(
            self.resolution_strategy,
            "resolution_strategy",
        )
        resolution_status = _ensure_non_empty_str(
            self.resolution_status,
            "resolution_status",
        )
        description = _ensure_non_empty_str(self.description, "description")

        if not _CONFLICT_BINDING_ID_PATTERN.fullmatch(conflict_binding_id):
            raise ValueError(f"Invalid conflict_binding_id: {conflict_binding_id}")
        if not _CONFLICT_CASE_ID_PATTERN.fullmatch(conflict_case_id):
            raise ValueError(f"Invalid conflict_case_id: {conflict_case_id}")

        _ensure_non_negative_int(self.evidence_records, "evidence_records")

        for field_name in (
            "evidence_bound",
            "governance_bound",
            "proposal_generated",
            "approval_required",
            "approval_granted",
            "conflict_marker_present",
            "version_incremented",
            "resolution_recorded",
            "memory_truth_required",
            "knowledge_graph_projection_only",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.evidence_records <= 0:
            raise ValueError("evidence_records must be >= 1")
        if not self.evidence_bound:
            raise ValueError("evidence_bound must be True")
        if not self.governance_bound:
            raise ValueError("governance_bound must be True")
        if not self.proposal_generated:
            raise ValueError("proposal_generated must be True")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.approval_granted:
            raise ValueError("approval_granted must be True")
        if not self.conflict_marker_present:
            raise ValueError("conflict_marker_present must be True")
        if not self.resolution_recorded:
            raise ValueError("resolution_recorded must be True")
        if resolution_status != "resolved":
            raise ValueError("resolution_status must be resolved")
        if resolution_strategy not in {"promote_new_version", "keep_existing_record"}:
            raise ValueError("unsupported resolution_strategy")
        if resolution_strategy == "promote_new_version" and not self.version_incremented:
            raise ValueError("promote_new_version must increment version")
        if resolution_strategy == "keep_existing_record" and self.version_incremented:
            raise ValueError("keep_existing_record must not increment version")
        if not self.memory_truth_required:
            raise ValueError("memory_truth_required must be True")
        if not self.knowledge_graph_projection_only:
            raise ValueError("knowledge_graph_projection_only must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.binding_status != "resolved_review_ready":
            raise ValueError("binding_status must be resolved_review_ready")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "conflict_binding_id", conflict_binding_id)
        object.__setattr__(self, "conflict_case_id", conflict_case_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "memory_tier_id", memory_tier_id)
        object.__setattr__(self, "governance_binding_id", governance_binding_id)
        object.__setattr__(self, "incoming_event_id", incoming_event_id)
        object.__setattr__(self, "existing_record_id", existing_record_id)
        object.__setattr__(self, "resolved_record_id", resolved_record_id)
        object.__setattr__(self, "archived_record_id", archived_record_id)
        object.__setattr__(self, "conflict_marker_id", conflict_marker_id)
        object.__setattr__(self, "resolution_strategy", resolution_strategy)
        object.__setattr__(self, "resolution_status", resolution_status)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class ConflictBindingContract:
    total_bindings: int
    ready_bindings: int
    evidence_bound_bindings: int
    governance_bound_bindings: int
    proposal_generated_bindings: int
    approval_required_bindings: int
    approval_granted_bindings: int
    conflict_marker_bindings: int
    resolved_bindings: int
    promote_new_version_bindings: int
    keep_existing_bindings: int
    memory_truth_required_bindings: int
    knowledge_graph_projection_bindings: int
    read_only_bindings: int
    entries: tuple[ConflictBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(
            self.total_bindings,
            "total_bindings",
        )
        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.binding_ready)
        computed_evidence = sum(1 for entry in self.entries if entry.evidence_bound)
        computed_governance = sum(1 for entry in self.entries if entry.governance_bound)
        computed_proposal = sum(1 for entry in self.entries if entry.proposal_generated)
        computed_approval_required = sum(
            1 for entry in self.entries if entry.approval_required
        )
        computed_approval_granted = sum(
            1 for entry in self.entries if entry.approval_granted
        )
        computed_marker = sum(
            1 for entry in self.entries if entry.conflict_marker_present
        )
        computed_resolved = sum(
            1 for entry in self.entries if entry.resolution_status == "resolved"
        )
        computed_promote = sum(
            1 for entry in self.entries
            if entry.resolution_strategy == "promote_new_version"
        )
        computed_keep = sum(
            1 for entry in self.entries
            if entry.resolution_strategy == "keep_existing_record"
        )
        computed_truth = sum(
            1 for entry in self.entries if entry.memory_truth_required
        )
        computed_projection = sum(
            1 for entry in self.entries if entry.knowledge_graph_projection_only
        )
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        expected_counts = {
            "ready_bindings": computed_ready,
            "evidence_bound_bindings": computed_evidence,
            "governance_bound_bindings": computed_governance,
            "proposal_generated_bindings": computed_proposal,
            "approval_required_bindings": computed_approval_required,
            "approval_granted_bindings": computed_approval_granted,
            "conflict_marker_bindings": computed_marker,
            "resolved_bindings": computed_resolved,
            "promote_new_version_bindings": computed_promote,
            "keep_existing_bindings": computed_keep,
            "memory_truth_required_bindings": computed_truth,
            "knowledge_graph_projection_bindings": computed_projection,
            "read_only_bindings": computed_read_only,
        }

        for field_name, expected_value in expected_counts.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all conflict bindings must be ready")
        if self.evidence_bound_bindings != total_bindings:
            raise ValueError("all conflict bindings must be evidence-bound")
        if self.governance_bound_bindings != total_bindings:
            raise ValueError("all conflict bindings must be governance-bound")
        if self.proposal_generated_bindings != total_bindings:
            raise ValueError("all conflict bindings must have proposal generated")
        if self.approval_required_bindings != total_bindings:
            raise ValueError("all conflict bindings must require approval")
        if self.approval_granted_bindings != total_bindings:
            raise ValueError("all conflict bindings must have approval granted")
        if self.conflict_marker_bindings != total_bindings:
            raise ValueError("all conflict bindings must have conflict markers")
        if self.resolved_bindings != total_bindings:
            raise ValueError("all conflict bindings must be resolved")
        if self.memory_truth_required_bindings != total_bindings:
            raise ValueError("all conflict bindings must require memory truth")
        if self.knowledge_graph_projection_bindings != total_bindings:
            raise ValueError("all conflict bindings must keep graph projection-only")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all conflict bindings must be read-only")

        binding_ids = tuple(entry.conflict_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate conflict_binding_id values detected")


def build_conflict_binding_contract() -> ConflictBindingContract:
    from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract
    from MAKSIMAR_CORE_LIB.memory_policy import build_governance_binding_contract
    from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION.memory_conflict_resolution_contract import (
        build_memory_conflict_resolution_contract,
    )

    evidence = build_evidence_memory_contract()
    governance = build_governance_binding_contract()
    conflict_resolution = build_memory_conflict_resolution_contract()

    governance_by_module = {
        entry.module_slug: entry
        for entry in governance.entries
    }

    entries = tuple(
        ConflictBindingEntry(
            conflict_binding_id=(
                "conflict_binding_"
                f"{safe_id_suffix(entry.module_slug)}_"
                f"{safe_id_suffix(entry.conflict_case_id)}_"
                f"{safe_id_suffix(entry.resolution_strategy)}"
            ),
            conflict_case_id=entry.conflict_case_id,
            module_slug=entry.module_slug,
            memory_tier_id=entry.memory_tier_id,
            governance_binding_id=governance_by_module[
                entry.module_slug
            ].governance_binding_id,
            incoming_event_id=entry.incoming_event_id,
            existing_record_id=entry.existing_record_id,
            resolved_record_id=entry.resolved_record_id,
            archived_record_id=entry.archived_record_id,
            conflict_marker_id=entry.conflict_marker_id,
            resolution_strategy=entry.resolution_strategy,
            resolution_status=entry.resolution_status,
            evidence_records=evidence.total_records,
            evidence_bound=evidence.ready_records == evidence.total_records,
            governance_bound=(
                entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].binding_ready
            ),
            proposal_generated=entry.proposal_generated,
            approval_required=entry.approval_required,
            approval_granted=entry.approval_granted,
            conflict_marker_present=bool(entry.conflict_marker_id),
            version_incremented=entry.version_incremented,
            resolution_recorded=(
                bool(entry.resolved_record_id)
                and bool(entry.archived_record_id)
                and entry.resolution_status == "resolved"
            ),
            memory_truth_required=(
                evidence.memory_truth_records == evidence.total_records
            ),
            knowledge_graph_projection_only=(
                evidence.knowledge_graph_projection_records == evidence.total_records
            ),
            read_only=governance_by_module[entry.module_slug].read_only,
            binding_status="resolved_review_ready",
            binding_ready=(
                entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].binding_ready
                and evidence.ready_records == evidence.total_records
                and evidence.conflict_detected_records == 0
                and entry.proposal_generated
                and entry.approval_required
                and entry.approval_granted
                and bool(entry.conflict_marker_id)
                and entry.resolution_status == "resolved"
                and bool(entry.resolved_record_id)
                and bool(entry.archived_record_id)
                and governance_by_module[entry.module_slug].read_only
            ),
            description=f"Conflict binding for {entry.conflict_case_id}.",
        )
        for entry in conflict_resolution.entries
    )

    return ConflictBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        evidence_bound_bindings=sum(1 for entry in entries if entry.evidence_bound),
        governance_bound_bindings=sum(1 for entry in entries if entry.governance_bound),
        proposal_generated_bindings=sum(
            1 for entry in entries if entry.proposal_generated
        ),
        approval_required_bindings=sum(
            1 for entry in entries if entry.approval_required
        ),
        approval_granted_bindings=sum(
            1 for entry in entries if entry.approval_granted
        ),
        conflict_marker_bindings=sum(
            1 for entry in entries if entry.conflict_marker_present
        ),
        resolved_bindings=sum(
            1 for entry in entries if entry.resolution_status == "resolved"
        ),
        promote_new_version_bindings=sum(
            1 for entry in entries
            if entry.resolution_strategy == "promote_new_version"
        ),
        keep_existing_bindings=sum(
            1 for entry in entries
            if entry.resolution_strategy == "keep_existing_record"
        ),
        memory_truth_required_bindings=sum(
            1 for entry in entries if entry.memory_truth_required
        ),
        knowledge_graph_projection_bindings=sum(
            1 for entry in entries if entry.knowledge_graph_projection_only
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
