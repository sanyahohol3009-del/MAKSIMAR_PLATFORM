from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class LiveSandboxRuntimePolicy:
    policy_id: str
    controlled_download_allowed: bool = True
    actual_download_started: bool = False
    runtime_start_allowed: bool = False
    model_execution_allowed: bool = False
    voice_runtime_allowed: bool = False
    screen_runtime_allowed: bool = False
    pc_control_allowed: bool = False
    dashboard_execution_allowed: bool = False
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True
    runtime_root_required: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.policy_id, "policy_id")
        _require_true(self.controlled_download_allowed, "controlled_download_allowed")
        _require_false(self.actual_download_started, "actual_download_started")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.model_execution_allowed, "model_execution_allowed")
        _require_false(self.voice_runtime_allowed, "voice_runtime_allowed")
        _require_false(self.screen_runtime_allowed, "screen_runtime_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")
        _require_true(self.runtime_root_required, "runtime_root_required")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "controlled_download_allowed": self.controlled_download_allowed,
            "actual_download_started": self.actual_download_started,
            "runtime_start_allowed": self.runtime_start_allowed,
            "model_execution_allowed": self.model_execution_allowed,
            "voice_runtime_allowed": self.voice_runtime_allowed,
            "screen_runtime_allowed": self.screen_runtime_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
            "runtime_root_required": self.runtime_root_required,
        }


def build_live_sandbox_runtime_policy() -> LiveSandboxRuntimePolicy:
    return LiveSandboxRuntimePolicy(policy_id="live_sandbox_runtime_policy_v0_1")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

