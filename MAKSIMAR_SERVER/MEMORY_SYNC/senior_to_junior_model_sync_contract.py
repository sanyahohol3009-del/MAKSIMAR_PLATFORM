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
class SeniorToJuniorModelSyncContract:
    contract_id: str
    sync_contract_enabled: bool
    sync_direction: str
    server_jARVIS_is_senior: bool
    mobile_junior_is_subordinate: bool
    sync_payload_is_app_safe: bool
    sync_payload_is_read_only: bool
    sync_payload_is_intent_context_only: bool
    canonical_core_export_allowed: bool
    canonical_memory_write_allowed: bool
    junior_canonical_write_allowed: bool
    junior_core_action_execution_allowed: bool
    junior_shell_execution_allowed: bool
    junior_pc_control_allowed: bool
    junior_direct_phone_control_allowed: bool
    model_download_allowed: bool
    local_inference_started: bool
    windows_voice_edge_parked: bool
    push_to_talk_stt_live_parked: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(self, "sync_direction", _ensure_non_empty(self.sync_direction, "sync_direction"))
        if self.sync_direction != "server_senior_to_mobile_junior":
            raise ValueError("sync_direction must be server_senior_to_mobile_junior")
        for field_name in (
            "sync_contract_enabled",
            "server_jARVIS_is_senior",
            "mobile_junior_is_subordinate",
            "sync_payload_is_app_safe",
            "sync_payload_is_read_only",
            "sync_payload_is_intent_context_only",
            "windows_voice_edge_parked",
            "push_to_talk_stt_live_parked",
            "proposal_only",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "canonical_core_export_allowed",
            "canonical_memory_write_allowed",
            "junior_canonical_write_allowed",
            "junior_core_action_execution_allowed",
            "junior_shell_execution_allowed",
            "junior_pc_control_allowed",
            "junior_direct_phone_control_allowed",
            "model_download_allowed",
            "local_inference_started",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "sync_contract_enabled": self.sync_contract_enabled,
            "sync_direction": self.sync_direction,
            "server_jARVIS_is_senior": self.server_jARVIS_is_senior,
            "mobile_junior_is_subordinate": self.mobile_junior_is_subordinate,
            "sync_payload_is_app_safe": self.sync_payload_is_app_safe,
            "sync_payload_is_read_only": self.sync_payload_is_read_only,
            "sync_payload_is_intent_context_only": self.sync_payload_is_intent_context_only,
            "canonical_core_export_allowed": self.canonical_core_export_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "junior_canonical_write_allowed": self.junior_canonical_write_allowed,
            "junior_core_action_execution_allowed": self.junior_core_action_execution_allowed,
            "junior_shell_execution_allowed": self.junior_shell_execution_allowed,
            "junior_pc_control_allowed": self.junior_pc_control_allowed,
            "junior_direct_phone_control_allowed": self.junior_direct_phone_control_allowed,
            "model_download_allowed": self.model_download_allowed,
            "local_inference_started": self.local_inference_started,
            "windows_voice_edge_parked": self.windows_voice_edge_parked,
            "push_to_talk_stt_live_parked": self.push_to_talk_stt_live_parked,
            "proposal_only": self.proposal_only,
        }


def build_senior_to_junior_model_sync_contract() -> SeniorToJuniorModelSyncContract:
    return SeniorToJuniorModelSyncContract(
        contract_id="senior_to_junior_model_sync_contract_v0_1",
        sync_contract_enabled=True,
        sync_direction="server_senior_to_mobile_junior",
        server_jARVIS_is_senior=True,
        mobile_junior_is_subordinate=True,
        sync_payload_is_app_safe=True,
        sync_payload_is_read_only=True,
        sync_payload_is_intent_context_only=True,
        canonical_core_export_allowed=False,
        canonical_memory_write_allowed=False,
        junior_canonical_write_allowed=False,
        junior_core_action_execution_allowed=False,
        junior_shell_execution_allowed=False,
        junior_pc_control_allowed=False,
        junior_direct_phone_control_allowed=False,
        model_download_allowed=False,
        local_inference_started=False,
        windows_voice_edge_parked=True,
        push_to_talk_stt_live_parked=True,
        proposal_only=True,
    )
