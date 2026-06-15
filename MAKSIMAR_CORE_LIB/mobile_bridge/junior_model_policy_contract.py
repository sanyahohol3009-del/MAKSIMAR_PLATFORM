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
class JuniorModelPolicyContract:
    contract_id: str
    junior_model_role: str
    senior_model_role: str
    junior_model_allowed: bool
    junior_model_size_limit_default_enabled: bool
    junior_model_size_limit_mb: int
    app_safe_only: bool
    text_intent_only: bool
    local_inference_allowed_as_future_runtime: bool
    local_inference_started: bool
    model_download_allowed: bool
    canonical_truth_allowed: bool
    canonical_memory_write_allowed: bool
    core_action_execution_allowed: bool
    shell_execution_allowed: bool
    pc_control_allowed: bool
    direct_mobile_control_allowed: bool
    server_mutation_allowed: bool
    deployment_allowed: bool
    owner_approval_bypass_allowed: bool
    server_remains_canonical_authority: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(
            self,
            "junior_model_role",
            _ensure_non_empty(self.junior_model_role, "junior_model_role"),
        )
        object.__setattr__(
            self,
            "senior_model_role",
            _ensure_non_empty(self.senior_model_role, "senior_model_role"),
        )
        if self.junior_model_role != "mobile_junior":
            raise ValueError("junior_model_role must be mobile_junior")
        if self.senior_model_role != "server_jARVIS_senior":
            raise ValueError("senior_model_role must be server_jARVIS_senior")
        if not isinstance(self.junior_model_size_limit_mb, int) or self.junior_model_size_limit_mb <= 0:
            raise ValueError("junior_model_size_limit_mb must be a positive integer")
        if self.junior_model_size_limit_mb > 1024:
            raise ValueError("junior_model_size_limit_mb must remain conservative")
        _require_true(self.junior_model_allowed, "junior_model_allowed")
        _require_true(
            self.junior_model_size_limit_default_enabled,
            "junior_model_size_limit_default_enabled",
        )
        _require_true(self.app_safe_only, "app_safe_only")
        _require_true(self.text_intent_only, "text_intent_only")
        _require_true(
            self.local_inference_allowed_as_future_runtime,
            "local_inference_allowed_as_future_runtime",
        )
        _require_false(self.local_inference_started, "local_inference_started")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.canonical_truth_allowed, "canonical_truth_allowed")
        _require_false(
            self.canonical_memory_write_allowed,
            "canonical_memory_write_allowed",
        )
        _require_false(
            self.core_action_execution_allowed,
            "core_action_execution_allowed",
        )
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.server_mutation_allowed, "server_mutation_allowed")
        _require_false(self.deployment_allowed, "deployment_allowed")
        _require_false(
            self.owner_approval_bypass_allowed,
            "owner_approval_bypass_allowed",
        )
        _require_true(
            self.server_remains_canonical_authority,
            "server_remains_canonical_authority",
        )
        _require_true(self.proposal_only, "proposal_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "junior_model_role": self.junior_model_role,
            "senior_model_role": self.senior_model_role,
            "junior_model_allowed": self.junior_model_allowed,
            "junior_model_size_limit_default_enabled": (
                self.junior_model_size_limit_default_enabled
            ),
            "junior_model_size_limit_mb": self.junior_model_size_limit_mb,
            "app_safe_only": self.app_safe_only,
            "text_intent_only": self.text_intent_only,
            "local_inference_allowed_as_future_runtime": (
                self.local_inference_allowed_as_future_runtime
            ),
            "local_inference_started": self.local_inference_started,
            "model_download_allowed": self.model_download_allowed,
            "canonical_truth_allowed": self.canonical_truth_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "core_action_execution_allowed": self.core_action_execution_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "server_mutation_allowed": self.server_mutation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "owner_approval_bypass_allowed": self.owner_approval_bypass_allowed,
            "server_remains_canonical_authority": self.server_remains_canonical_authority,
            "proposal_only": self.proposal_only,
        }


def build_junior_model_policy_contract() -> JuniorModelPolicyContract:
    return JuniorModelPolicyContract(
        contract_id="junior_model_policy_contract_v0_1",
        junior_model_role="mobile_junior",
        senior_model_role="server_jARVIS_senior",
        junior_model_allowed=True,
        junior_model_size_limit_default_enabled=True,
        junior_model_size_limit_mb=512,
        app_safe_only=True,
        text_intent_only=True,
        local_inference_allowed_as_future_runtime=True,
        local_inference_started=False,
        model_download_allowed=False,
        canonical_truth_allowed=False,
        canonical_memory_write_allowed=False,
        core_action_execution_allowed=False,
        shell_execution_allowed=False,
        pc_control_allowed=False,
        direct_mobile_control_allowed=False,
        server_mutation_allowed=False,
        deployment_allowed=False,
        owner_approval_bypass_allowed=False,
        server_remains_canonical_authority=True,
        proposal_only=True,
    )
