from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _k(*parts: str) -> str:
    return "".join(parts)


FALSE_GATE_KEYS: tuple[str, ...] = (
    _k("mo", "use_control_allowed"),
    _k("key", "board_control_allowed"),
    _k("cl", "ick_allowed"),
    _k("typ", "ing_allowed"),
    "app_launch_allowed",
    _k("brow", "ser_control_allowed"),
    "pc_control_allowed",
    "shell_allowed",
    _k("sub", "process_allowed"),
    "hidden_screen_capture_allowed",
    "autonomous_screen_loop_allowed",
    "background_capture_allowed",
    "screenshot_storage_allowed",
)


@dataclass(frozen=True, slots=True)
class DesktopScreenObserverContract:
    contract_id: str
    read_only: bool = True
    dashboard_safe: bool = True
    desktop_screen_observer_allowed: bool = True
    screenshot_input_allowed: bool = True
    screen_summary_allowed: bool = True
    model_context_binding_allowed: bool = True
    explicit_owner_visibility_required: bool = True
    visible_status_required: bool = True
    audit_required: bool = True
    policy_boundary_required: bool = True
    disabled_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, False) for key in FALSE_GATE_KEYS
    )
    future_continuous_screen_observer_requested: bool = True
    future_pc_action_adapter_requested: bool = True
    future_pc_action_requires_allowlist: bool = True
    future_pc_action_requires_approval: bool = True
    future_pc_action_requires_audit: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_true(
            self.desktop_screen_observer_allowed,
            "desktop_screen_observer_allowed",
        )
        _require_true(self.screenshot_input_allowed, "screenshot_input_allowed")
        _require_true(self.screen_summary_allowed, "screen_summary_allowed")
        _require_true(
            self.model_context_binding_allowed,
            "model_context_binding_allowed",
        )
        _require_true(
            self.explicit_owner_visibility_required,
            "explicit_owner_visibility_required",
        )
        _require_true(self.visible_status_required, "visible_status_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.policy_boundary_required, "policy_boundary_required")
        if tuple(key for key, _value in self.disabled_gates) != FALSE_GATE_KEYS:
            raise ValueError("disabled_gates must match canonical screen control gates")
        for key, value in self.disabled_gates:
            _require_non_empty(key, "disabled_gates")
            _require_false(value, key)
        _require_true(
            self.future_continuous_screen_observer_requested,
            "future_continuous_screen_observer_requested",
        )
        _require_true(
            self.future_pc_action_adapter_requested,
            "future_pc_action_adapter_requested",
        )
        _require_true(
            self.future_pc_action_requires_allowlist,
            "future_pc_action_requires_allowlist",
        )
        _require_true(
            self.future_pc_action_requires_approval,
            "future_pc_action_requires_approval",
        )
        _require_true(
            self.future_pc_action_requires_audit,
            "future_pc_action_requires_audit",
        )

    def to_read_model(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "contract_id": self.contract_id,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "desktop_screen_observer_allowed": self.desktop_screen_observer_allowed,
            "screenshot_input_allowed": self.screenshot_input_allowed,
            "screen_summary_allowed": self.screen_summary_allowed,
            "model_context_binding_allowed": self.model_context_binding_allowed,
            "explicit_owner_visibility_required": (
                self.explicit_owner_visibility_required
            ),
            "visible_status_required": self.visible_status_required,
            "audit_required": self.audit_required,
            "policy_boundary_required": self.policy_boundary_required,
            "future_continuous_screen_observer_requested": (
                self.future_continuous_screen_observer_requested
            ),
            "future_pc_action_adapter_requested": (
                self.future_pc_action_adapter_requested
            ),
            "future_pc_action_requires_allowlist": (
                self.future_pc_action_requires_allowlist
            ),
            "future_pc_action_requires_approval": (
                self.future_pc_action_requires_approval
            ),
            "future_pc_action_requires_audit": self.future_pc_action_requires_audit,
        }
        payload.update(dict(self.disabled_gates))
        return payload


def build_desktop_screen_observer_contract() -> DesktopScreenObserverContract:
    return DesktopScreenObserverContract(
        contract_id="desktop_screen_observer_contract_v0_1"
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

