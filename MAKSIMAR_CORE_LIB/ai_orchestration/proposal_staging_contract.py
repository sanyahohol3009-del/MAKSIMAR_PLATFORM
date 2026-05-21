from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ProposalStagingContract:
    proposal_id: str
    source_request_id: str
    proposal_payload_ref: str
    proposal_only: bool
    owner_approval_required: bool
    apply_allowed: bool
    auto_apply_allowed: bool
    execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("proposal_id", self.proposal_id)
        _validate_non_empty("source_request_id", self.source_request_id)
        _validate_non_empty("proposal_payload_ref", self.proposal_payload_ref)
        _validate_true("proposal_only", self.proposal_only)
        _validate_true("owner_approval_required", self.owner_approval_required)
        _validate_false("apply_allowed", self.apply_allowed)
        _validate_false("auto_apply_allowed", self.auto_apply_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "source_request_id": self.source_request_id,
            "proposal_payload_ref": self.proposal_payload_ref,
            "proposal_only": self.proposal_only,
            "owner_approval_required": self.owner_approval_required,
            "apply_allowed": self.apply_allowed,
            "auto_apply_allowed": self.auto_apply_allowed,
            "execution_allowed": self.execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_proposal_staging_contract() -> ProposalStagingContract:
    return ProposalStagingContract(
        proposal_id="ai_orchestration_proposal_v1",
        source_request_id="model_request_v1",
        proposal_payload_ref="proposal_payload_ref",
        proposal_only=True,
        owner_approval_required=True,
        apply_allowed=False,
        auto_apply_allowed=False,
        execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "ai_may_only_propose",
            "owner_approval_required",
            "apply_blocked",
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
