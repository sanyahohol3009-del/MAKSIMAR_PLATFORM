from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    ProposalStagingContract,
    build_default_proposal_staging_contract,
)


@dataclass(frozen=True, slots=True)
class ProposalStagingServiceReadModel:
    service_id: str
    proposal_contract: ProposalStagingContract
    proposal_only: bool
    apply_allowed: bool
    auto_apply_allowed: bool
    execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("service_id", self.service_id)
        if not isinstance(self.proposal_contract, ProposalStagingContract):
            raise TypeError("proposal_contract must be ProposalStagingContract")
        _validate_true("proposal_only", self.proposal_only)
        _validate_false("apply_allowed", self.apply_allowed)
        _validate_false("auto_apply_allowed", self.auto_apply_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "proposal_contract": self.proposal_contract.to_dict(),
            "proposal_only": self.proposal_only,
            "apply_allowed": self.apply_allowed,
            "auto_apply_allowed": self.auto_apply_allowed,
            "execution_allowed": self.execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_proposal_staging_service_read_model() -> ProposalStagingServiceReadModel:
    return ProposalStagingServiceReadModel(
        service_id="proposal_staging_service_v1",
        proposal_contract=build_default_proposal_staging_contract(),
        proposal_only=True,
        apply_allowed=False,
        auto_apply_allowed=False,
        execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "proposal_staging_service_read_model_only",
            "ai_may_propose_not_apply",
            "runtime_mutation_blocked",
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
