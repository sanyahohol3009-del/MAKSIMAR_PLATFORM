from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ALLOWED_JARVIS_ACTION_CANDIDATES: tuple[str, ...] = (
    "open_youtube",
    "open_browser",
    "open_project_status",
    "read_test_status",
    "volume_up",
    "volume_down",
    "pause_media",
    "resume_media",
)

FORBIDDEN_JARVIS_ACTIONS: tuple[str, ...] = (
    "raw_shell",
    "delete_files",
    "edit_code",
    "git_commit",
    "git_push",
    "install_program",
    "open_network_port",
)


@dataclass(frozen=True, slots=True)
class JarvisAllowedActionCandidate:
    action_id: str
    owner_command_required: bool = True
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True
    allowlist_required: bool = True
    execution_enabled: bool = False
    runtime_start_allowed: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        assert_action_not_forbidden(self.action_id)
        _require_member(self.action_id, ALLOWED_JARVIS_ACTION_CANDIDATES, "action_id")
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")
        _require_true(self.allowlist_required, "allowlist_required")
        _require_false(self.execution_enabled, "execution_enabled")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "owner_command_required": self.owner_command_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
            "allowlist_required": self.allowlist_required,
            "execution_enabled": self.execution_enabled,
            "runtime_start_allowed": self.runtime_start_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


@dataclass(frozen=True, slots=True)
class JarvisActionAllowlistContract:
    allowed_action_candidates: tuple[JarvisAllowedActionCandidate, ...]
    forbidden_actions: tuple[str, ...]

    def __post_init__(self) -> None:
        if tuple(action.action_id for action in self.allowed_action_candidates) != (
            ALLOWED_JARVIS_ACTION_CANDIDATES
        ):
            raise ValueError("allowed_action_candidates must match the canonical action set")
        if self.forbidden_actions != FORBIDDEN_JARVIS_ACTIONS:
            raise ValueError("forbidden_actions must match the canonical forbidden action set")
        for action_id in self.forbidden_actions:
            _require_non_empty(action_id, "forbidden_actions")

    def is_action_allowed_candidate(self, action_id: str) -> bool:
        assert_action_not_forbidden(action_id)
        return action_id in ALLOWED_JARVIS_ACTION_CANDIDATES

    def to_read_model(self) -> dict[str, Any]:
        return {
            "allowed_action_candidates": tuple(
                action.to_read_model() for action in self.allowed_action_candidates
            ),
            "allowed_action_ids": tuple(
                action.action_id for action in self.allowed_action_candidates
            ),
            "forbidden_actions": self.forbidden_actions,
            "execution_enabled": False,
            "runtime_start_allowed": False,
            "pc_control_allowed": False,
        }


def build_jarvis_action_allowlist_contract() -> JarvisActionAllowlistContract:
    return JarvisActionAllowlistContract(
        allowed_action_candidates=tuple(
            JarvisAllowedActionCandidate(action_id=action_id)
            for action_id in ALLOWED_JARVIS_ACTION_CANDIDATES
        ),
        forbidden_actions=FORBIDDEN_JARVIS_ACTIONS,
    )


def is_action_allowed_candidate(action_id: str) -> bool:
    return build_jarvis_action_allowlist_contract().is_action_allowed_candidate(action_id)


def assert_action_not_forbidden(action_id: str) -> None:
    _require_non_empty(action_id, "action_id")
    if action_id in FORBIDDEN_JARVIS_ACTIONS:
        raise ValueError(f"forbidden JARVIS action rejected: {action_id}")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_member(value: str, allowed_values: tuple[str, ...], field_name: str) -> None:
    _require_non_empty(value, field_name)
    if value not in allowed_values:
        raise ValueError(f"{field_name} has unsupported value: {value}")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain required")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

