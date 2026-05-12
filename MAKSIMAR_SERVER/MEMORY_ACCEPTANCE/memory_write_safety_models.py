from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


MemoryWriteScope = Literal[
    "read_only_preview",
    "sandbox_draft",
    "staging_candidate",
    "canonical_release",
]


@dataclass(frozen=True, slots=True)
class MemoryWriteSafetyRule:
    rule_id: str
    write_scope: MemoryWriteScope
    write_allowed: bool
    approval_required: bool
    approval_granted_by_default: bool
    sandbox_stage_required: bool
    diff_preview_required: bool
    risk_summary_required: bool
    audit_trail_required: bool
    direct_canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    rule_ready: bool

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id must be non-empty")
        if self.direct_canonical_write_allowed:
            raise ValueError("direct_canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.approval_granted_by_default:
            raise ValueError("approval_granted_by_default must be False")
        if self.write_scope in {"sandbox_draft", "staging_candidate", "canonical_release"}:
            if self.approval_required is not True:
                raise ValueError(f"approval_required must be True for {self.write_scope}")
            if self.diff_preview_required is not True:
                raise ValueError(f"diff_preview_required must be True for {self.write_scope}")
            if self.risk_summary_required is not True:
                raise ValueError(f"risk_summary_required must be True for {self.write_scope}")
            if self.audit_trail_required is not True:
                raise ValueError(f"audit_trail_required must be True for {self.write_scope}")
        if self.write_scope == "canonical_release" and self.sandbox_stage_required is not True:
            raise ValueError("canonical_release requires sandbox_stage_required=True")
        if self.rule_ready is not True:
            raise ValueError("rule_ready must be True")


@dataclass(frozen=True, slots=True)
class MemoryWriteSafetyPolicy:
    policy_id: str
    rules: Tuple[MemoryWriteSafetyRule, ...]
    duplicate_write_allowed: bool
    direct_runtime_to_canonical_write_allowed: bool
    canonical_write_allowed_without_approval: bool
    runtime_mutation_allowed: bool
    policy_ready: bool

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must be non-empty")
        if not self.rules:
            raise ValueError("rules must be non-empty")
        rule_ids = {rule.rule_id for rule in self.rules}
        if len(rule_ids) != len(self.rules):
            raise ValueError("rule_id values must be unique")
        if self.duplicate_write_allowed:
            raise ValueError("duplicate_write_allowed must be False")
        if self.direct_runtime_to_canonical_write_allowed:
            raise ValueError("direct_runtime_to_canonical_write_allowed must be False")
        if self.canonical_write_allowed_without_approval:
            raise ValueError("canonical_write_allowed_without_approval must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(rule.rule_ready for rule in self.rules):
            raise ValueError("all rules must be ready")
        if self.policy_ready is not True:
            raise ValueError("policy_ready must be True")


def build_memory_write_safety_policy() -> MemoryWriteSafetyPolicy:
    rules = (
        MemoryWriteSafetyRule(
            rule_id="read_only_preview_no_write",
            write_scope="read_only_preview",
            write_allowed=False,
            approval_required=False,
            approval_granted_by_default=False,
            sandbox_stage_required=False,
            diff_preview_required=False,
            risk_summary_required=False,
            audit_trail_required=True,
            direct_canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            rule_ready=True,
        ),
        MemoryWriteSafetyRule(
            rule_id="sandbox_draft_guarded_write",
            write_scope="sandbox_draft",
            write_allowed=True,
            approval_required=True,
            approval_granted_by_default=False,
            sandbox_stage_required=True,
            diff_preview_required=True,
            risk_summary_required=True,
            audit_trail_required=True,
            direct_canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            rule_ready=True,
        ),
        MemoryWriteSafetyRule(
            rule_id="staging_candidate_guarded_write",
            write_scope="staging_candidate",
            write_allowed=True,
            approval_required=True,
            approval_granted_by_default=False,
            sandbox_stage_required=True,
            diff_preview_required=True,
            risk_summary_required=True,
            audit_trail_required=True,
            direct_canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            rule_ready=True,
        ),
        MemoryWriteSafetyRule(
            rule_id="canonical_release_requires_promotion",
            write_scope="canonical_release",
            write_allowed=False,
            approval_required=True,
            approval_granted_by_default=False,
            sandbox_stage_required=True,
            diff_preview_required=True,
            risk_summary_required=True,
            audit_trail_required=True,
            direct_canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            rule_ready=True,
        ),
    )

    return MemoryWriteSafetyPolicy(
        policy_id="memory_write_safety_policy_phase_6_0_001",
        rules=rules,
        duplicate_write_allowed=False,
        direct_runtime_to_canonical_write_allowed=False,
        canonical_write_allowed_without_approval=False,
        runtime_mutation_allowed=False,
        policy_ready=True,
    )
