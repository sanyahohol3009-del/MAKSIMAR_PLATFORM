from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


PromotionBindingStatus = Literal["ready_for_review", "blocked"]

_PROMOTION_BINDING_ID_PATTERN = re.compile(r"^promotion_binding_[a-z][a-z0-9_]*$")


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
class PromotionBindingEntry:
    promotion_binding_id: str
    module_slug: str
    memory_tier_id: str
    input_event_id: str
    evidence_records: int
    promoted_entries: int
    archived_entries: int
    evidence_bound: bool
    classification_passed: bool
    deduplication_passed: bool
    conflict_check_passed: bool
    governance_bound: bool
    approval_required: bool
    auto_promotion_allowed: bool
    controlled_promotion_allowed: bool
    read_only: bool
    binding_status: PromotionBindingStatus
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        promotion_binding_id = _ensure_non_empty_str(
            self.promotion_binding_id,
            "promotion_binding_id",
        )
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        memory_tier_id = _ensure_non_empty_str(self.memory_tier_id, "memory_tier_id")
        input_event_id = _ensure_non_empty_str(self.input_event_id, "input_event_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _PROMOTION_BINDING_ID_PATTERN.fullmatch(promotion_binding_id):
            raise ValueError(f"Invalid promotion_binding_id: {promotion_binding_id}")

        for field_name in ("evidence_records", "promoted_entries", "archived_entries"):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in (
            "evidence_bound",
            "classification_passed",
            "deduplication_passed",
            "conflict_check_passed",
            "governance_bound",
            "approval_required",
            "auto_promotion_allowed",
            "controlled_promotion_allowed",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.evidence_records <= 0:
            raise ValueError("evidence_records must be >= 1")
        if self.promoted_entries + self.archived_entries <= 0:
            raise ValueError("promotion binding must reference at least one disposition")
        if not self.evidence_bound:
            raise ValueError("evidence_bound must be True")
        if not self.classification_passed:
            raise ValueError("classification_passed must be True")
        if not self.deduplication_passed and self.promoted_entries > 0:
            raise ValueError("deduplication_passed must be True for promoted entries")
        if not self.deduplication_passed and self.archived_entries <= 0:
            raise ValueError(
                "deduplication_passed may be False only for archived entries"
            )
        if not self.conflict_check_passed and self.promoted_entries > 0:
            raise ValueError("conflict_check_passed must be True for promoted entries")
        if not self.conflict_check_passed and self.archived_entries <= 0:
            raise ValueError(
                "conflict_check_passed may be False only for archived entries"
            )
        if not self.governance_bound:
            raise ValueError("governance_bound must be True")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if not self.controlled_promotion_allowed:
            raise ValueError("controlled_promotion_allowed must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.binding_status != "ready_for_review":
            raise ValueError("binding_status must be ready_for_review")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "promotion_binding_id", promotion_binding_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "memory_tier_id", memory_tier_id)
        object.__setattr__(self, "input_event_id", input_event_id)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class PromotionBindingContract:
    total_bindings: int
    ready_bindings: int
    evidence_bound_bindings: int
    governance_bound_bindings: int
    approval_required_bindings: int
    auto_promotion_allowed_bindings: int
    controlled_promotion_bindings: int
    read_only_bindings: int
    promoted_entries: int
    archived_entries: int
    entries: tuple[PromotionBindingEntry, ...]

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
        computed_approval = sum(1 for entry in self.entries if entry.approval_required)
        computed_auto = sum(1 for entry in self.entries if entry.auto_promotion_allowed)
        computed_controlled = sum(
            1 for entry in self.entries if entry.controlled_promotion_allowed
        )
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)
        computed_promoted = sum(entry.promoted_entries for entry in self.entries)
        computed_archived = sum(entry.archived_entries for entry in self.entries)

        if self.ready_bindings != computed_ready:
            raise ValueError("ready_bindings must match computed count")
        if self.evidence_bound_bindings != computed_evidence:
            raise ValueError("evidence_bound_bindings must match computed count")
        if self.governance_bound_bindings != computed_governance:
            raise ValueError("governance_bound_bindings must match computed count")
        if self.approval_required_bindings != computed_approval:
            raise ValueError("approval_required_bindings must match computed count")
        if self.auto_promotion_allowed_bindings != computed_auto:
            raise ValueError("auto_promotion_allowed_bindings must match computed count")
        if self.controlled_promotion_bindings != computed_controlled:
            raise ValueError("controlled_promotion_bindings must match computed count")
        if self.read_only_bindings != computed_read_only:
            raise ValueError("read_only_bindings must match computed count")
        if self.promoted_entries != computed_promoted:
            raise ValueError("promoted_entries must match computed count")
        if self.archived_entries != computed_archived:
            raise ValueError("archived_entries must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all promotion bindings must be ready")
        if self.evidence_bound_bindings != total_bindings:
            raise ValueError("all promotion bindings must be evidence-bound")
        if self.governance_bound_bindings != total_bindings:
            raise ValueError("all promotion bindings must be governance-bound")
        if self.approval_required_bindings != total_bindings:
            raise ValueError("all promotion bindings must require approval")
        if self.auto_promotion_allowed_bindings != 0:
            raise ValueError("auto promotion must be disabled")
        if self.controlled_promotion_bindings != total_bindings:
            raise ValueError("controlled promotion must be enabled")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all promotion bindings must be read-only")

        binding_ids = tuple(entry.promotion_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate promotion_binding_id values detected")
