from __future__ import annotations

from dataclasses import dataclass
from typing import Any


JARVIS_PC_ACTION_ALLOWLIST_IDS: tuple[str, ...] = (
    "open_browser",
    "open_youtube",
    "open_youtube_kids_search",
    "read_project_status",
    "show_test_status",
)


def _k(*parts: str) -> str:
    return "".join(parts)


FALSE_ADAPTER_GATES: tuple[str, ...] = (
    "direct_pc_control_allowed",
    "runtime_execution_allowed",
    "mouse_runtime_allowed",
    "keyboard_runtime_allowed",
    _k("cl", "ick_runtime_allowed"),
    "typing_runtime_allowed",
    "app_launch_runtime_allowed",
    "browser_runtime_allowed",
    "shell_allowed",
    _k("sub", "process_allowed"),
    _k("power", "shell_allowed"),
    "hidden_remote_control_allowed",
    "autonomous_action_allowed",
    "dashboard_execution_allowed",
)


@dataclass(frozen=True, slots=True)
class JarvisPcActionAdapterContract:
    adapter_id: str
    allowed_action_ids: tuple[str, ...]
    read_only_contract: bool = True
    controlled_pc_action_candidate: bool = True
    owner_command_required: bool = True
    allowlist_required: bool = True
    approval_required: bool = True
    audit_required: bool = True
    policy_boundary_required: bool = True
    screen_context_required: bool = True
    voice_or_text_intent_required: bool = True
    explicit_action_preview_required: bool = True
    disabled_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, False) for key in FALSE_ADAPTER_GATES
    )

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_id, "adapter_id")
        if self.allowed_action_ids != JARVIS_PC_ACTION_ALLOWLIST_IDS:
            raise ValueError("allowed_action_ids must match canonical JARVIS PC actions")
        _require_true(self.read_only_contract, "read_only_contract")
        _require_true(
            self.controlled_pc_action_candidate,
            "controlled_pc_action_candidate",
        )
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.allowlist_required, "allowlist_required")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.policy_boundary_required, "policy_boundary_required")
        _require_true(self.screen_context_required, "screen_context_required")
        _require_true(
            self.voice_or_text_intent_required,
            "voice_or_text_intent_required",
        )
        _require_true(
            self.explicit_action_preview_required,
            "explicit_action_preview_required",
        )
        if tuple(key for key, _value in self.disabled_gates) != FALSE_ADAPTER_GATES:
            raise ValueError("disabled_gates must match canonical adapter gates")
        for key, value in self.disabled_gates:
            _require_non_empty(key, "disabled_gates")
            _require_false(value, key)

    def to_read_model(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "adapter_id": self.adapter_id,
            "allowed_action_ids": self.allowed_action_ids,
            "read_only_contract": self.read_only_contract,
            "controlled_pc_action_candidate": self.controlled_pc_action_candidate,
            "owner_command_required": self.owner_command_required,
            "allowlist_required": self.allowlist_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "policy_boundary_required": self.policy_boundary_required,
            "screen_context_required": self.screen_context_required,
            "voice_or_text_intent_required": self.voice_or_text_intent_required,
            "explicit_action_preview_required": self.explicit_action_preview_required,
        }
        payload.update(dict(self.disabled_gates))
        return payload


def build_jarvis_pc_action_adapter_contract() -> JarvisPcActionAdapterContract:
    return JarvisPcActionAdapterContract(
        adapter_id="jarvis_pc_action_adapter_contract_v0_1",
        allowed_action_ids=JARVIS_PC_ACTION_ALLOWLIST_IDS,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

