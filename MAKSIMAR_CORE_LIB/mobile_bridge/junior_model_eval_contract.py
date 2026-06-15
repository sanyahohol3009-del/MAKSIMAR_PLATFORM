from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class JuniorModelEvalContract:
    contract_id: str
    eval_required_before_runtime_enable: bool
    eval_is_policy_check_only: bool
    eval_rationale_required: bool
    eval_rationale_must_be_human_readable: bool
    eval_may_not_enable_runtime: bool
    eval_may_not_download_model: bool
    eval_may_not_grant_core_actions: bool
    eval_may_not_grant_canonical_write: bool
    server_approval_required_for_runtime: bool
    owner_approval_required: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        _require_true(
            self.eval_required_before_runtime_enable,
            "eval_required_before_runtime_enable",
        )
        _require_true(self.eval_is_policy_check_only, "eval_is_policy_check_only")
        _require_true(self.eval_rationale_required, "eval_rationale_required")
        _require_true(
            self.eval_rationale_must_be_human_readable,
            "eval_rationale_must_be_human_readable",
        )
        _require_true(self.eval_may_not_enable_runtime, "eval_may_not_enable_runtime")
        _require_true(self.eval_may_not_download_model, "eval_may_not_download_model")
        _require_true(
            self.eval_may_not_grant_core_actions,
            "eval_may_not_grant_core_actions",
        )
        _require_true(
            self.eval_may_not_grant_canonical_write,
            "eval_may_not_grant_canonical_write",
        )
        _require_true(
            self.server_approval_required_for_runtime,
            "server_approval_required_for_runtime",
        )
        _require_true(self.owner_approval_required, "owner_approval_required")
        _require_true(self.proposal_only, "proposal_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "eval_required_before_runtime_enable": self.eval_required_before_runtime_enable,
            "eval_is_policy_check_only": self.eval_is_policy_check_only,
            "eval_rationale_required": self.eval_rationale_required,
            "eval_rationale_must_be_human_readable": self.eval_rationale_must_be_human_readable,
            "eval_may_not_enable_runtime": self.eval_may_not_enable_runtime,
            "eval_may_not_download_model": self.eval_may_not_download_model,
            "eval_may_not_grant_core_actions": self.eval_may_not_grant_core_actions,
            "eval_may_not_grant_canonical_write": self.eval_may_not_grant_canonical_write,
            "server_approval_required_for_runtime": self.server_approval_required_for_runtime,
            "owner_approval_required": self.owner_approval_required,
            "proposal_only": self.proposal_only,
        }


def build_junior_model_eval_contract() -> JuniorModelEvalContract:
    return JuniorModelEvalContract(
        contract_id="junior_model_eval_contract_v0_1",
        eval_required_before_runtime_enable=True,
        eval_is_policy_check_only=True,
        eval_rationale_required=True,
        eval_rationale_must_be_human_readable=True,
        eval_may_not_enable_runtime=True,
        eval_may_not_download_model=True,
        eval_may_not_grant_core_actions=True,
        eval_may_not_grant_canonical_write=True,
        server_approval_required_for_runtime=True,
        owner_approval_required=True,
        proposal_only=True,
    )
