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
class LocalLlmRuntimeContract:
    contract_id: str
    junior_model_role: str
    senior_model_role: str
    local_llm_runtime_allowed: bool
    local_llm_runtime_started: bool
    model_download_allowed: bool
    model_file_present_required: bool
    local_inference_probe_allowed: bool
    canonical_truth_allowed: bool
    canonical_memory_write_allowed: bool
    core_action_execution_allowed: bool
    shell_execution_allowed: bool
    pc_control_allowed: bool
    direct_mobile_control_allowed: bool
    server_mutation_allowed: bool
    deployment_allowed: bool
    network_sync_authority: bool
    proposal_only: bool
    app_safe_only: bool
    text_intent_only: bool
    senior_awareness_required: bool
    junior_awareness_required: bool

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

        _require_true(self.local_llm_runtime_allowed, "local_llm_runtime_allowed")
        _require_false(self.local_llm_runtime_started, "local_llm_runtime_started")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.model_file_present_required, "model_file_present_required")
        _require_false(self.local_inference_probe_allowed, "local_inference_probe_allowed")
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
        _require_false(self.network_sync_authority, "network_sync_authority")
        _require_true(self.proposal_only, "proposal_only")
        _require_true(self.app_safe_only, "app_safe_only")
        _require_true(self.text_intent_only, "text_intent_only")
        _require_true(self.senior_awareness_required, "senior_awareness_required")
        _require_true(self.junior_awareness_required, "junior_awareness_required")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "junior_model_role": self.junior_model_role,
            "senior_model_role": self.senior_model_role,
            "local_llm_runtime_allowed": self.local_llm_runtime_allowed,
            "local_llm_runtime_started": self.local_llm_runtime_started,
            "model_download_allowed": self.model_download_allowed,
            "model_file_present_required": self.model_file_present_required,
            "local_inference_probe_allowed": self.local_inference_probe_allowed,
            "canonical_truth_allowed": self.canonical_truth_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "core_action_execution_allowed": self.core_action_execution_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "server_mutation_allowed": self.server_mutation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "network_sync_authority": self.network_sync_authority,
            "proposal_only": self.proposal_only,
            "app_safe_only": self.app_safe_only,
            "text_intent_only": self.text_intent_only,
            "senior_awareness_required": self.senior_awareness_required,
            "junior_awareness_required": self.junior_awareness_required,
        }


def build_local_llm_runtime_contract() -> LocalLlmRuntimeContract:
    return LocalLlmRuntimeContract(
        contract_id="local_llm_runtime_contract_v0_1",
        junior_model_role="mobile_junior",
        senior_model_role="server_jARVIS_senior",
        local_llm_runtime_allowed=True,
        local_llm_runtime_started=False,
        model_download_allowed=False,
        model_file_present_required=False,
        local_inference_probe_allowed=False,
        canonical_truth_allowed=False,
        canonical_memory_write_allowed=False,
        core_action_execution_allowed=False,
        shell_execution_allowed=False,
        pc_control_allowed=False,
        direct_mobile_control_allowed=False,
        server_mutation_allowed=False,
        deployment_allowed=False,
        network_sync_authority=False,
        proposal_only=True,
        app_safe_only=True,
        text_intent_only=True,
        senior_awareness_required=True,
        junior_awareness_required=True,
    )
