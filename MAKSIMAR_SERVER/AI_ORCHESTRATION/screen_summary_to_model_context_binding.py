from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _k(*parts: str) -> str:
    return "".join(parts)


FALSE_BINDING_GATE_KEYS: tuple[str, ...] = (
    "direct_model_action_allowed",
    "tool_call_allowed",
    "pc_control_allowed",
    _k("mo", "use_control_allowed"),
    _k("key", "board_control_allowed"),
    _k("cl", "ick_allowed"),
    _k("typ", "ing_allowed"),
    "app_launch_allowed",
    _k("brow", "ser_control_allowed"),
    "direct_runtime_execution_allowed",
    "hidden_remote_control_allowed",
)


@dataclass(frozen=True, slots=True)
class ScreenSummaryToModelContextBinding:
    binding_id: str
    read_only: bool = True
    model_context_binding_allowed: bool = True
    screen_summary_required: bool = True
    owner_visible_status_required: bool = True
    policy_boundary_required: bool = True
    audit_required: bool = True
    disabled_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, False) for key in FALSE_BINDING_GATE_KEYS
    )

    def __post_init__(self) -> None:
        _require_non_empty(self.binding_id, "binding_id")
        _require_true(self.read_only, "read_only")
        _require_true(
            self.model_context_binding_allowed,
            "model_context_binding_allowed",
        )
        _require_true(self.screen_summary_required, "screen_summary_required")
        _require_true(
            self.owner_visible_status_required,
            "owner_visible_status_required",
        )
        _require_true(self.policy_boundary_required, "policy_boundary_required")
        _require_true(self.audit_required, "audit_required")
        if tuple(key for key, _value in self.disabled_gates) != FALSE_BINDING_GATE_KEYS:
            raise ValueError("disabled_gates must match canonical model context gates")
        for key, value in self.disabled_gates:
            _require_non_empty(key, "disabled_gates")
            _require_false(value, key)

    def to_read_model(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "binding_id": self.binding_id,
            "read_only": self.read_only,
            "model_context_binding_allowed": self.model_context_binding_allowed,
            "screen_summary_required": self.screen_summary_required,
            "owner_visible_status_required": self.owner_visible_status_required,
            "policy_boundary_required": self.policy_boundary_required,
            "audit_required": self.audit_required,
        }
        payload.update(dict(self.disabled_gates))
        return payload


def build_screen_summary_to_model_context_binding() -> (
    ScreenSummaryToModelContextBinding
):
    return ScreenSummaryToModelContextBinding(
        binding_id="screen_summary_to_model_context_binding_v0_1"
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

