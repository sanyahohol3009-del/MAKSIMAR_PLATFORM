from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisCommandSecurityBindingContract:
    binding_id: str
    explicit_owner_command_required: bool = True
    owner_voice_or_text_confirmation_required: bool = True
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True
    rollback_or_stop_required: bool = True
    allowlist_required: bool = True
    direct_execution_allowed: bool = False
    shell_allowed: bool = False
    browser_control_allowed: bool = False
    app_control_allowed: bool = False
    mouse_keyboard_control_allowed: bool = False
    network_port_open_allowed: bool = False
    file_delete_allowed: bool = False
    code_edit_allowed: bool = False
    git_operation_allowed: bool = False
    model_download_allowed: bool = False
    runtime_start_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.binding_id, "binding_id")
        _require_true(self.explicit_owner_command_required, "explicit_owner_command_required")
        _require_true(
            self.owner_voice_or_text_confirmation_required,
            "owner_voice_or_text_confirmation_required",
        )
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")
        _require_true(self.rollback_or_stop_required, "rollback_or_stop_required")
        _require_true(self.allowlist_required, "allowlist_required")
        _require_false(self.direct_execution_allowed, "direct_execution_allowed")
        _require_false(self.shell_allowed, "shell_allowed")
        _require_false(self.browser_control_allowed, "browser_control_allowed")
        _require_false(self.app_control_allowed, "app_control_allowed")
        _require_false(self.mouse_keyboard_control_allowed, "mouse_keyboard_control_allowed")
        _require_false(self.network_port_open_allowed, "network_port_open_allowed")
        _require_false(self.file_delete_allowed, "file_delete_allowed")
        _require_false(self.code_edit_allowed, "code_edit_allowed")
        _require_false(self.git_operation_allowed, "git_operation_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "explicit_owner_command_required": self.explicit_owner_command_required,
            "owner_voice_or_text_confirmation_required": (
                self.owner_voice_or_text_confirmation_required
            ),
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
            "rollback_or_stop_required": self.rollback_or_stop_required,
            "allowlist_required": self.allowlist_required,
            "direct_execution_allowed": self.direct_execution_allowed,
            "shell_allowed": self.shell_allowed,
            "browser_control_allowed": self.browser_control_allowed,
            "app_control_allowed": self.app_control_allowed,
            "mouse_keyboard_control_allowed": self.mouse_keyboard_control_allowed,
            "network_port_open_allowed": self.network_port_open_allowed,
            "file_delete_allowed": self.file_delete_allowed,
            "code_edit_allowed": self.code_edit_allowed,
            "git_operation_allowed": self.git_operation_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_jarvis_command_security_binding_contract() -> (
    JarvisCommandSecurityBindingContract
):
    return JarvisCommandSecurityBindingContract(
        binding_id="jarvis_command_security_binding_contract_v0_1"
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain required")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

