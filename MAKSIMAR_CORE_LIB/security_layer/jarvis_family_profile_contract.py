from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED_PROFILE_TYPES = {"owner", "trusted_family", "child"}


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_profile_type(value: str) -> str:
    normalized = _require_non_empty(value, "profile_type")
    if normalized not in _ALLOWED_PROFILE_TYPES:
        raise ValueError(f"profile_type must be one of {tuple(sorted(_ALLOWED_PROFILE_TYPES))!r}")
    return normalized


@dataclass(frozen=True, slots=True)
class JarvisFamilyProfile:
    profile_id: str
    display_name: str
    profile_type: str
    can_request_project_read: bool
    can_request_pc_action: bool
    pc_action_requires_approval: bool
    can_request_memory_read: bool
    can_request_canonical_write_without_approval: bool
    can_request_git_write: bool
    can_request_install_download: bool
    can_request_destructive_actions: bool
    can_request_external_send_payment: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "profile_id", _require_non_empty(self.profile_id, "profile_id"))
        object.__setattr__(self, "display_name", _require_non_empty(self.display_name, "display_name"))
        object.__setattr__(self, "profile_type", _require_profile_type(self.profile_type))
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.profile_type == "owner":
            if self.can_request_project_read is not True or self.can_request_memory_read is not True:
                raise ValueError("owner profile must allow project and memory read")
            if self.can_request_pc_action is not True or self.pc_action_requires_approval is not True:
                raise ValueError("owner profile must allow pc action with approval")
        if self.profile_type == "trusted_family":
            if self.can_request_git_write or self.can_request_install_download or self.can_request_destructive_actions:
                raise ValueError("trusted_family profile must not allow git write/install/destructive actions")
        if self.profile_type == "child":
            if self.can_request_pc_action or self.can_request_destructive_actions or self.can_request_external_send_payment:
                raise ValueError("child profile must not allow pc action/destructive/send-payment actions")
            if self.can_request_canonical_write_without_approval:
                raise ValueError("child profile must not allow canonical writes")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "display_name": self.display_name,
            "profile_type": self.profile_type,
            "can_request_project_read": self.can_request_project_read,
            "can_request_pc_action": self.can_request_pc_action,
            "pc_action_requires_approval": self.pc_action_requires_approval,
            "can_request_memory_read": self.can_request_memory_read,
            "can_request_canonical_write_without_approval": self.can_request_canonical_write_without_approval,
            "can_request_git_write": self.can_request_git_write,
            "can_request_install_download": self.can_request_install_download,
            "can_request_destructive_actions": self.can_request_destructive_actions,
            "can_request_external_send_payment": self.can_request_external_send_payment,
            "reason_codes": self.reason_codes,
        }


def build_owner_profile() -> JarvisFamilyProfile:
    return JarvisFamilyProfile(
        profile_id="owner_profile_aleksandr_v1",
        display_name="Александр",
        profile_type="owner",
        can_request_project_read=True,
        can_request_pc_action=True,
        pc_action_requires_approval=True,
        can_request_memory_read=True,
        can_request_canonical_write_without_approval=False,
        can_request_git_write=False,
        can_request_install_download=False,
        can_request_destructive_actions=False,
        can_request_external_send_payment=False,
        reason_codes=("owner_operator", "approval_gate_required", "read_write_boundaries_preserved"),
    )


def build_trusted_family_profile() -> JarvisFamilyProfile:
    return JarvisFamilyProfile(
        profile_id="trusted_family_profile_yulia_v1",
        display_name="Юля",
        profile_type="trusted_family",
        can_request_project_read=True,
        can_request_pc_action=True,
        pc_action_requires_approval=True,
        can_request_memory_read=True,
        can_request_canonical_write_without_approval=False,
        can_request_git_write=False,
        can_request_install_download=False,
        can_request_destructive_actions=False,
        can_request_external_send_payment=False,
        reason_codes=("trusted_family", "safe_household_help_only", "approval_gate_required"),
    )


def build_child_profile(*, child_name: str) -> JarvisFamilyProfile:
    normalized_name = _require_non_empty(child_name, "child_name")
    return JarvisFamilyProfile(
        profile_id=f"child_profile_{normalized_name.casefold()}_v1",
        display_name=normalized_name,
        profile_type="child",
        can_request_project_read=True,
        can_request_pc_action=False,
        pc_action_requires_approval=True,
        can_request_memory_read=True,
        can_request_canonical_write_without_approval=False,
        can_request_git_write=False,
        can_request_install_download=False,
        can_request_destructive_actions=False,
        can_request_external_send_payment=False,
        reason_codes=("child_profile", "learning_game_coach_only", "no_direct_pc_control"),
    )
