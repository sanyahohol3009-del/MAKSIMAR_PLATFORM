from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_policy.memory_policy_scope_models import (
    build_memory_policy_scope_contract,
)


_GOVERNANCE_BINDING_ID_PATTERN = re.compile(r"^governance_binding_[a-z][a-z0-9_]*$")


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


def _safe_id_suffix(value: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("id suffix must be non-empty")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return suffix


@dataclass(frozen=True, slots=True)
class GovernanceBindingEntry:
    governance_binding_id: str
    scope_id: str
    module_slug: str
    memory_tier_id: str
    evidence_records: int
    conflict_detected_records: int
    citation_required_records: int
    approval_required: bool
    controlled_promotion_allowed: bool
    auto_promotion_allowed: bool
    conflict_resolution_required: bool
    memory_truth_required: bool
    knowledge_graph_projection_only: bool
    read_only: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        governance_binding_id = _ensure_non_empty_str(
            self.governance_binding_id,
            "governance_binding_id",
        )
        scope_id = _ensure_non_empty_str(self.scope_id, "scope_id")
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        memory_tier_id = _ensure_non_empty_str(self.memory_tier_id, "memory_tier_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _GOVERNANCE_BINDING_ID_PATTERN.fullmatch(governance_binding_id):
            raise ValueError(f"Invalid governance_binding_id: {governance_binding_id}")

        for field_name in (
            "evidence_records",
            "conflict_detected_records",
            "citation_required_records",
        ):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in (
            "approval_required",
            "controlled_promotion_allowed",
            "auto_promotion_allowed",
            "conflict_resolution_required",
            "memory_truth_required",
            "knowledge_graph_projection_only",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.evidence_records <= 0:
            raise ValueError("evidence_records must be >= 1")
        if self.conflict_detected_records != 0:
            raise ValueError("conflict_detected_records must be 0")
        if self.citation_required_records != self.evidence_records:
            raise ValueError("citation_required_records must match evidence_records")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.controlled_promotion_allowed:
            raise ValueError("controlled_promotion_allowed must be True")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if not self.conflict_resolution_required:
            raise ValueError("conflict_resolution_required must be True")
        if not self.memory_truth_required:
            raise ValueError("memory_truth_required must be True")
        if not self.knowledge_graph_projection_only:
            raise ValueError("knowledge_graph_projection_only must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "governance_binding_id", governance_binding_id)
        object.__setattr__(self, "scope_id", scope_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "memory_tier_id", memory_tier_id)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class GovernanceBindingContract:
    total_bindings: int
    ready_bindings: int
    approval_required_bindings: int
    controlled_promotion_bindings: int
    auto_promotion_allowed_bindings: int
    conflict_resolution_required_bindings: int
    conflict_detected_bindings: int
    memory_truth_required_bindings: int
    knowledge_graph_projection_bindings: int
    read_only_bindings: int
    entries: tuple[GovernanceBindingEntry, ...]

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
        computed_approval = sum(1 for entry in self.entries if entry.approval_required)
        computed_promotion = sum(
            1 for entry in self.entries if entry.controlled_promotion_allowed
        )
        computed_auto = sum(
            1 for entry in self.entries if entry.auto_promotion_allowed
        )
        computed_conflict_required = sum(
            1 for entry in self.entries if entry.conflict_resolution_required
        )
        computed_conflict_detected = sum(
            1 for entry in self.entries if entry.conflict_detected_records > 0
        )
        computed_truth = sum(
            1 for entry in self.entries if entry.memory_truth_required
        )
        computed_projection = sum(
            1 for entry in self.entries if entry.knowledge_graph_projection_only
        )
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        if self.ready_bindings != computed_ready:
            raise ValueError("ready_bindings must match computed count")
        if self.approval_required_bindings != computed_approval:
            raise ValueError("approval_required_bindings must match computed count")
        if self.controlled_promotion_bindings != computed_promotion:
            raise ValueError("controlled_promotion_bindings must match computed count")
        if self.auto_promotion_allowed_bindings != computed_auto:
            raise ValueError("auto_promotion_allowed_bindings must match computed count")
        if self.conflict_resolution_required_bindings != computed_conflict_required:
            raise ValueError("conflict_resolution_required_bindings must match computed count")
        if self.conflict_detected_bindings != computed_conflict_detected:
            raise ValueError("conflict_detected_bindings must match computed count")
        if self.memory_truth_required_bindings != computed_truth:
            raise ValueError("memory_truth_required_bindings must match computed count")
        if self.knowledge_graph_projection_bindings != computed_projection:
            raise ValueError("knowledge_graph_projection_bindings must match computed count")
        if self.read_only_bindings != computed_read_only:
            raise ValueError("read_only_bindings must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all governance bindings must be ready")
        if self.approval_required_bindings != total_bindings:
            raise ValueError("all governance bindings must require approval")
        if self.controlled_promotion_bindings != total_bindings:
            raise ValueError("all governance bindings must allow controlled promotion")
        if self.auto_promotion_allowed_bindings != 0:
            raise ValueError("auto promotion must be disabled")
        if self.conflict_resolution_required_bindings != total_bindings:
            raise ValueError("all governance bindings must require conflict resolution")
        if self.conflict_detected_bindings != 0:
            raise ValueError("governance bindings must be conflict-clear")
        if self.memory_truth_required_bindings != total_bindings:
            raise ValueError("all governance bindings must require memory truth")
        if self.knowledge_graph_projection_bindings != total_bindings:
            raise ValueError("all governance bindings must keep knowledge graph projection-only")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all governance bindings must be read-only")

        binding_ids = tuple(entry.governance_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate governance_binding_id values detected")


def build_governance_binding_contract() -> GovernanceBindingContract:
    from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract

    scope_contract = build_memory_policy_scope_contract()
    evidence = build_evidence_memory_contract()

    entries = tuple(
        GovernanceBindingEntry(
            governance_binding_id=(
                f"governance_binding_{_safe_id_suffix(scope.module_slug)}"
            ),
            scope_id=scope.scope_id,
            module_slug=scope.module_slug,
            memory_tier_id=scope.memory_tier_id,
            evidence_records=evidence.total_records,
            conflict_detected_records=evidence.conflict_detected_records,
            citation_required_records=evidence.citation_required_records,
            approval_required=scope.approval_required,
            controlled_promotion_allowed=scope.promotion_allowed,
            auto_promotion_allowed=scope.auto_promotion_allowed,
            conflict_resolution_required=scope.conflict_resolution_required,
            memory_truth_required=evidence.memory_truth_records == evidence.total_records,
            knowledge_graph_projection_only=(
                evidence.knowledge_graph_projection_records == evidence.total_records
            ),
            read_only=scope.read_only and evidence.read_only_records == evidence.total_records,
            binding_ready=(
                scope.scope_ready
                and evidence.ready_records == evidence.total_records
                and evidence.conflict_detected_records == 0
                and evidence.citation_required_records == evidence.total_records
                and scope.approval_required
                and scope.promotion_allowed
                and not scope.auto_promotion_allowed
                and scope.conflict_resolution_required
                and scope.read_only
            ),
            description=f"Governance binding for {scope.module_slug}.",
        )
        for scope in scope_contract.entries
    )

    return GovernanceBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        approval_required_bindings=sum(
            1 for entry in entries if entry.approval_required
        ),
        controlled_promotion_bindings=sum(
            1 for entry in entries if entry.controlled_promotion_allowed
        ),
        auto_promotion_allowed_bindings=sum(
            1 for entry in entries if entry.auto_promotion_allowed
        ),
        conflict_resolution_required_bindings=sum(
            1 for entry in entries if entry.conflict_resolution_required
        ),
        conflict_detected_bindings=sum(
            1 for entry in entries if entry.conflict_detected_records > 0
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
