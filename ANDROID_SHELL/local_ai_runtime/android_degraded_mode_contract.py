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
class AndroidDegradedModeContract:
    contract_id: str
    platform: str
    degraded_mode_available: bool
    degraded_mode_is_app_safe: bool
    degraded_mode_text_intent_only: bool
    degraded_mode_can_answer_local_safe_help: bool
    degraded_mode_can_execute_core_actions: bool
    degraded_mode_can_write_memory: bool
    degraded_mode_can_control_phone: bool
    degraded_mode_can_control_pc: bool
    degraded_mode_can_bypass_approval: bool
    degraded_mode_requires_server_resync: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(self, "platform", _ensure_non_empty(self.platform, "platform"))
        if self.platform != "android":
            raise ValueError("platform must be android")
        for field_name in (
            "degraded_mode_available",
            "degraded_mode_is_app_safe",
            "degraded_mode_text_intent_only",
            "degraded_mode_can_answer_local_safe_help",
            "degraded_mode_requires_server_resync",
            "proposal_only",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "degraded_mode_can_execute_core_actions",
            "degraded_mode_can_write_memory",
            "degraded_mode_can_control_phone",
            "degraded_mode_can_control_pc",
            "degraded_mode_can_bypass_approval",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "platform": self.platform,
            "degraded_mode_available": self.degraded_mode_available,
            "degraded_mode_is_app_safe": self.degraded_mode_is_app_safe,
            "degraded_mode_text_intent_only": self.degraded_mode_text_intent_only,
            "degraded_mode_can_answer_local_safe_help": self.degraded_mode_can_answer_local_safe_help,
            "degraded_mode_can_execute_core_actions": self.degraded_mode_can_execute_core_actions,
            "degraded_mode_can_write_memory": self.degraded_mode_can_write_memory,
            "degraded_mode_can_control_phone": self.degraded_mode_can_control_phone,
            "degraded_mode_can_control_pc": self.degraded_mode_can_control_pc,
            "degraded_mode_can_bypass_approval": self.degraded_mode_can_bypass_approval,
            "degraded_mode_requires_server_resync": self.degraded_mode_requires_server_resync,
            "proposal_only": self.proposal_only,
        }


def build_android_degraded_mode_contract() -> AndroidDegradedModeContract:
    return AndroidDegradedModeContract(
        contract_id="android_degraded_mode_contract_v0_1",
        platform="android",
        degraded_mode_available=True,
        degraded_mode_is_app_safe=True,
        degraded_mode_text_intent_only=True,
        degraded_mode_can_answer_local_safe_help=True,
        degraded_mode_can_execute_core_actions=False,
        degraded_mode_can_write_memory=False,
        degraded_mode_can_control_phone=False,
        degraded_mode_can_control_pc=False,
        degraded_mode_can_bypass_approval=False,
        degraded_mode_requires_server_resync=True,
        proposal_only=True,
    )
