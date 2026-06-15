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
class AndroidLocalAiAdapterContract:
    contract_id: str
    platform: str
    local_ai_adapter_contract: bool
    junior_model_role: str
    senior_model_role: str
    app_safe_only: bool
    text_intent_only: bool
    local_model_runtime_supported: bool
    local_model_runtime_started: bool
    model_download_allowed: bool
    model_file_required: bool
    local_inference_started: bool
    local_inference_probe_allowed: bool
    canonical_truth_allowed: bool
    canonical_write_allowed: bool
    canonical_memory_write_allowed: bool
    core_action_execution_allowed: bool
    shell_execution_allowed: bool
    pc_control_allowed: bool
    direct_mobile_control_allowed: bool
    phone_control_allowed: bool
    deployment_allowed: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(self, "platform", _ensure_non_empty(self.platform, "platform"))
        object.__setattr__(self, "junior_model_role", _ensure_non_empty(self.junior_model_role, "junior_model_role"))
        object.__setattr__(self, "senior_model_role", _ensure_non_empty(self.senior_model_role, "senior_model_role"))
        if self.platform != "android":
            raise ValueError("platform must be android")
        if self.junior_model_role != "mobile_junior":
            raise ValueError("junior_model_role must be mobile_junior")
        if self.senior_model_role != "server_jARVIS_senior":
            raise ValueError("senior_model_role must be server_jARVIS_senior")
        for field_name in (
            "local_ai_adapter_contract",
            "app_safe_only",
            "text_intent_only",
            "local_model_runtime_supported",
            "proposal_only",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "local_model_runtime_started",
            "model_download_allowed",
            "model_file_required",
            "local_inference_started",
            "local_inference_probe_allowed",
            "canonical_truth_allowed",
            "canonical_write_allowed",
            "canonical_memory_write_allowed",
            "core_action_execution_allowed",
            "shell_execution_allowed",
            "pc_control_allowed",
            "direct_mobile_control_allowed",
            "phone_control_allowed",
            "deployment_allowed",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "platform": self.platform,
            "local_ai_adapter_contract": self.local_ai_adapter_contract,
            "junior_model_role": self.junior_model_role,
            "senior_model_role": self.senior_model_role,
            "app_safe_only": self.app_safe_only,
            "text_intent_only": self.text_intent_only,
            "local_model_runtime_supported": self.local_model_runtime_supported,
            "local_model_runtime_started": self.local_model_runtime_started,
            "model_download_allowed": self.model_download_allowed,
            "model_file_required": self.model_file_required,
            "local_inference_started": self.local_inference_started,
            "local_inference_probe_allowed": self.local_inference_probe_allowed,
            "canonical_truth_allowed": self.canonical_truth_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "core_action_execution_allowed": self.core_action_execution_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "phone_control_allowed": self.phone_control_allowed,
            "deployment_allowed": self.deployment_allowed,
            "proposal_only": self.proposal_only,
        }


def build_android_local_ai_adapter_contract() -> AndroidLocalAiAdapterContract:
    return AndroidLocalAiAdapterContract(
        contract_id="android_local_ai_adapter_contract_v0_1",
        platform="android",
        local_ai_adapter_contract=True,
        junior_model_role="mobile_junior",
        senior_model_role="server_jARVIS_senior",
        app_safe_only=True,
        text_intent_only=True,
        local_model_runtime_supported=True,
        local_model_runtime_started=False,
        model_download_allowed=False,
        model_file_required=False,
        local_inference_started=False,
        local_inference_probe_allowed=False,
        canonical_truth_allowed=False,
        canonical_write_allowed=False,
        canonical_memory_write_allowed=False,
        core_action_execution_allowed=False,
        shell_execution_allowed=False,
        pc_control_allowed=False,
        direct_mobile_control_allowed=False,
        phone_control_allowed=False,
        deployment_allowed=False,
        proposal_only=True,
    )
