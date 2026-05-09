from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryPolicyGovernanceScope = Literal[
    "foundational_memory",
    "operational_memory",
]

_SCOPE_ID_PATTERN = re.compile(r"^memory_policy_scope_[a-z][a-z0-9_]*$")


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
class MemoryPolicyScopeEntry:
    scope_id: str
    module_slug: str
    memory_tier_id: str
    retention_class: str
    governance_scope: MemoryPolicyGovernanceScope
    evidence_required: bool
    approval_required: bool
    conflict_resolution_required: bool
    promotion_allowed: bool
    auto_promotion_allowed: bool
    read_only: bool
    scope_ready: bool
    description: str

    def __post_init__(self) -> None:
        scope_id = _ensure_non_empty_str(self.scope_id, "scope_id")
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        memory_tier_id = _ensure_non_empty_str(self.memory_tier_id, "memory_tier_id")
        retention_class = _ensure_non_empty_str(self.retention_class, "retention_class")
        description = _ensure_non_empty_str(self.description, "description")

        if not _SCOPE_ID_PATTERN.fullmatch(scope_id):
            raise ValueError(f"Invalid scope_id: {scope_id}")

        for field_name in (
            "evidence_required",
            "approval_required",
            "conflict_resolution_required",
            "promotion_allowed",
            "auto_promotion_allowed",
            "read_only",
            "scope_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.evidence_required:
            raise ValueError("evidence_required must be True")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.conflict_resolution_required:
            raise ValueError("conflict_resolution_required must be True")
        if not self.promotion_allowed:
            raise ValueError("promotion_allowed must be True")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.scope_ready:
            raise ValueError("scope_ready must be True")

        object.__setattr__(self, "scope_id", scope_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "memory_tier_id", memory_tier_id)
        object.__setattr__(self, "retention_class", retention_class)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class MemoryPolicyScopeContract:
    total_scopes: int
    ready_scopes: int
    evidence_required_scopes: int
    approval_required_scopes: int
    conflict_resolution_required_scopes: int
    promotion_allowed_scopes: int
    auto_promotion_allowed_scopes: int
    read_only_scopes: int
    entries: tuple[MemoryPolicyScopeEntry, ...]

    def __post_init__(self) -> None:
        total_scopes = _ensure_non_negative_int(self.total_scopes, "total_scopes")
        if total_scopes != len(self.entries):
            raise ValueError("total_scopes must match entries length")
        if total_scopes <= 0:
            raise ValueError("total_scopes must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.scope_ready)
        computed_evidence = sum(1 for entry in self.entries if entry.evidence_required)
        computed_approval = sum(1 for entry in self.entries if entry.approval_required)
        computed_conflict = sum(
            1 for entry in self.entries if entry.conflict_resolution_required
        )
        computed_promotion = sum(1 for entry in self.entries if entry.promotion_allowed)
        computed_auto = sum(1 for entry in self.entries if entry.auto_promotion_allowed)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        if self.ready_scopes != computed_ready:
            raise ValueError("ready_scopes must match computed count")
        if self.evidence_required_scopes != computed_evidence:
            raise ValueError("evidence_required_scopes must match computed count")
        if self.approval_required_scopes != computed_approval:
            raise ValueError("approval_required_scopes must match computed count")
        if self.conflict_resolution_required_scopes != computed_conflict:
            raise ValueError("conflict_resolution_required_scopes must match computed count")
        if self.promotion_allowed_scopes != computed_promotion:
            raise ValueError("promotion_allowed_scopes must match computed count")
        if self.auto_promotion_allowed_scopes != computed_auto:
            raise ValueError("auto_promotion_allowed_scopes must match computed count")
        if self.read_only_scopes != computed_read_only:
            raise ValueError("read_only_scopes must match computed count")

        if self.ready_scopes != total_scopes:
            raise ValueError("all policy scopes must be ready")
        if self.evidence_required_scopes != total_scopes:
            raise ValueError("all policy scopes must require evidence")
        if self.approval_required_scopes != total_scopes:
            raise ValueError("all policy scopes must require approval")
        if self.conflict_resolution_required_scopes != total_scopes:
            raise ValueError("all policy scopes must require conflict resolution")
        if self.promotion_allowed_scopes != total_scopes:
            raise ValueError("all policy scopes must allow controlled promotion")
        if self.auto_promotion_allowed_scopes != 0:
            raise ValueError("auto promotion must be disabled")
        if self.read_only_scopes != total_scopes:
            raise ValueError("all policy scopes must be read-only")

        scope_ids = tuple(entry.scope_id for entry in self.entries)
        if len(set(scope_ids)) != len(scope_ids):
            raise ValueError("duplicate scope_id values detected")


def build_memory_policy_scope_contract() -> MemoryPolicyScopeContract:
    from MAKSIMAR_CORE_LIB.memory_policy.memory_classification_policy import (
        build_memory_classification_policy_contract,
    )

    classification = build_memory_classification_policy_contract()

    entries = tuple(
        MemoryPolicyScopeEntry(
            scope_id=f"memory_policy_scope_{_safe_id_suffix(entry.module_slug)}",
            module_slug=entry.module_slug,
            memory_tier_id=entry.memory_tier_id,
            retention_class=entry.retention_class,
            governance_scope=(
                "foundational_memory"
                if entry.retention_class == "foundational"
                else "operational_memory"
            ),
            evidence_required=True,
            approval_required=True,
            conflict_resolution_required=True,
            promotion_allowed=True,
            auto_promotion_allowed=False,
            read_only=True,
            scope_ready=entry.active,
            description=f"Governance scope for {entry.module_slug}.",
        )
        for entry in classification.entries
    )

    return MemoryPolicyScopeContract(
        total_scopes=len(entries),
        ready_scopes=sum(1 for entry in entries if entry.scope_ready),
        evidence_required_scopes=sum(1 for entry in entries if entry.evidence_required),
        approval_required_scopes=sum(1 for entry in entries if entry.approval_required),
        conflict_resolution_required_scopes=sum(
            1 for entry in entries if entry.conflict_resolution_required
        ),
        promotion_allowed_scopes=sum(1 for entry in entries if entry.promotion_allowed),
        auto_promotion_allowed_scopes=sum(
            1 for entry in entries if entry.auto_promotion_allowed
        ),
        read_only_scopes=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
