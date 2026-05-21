from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.feedback_engine_contract import (
    FeedbackEngineContract,
    build_default_feedback_engine_contract,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.finops_budget_contract import (
    FinOpsBudgetContract,
    build_default_finops_budget_contract,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_provenance_contract import (
    ModelProvenanceContract,
    build_default_model_provenance_contract,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.orchestration_policy import (
    AIOrchestrationPolicy,
    build_default_ai_orchestration_policy,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.proposal_staging_contract import (
    ProposalStagingContract,
    build_default_proposal_staging_contract,
)


@dataclass(frozen=True, slots=True)
class AIOrchestrationReadModel:
    read_model_id: str
    proposal_staging: ProposalStagingContract
    model_provenance: ModelProvenanceContract
    finops_budget: FinOpsBudgetContract
    feedback_engine: FeedbackEngineContract
    orchestration_policy: AIOrchestrationPolicy
    proposal_ready: bool
    provenance_ready: bool
    budget_guard_ready: bool
    feedback_ready: bool
    may_propose: bool
    may_apply: bool
    execution_allowed: bool
    runtime_mutation_allowed: bool
    production_deployment_allowed: bool
    public_exposure_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.proposal_staging, ProposalStagingContract):
            raise TypeError("proposal_staging must be ProposalStagingContract")
        if not isinstance(self.model_provenance, ModelProvenanceContract):
            raise TypeError("model_provenance must be ModelProvenanceContract")
        if not isinstance(self.finops_budget, FinOpsBudgetContract):
            raise TypeError("finops_budget must be FinOpsBudgetContract")
        if not isinstance(self.feedback_engine, FeedbackEngineContract):
            raise TypeError("feedback_engine must be FeedbackEngineContract")
        if not isinstance(self.orchestration_policy, AIOrchestrationPolicy):
            raise TypeError("orchestration_policy must be AIOrchestrationPolicy")

        _validate_true("proposal_ready", self.proposal_ready)
        _validate_true("provenance_ready", self.provenance_ready)
        _validate_true("budget_guard_ready", self.budget_guard_ready)
        _validate_true("feedback_ready", self.feedback_ready)
        _validate_true("may_propose", self.may_propose)
        _validate_false("may_apply", self.may_apply)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("production_deployment_allowed", self.production_deployment_allowed)
        _validate_false("public_exposure_allowed", self.public_exposure_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "proposal_staging": self.proposal_staging.to_dict(),
            "model_provenance": self.model_provenance.to_dict(),
            "finops_budget": self.finops_budget.to_dict(),
            "feedback_engine": self.feedback_engine.to_dict(),
            "orchestration_policy": self.orchestration_policy.to_dict(),
            "proposal_ready": self.proposal_ready,
            "provenance_ready": self.provenance_ready,
            "budget_guard_ready": self.budget_guard_ready,
            "feedback_ready": self.feedback_ready,
            "may_propose": self.may_propose,
            "may_apply": self.may_apply,
            "execution_allowed": self.execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "production_deployment_allowed": self.production_deployment_allowed,
            "public_exposure_allowed": self.public_exposure_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_ai_orchestration_read_model() -> AIOrchestrationReadModel:
    proposal = build_default_proposal_staging_contract()
    provenance = build_default_model_provenance_contract()
    budget = build_default_finops_budget_contract()
    feedback = build_default_feedback_engine_contract()
    policy = build_default_ai_orchestration_policy()

    return AIOrchestrationReadModel(
        read_model_id="ai_orchestration_read_model_v1",
        proposal_staging=proposal,
        model_provenance=provenance,
        finops_budget=budget,
        feedback_engine=feedback,
        orchestration_policy=policy,
        proposal_ready=proposal.proposal_only,
        provenance_ready=provenance.provenance_ready,
        budget_guard_ready=budget.budget_guard_ready,
        feedback_ready=feedback.feedback_ready,
        may_propose=policy.may_propose,
        may_apply=policy.may_apply,
        execution_allowed=False,
        runtime_mutation_allowed=False,
        production_deployment_allowed=False,
        public_exposure_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_orchestration_read_model_dashboard_safe",
            "proposal_provenance_budget_feedback_visible",
            "ai_may_propose_not_apply",
            "execution_blocked",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
