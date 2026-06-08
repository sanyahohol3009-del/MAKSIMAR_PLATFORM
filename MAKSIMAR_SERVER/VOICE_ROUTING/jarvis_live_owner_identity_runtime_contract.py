from __future__ import annotations

from dataclasses import dataclass
from typing import Any


OWNER_DETECTION_KEYWORDS: tuple[str, ...] = ("александр", "джарвис", "jarvis")


@dataclass(frozen=True, slots=True)
class JarvisLiveOwnerIdentityRuntimeContract:
    contract_id: str = "jarvis_live_owner_identity_runtime_v0_1"
    owner_display_name: str = "Александр"
    owner_detection_keywords: tuple[str, ...] = OWNER_DETECTION_KEYWORDS
    owner_phrase_detection_required: bool = True
    owner_visible_state_required: bool = True
    unknown_speaker_no_action_required: bool = True
    owner_command_required_before_actions: bool = True
    biometric_auth_claimed: bool = False
    speaker_verification_claimed: bool = False
    unknown_speaker_action_allowed: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.owner_display_name != "Александр":
            raise ValueError("owner_display_name must be Александр")
        if self.owner_detection_keywords != OWNER_DETECTION_KEYWORDS:
            raise ValueError("owner_detection_keywords must remain canonical")
        for keyword in self.owner_detection_keywords:
            _require_non_empty(keyword, "owner_detection_keywords")
        for field_name in (
            "owner_phrase_detection_required",
            "owner_visible_state_required",
            "unknown_speaker_no_action_required",
            "owner_command_required_before_actions",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "biometric_auth_claimed",
            "speaker_verification_claimed",
            "unknown_speaker_action_allowed",
            "pc_control_allowed",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "owner_display_name": self.owner_display_name,
            "owner_detection_keywords": self.owner_detection_keywords,
            "owner_phrase_detection_required": self.owner_phrase_detection_required,
            "owner_visible_state_required": self.owner_visible_state_required,
            "unknown_speaker_no_action_required": self.unknown_speaker_no_action_required,
            "owner_command_required_before_actions": self.owner_command_required_before_actions,
            "biometric_auth_claimed": self.biometric_auth_claimed,
            "speaker_verification_claimed": self.speaker_verification_claimed,
            "unknown_speaker_action_allowed": self.unknown_speaker_action_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


def build_jarvis_live_owner_identity_runtime_contract() -> (
    JarvisLiveOwnerIdentityRuntimeContract
):
    return JarvisLiveOwnerIdentityRuntimeContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")
