from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


CodegenBoundaryKind = Literal[
    "immutable_core_boundary",
    "runtime_mutation_boundary",
    "deployment_boundary",
    "sandbox_boundary",
    "artifact_boundary",
    "approval_boundary",
]


@dataclass(frozen=True, slots=True)
class CodegenBoundaryRule:
    rule_id: str
    boundary_kind: CodegenBoundaryKind
    boundary_path: str
    crossing_allowed_now: bool
    proposal_required: bool
    audit_required: bool
    approval_required: bool
    sandbox_required_later: bool
    evidence_required: bool
    rule_ready: bool

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id must be non-empty")
        if not self.boundary_path:
            raise ValueError("boundary_path must be non-empty")
        if self.crossing_allowed_now:
            raise ValueError("crossing_allowed_now must be False")
        if self.proposal_required is not True:
            raise ValueError("proposal_required must be True")
        if self.audit_required is not True:
            raise ValueError("audit_required must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.evidence_required is not True:
            raise ValueError("evidence_required must be True")
        if self.boundary_kind in {"immutable_core_boundary", "deployment_boundary", "sandbox_boundary"}:
            if self.sandbox_required_later is not True:
                raise ValueError(f"{self.boundary_kind} requires sandbox_required_later=True")
        if self.rule_ready is not True:
            raise ValueError("rule_ready must be True")


@dataclass(frozen=True, slots=True)
class CodegenBoundaryContract:
    contract_id: str
    rules: Tuple[CodegenBoundaryRule, ...]
    immutable_core_protected: bool
    runtime_mutation_blocked: bool
    deployment_blocked: bool
    sandbox_execution_deferred: bool
    artifact_reference_required: bool
    approval_boundary_ready: bool
    boundary_contract_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if not self.rules:
            raise ValueError("rules must be non-empty")
        rule_ids = {rule.rule_id for rule in self.rules}
        if len(rule_ids) != len(self.rules):
            raise ValueError("rule_id values must be unique")
        if self.immutable_core_protected is not True:
            raise ValueError("immutable_core_protected must be True")
        if self.runtime_mutation_blocked is not True:
            raise ValueError("runtime_mutation_blocked must be True")
        if self.deployment_blocked is not True:
            raise ValueError("deployment_blocked must be True")
        if self.sandbox_execution_deferred is not True:
            raise ValueError("sandbox_execution_deferred must be True")
        if self.artifact_reference_required is not True:
            raise ValueError("artifact_reference_required must be True")
        if self.approval_boundary_ready is not True:
            raise ValueError("approval_boundary_ready must be True")
        if not all(rule.rule_ready for rule in self.rules):
            raise ValueError("all rules must be ready")
        if self.boundary_contract_ready is not True:
            raise ValueError("boundary_contract_ready must be True")


def build_codegen_boundary_contract() -> CodegenBoundaryContract:
    rules = (
        CodegenBoundaryRule(
            rule_id="boundary_immutable_core_no_direct_write",
            boundary_kind="immutable_core_boundary",
            boundary_path="CORE_ROOT",
            crossing_allowed_now=False,
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            evidence_required=True,
            rule_ready=True,
        ),
        CodegenBoundaryRule(
            rule_id="boundary_runtime_no_mutation",
            boundary_kind="runtime_mutation_boundary",
            boundary_path="RUNTIME",
            crossing_allowed_now=False,
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            evidence_required=True,
            rule_ready=True,
        ),
        CodegenBoundaryRule(
            rule_id="boundary_deployment_blocked",
            boundary_kind="deployment_boundary",
            boundary_path="deployment",
            crossing_allowed_now=False,
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            evidence_required=True,
            rule_ready=True,
        ),
        CodegenBoundaryRule(
            rule_id="boundary_sandbox_deferred",
            boundary_kind="sandbox_boundary",
            boundary_path="sandbox",
            crossing_allowed_now=False,
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            evidence_required=True,
            rule_ready=True,
        ),
        CodegenBoundaryRule(
            rule_id="boundary_artifact_ref_required",
            boundary_kind="artifact_boundary",
            boundary_path="DATA_PLANE/artifacts",
            crossing_allowed_now=False,
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            evidence_required=True,
            rule_ready=True,
        ),
        CodegenBoundaryRule(
            rule_id="boundary_approval_required",
            boundary_kind="approval_boundary",
            boundary_path="MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            crossing_allowed_now=False,
            proposal_required=True,
            audit_required=True,
            approval_required=True,
            sandbox_required_later=True,
            evidence_required=True,
            rule_ready=True,
        ),
    )

    return CodegenBoundaryContract(
        contract_id="codegen_boundary_contract_phase_6_3_001",
        rules=rules,
        immutable_core_protected=True,
        runtime_mutation_blocked=True,
        deployment_blocked=True,
        sandbox_execution_deferred=True,
        artifact_reference_required=True,
        approval_boundary_ready=True,
        boundary_contract_ready=True,
    )
