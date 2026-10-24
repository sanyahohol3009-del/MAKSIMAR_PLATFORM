from __future__ import annotations

from dataclasses import dataclass
from typing import Any


TRUE_APPROVAL_GATES: tuple[str, ...] = (
    "owner_gate_required",
    "allowlist_match_required",
    "audit_record_required",
    "policy_boundary_required",
    "refusal_on_unknown_action",
    "refusal_on_missing_owner_command",
)

TRUE_EXECUTION_GATES: tuple[str, ...] = ("policy_execution_allowed_when_requirements_satisfied",)

FALSE_APPROVAL_GATES: tuple[str, ...] = (
    "approval_prompt_required",
    "action_preview_required",
    "silent_execution_allowed",
    "hidden_action_allowed",
    "bypass_approval_allowed",
    "bypass_audit_allowed",
)


@dataclass(frozen=True, slots=True)
class JarvisPcActionApprovalBinding:
    binding_id: str
    required_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, True) for key in TRUE_APPROVAL_GATES
    )
    enabled_execution_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, True) for key in TRUE_EXECUTION_GATES
    )
    disabled_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, False) for key in FALSE_APPROVAL_GATES
    )

    def __post_init__(self) -> None:
        _require_non_empty(self.binding_id, "binding_id")
        if tuple(key for key, _value in self.required_gates) != TRUE_APPROVAL_GATES:
            raise ValueError("required_gates must match canonical approval gates")
        if tuple(key for key, _value in self.enabled_execution_gates) != TRUE_EXECUTION_GATES:
            raise ValueError("enabled_execution_gates must match canonical execution gates")
        if tuple(key for key, _value in self.disabled_gates) != FALSE_APPROVAL_GATES:
            raise ValueError("disabled_gates must match canonical approval denial gates")
        for key, value in self.required_gates:
            _require_non_empty(key, "required_gates")
            _require_true(value, key)
        for key, value in self.enabled_execution_gates:
            _require_non_empty(key, "enabled_execution_gates")
            _require_true(value, key)
        for key, value in self.disabled_gates:
            _require_non_empty(key, "disabled_gates")
            _require_false(value, key)

    def to_read_model(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"binding_id": self.binding_id}
        payload.update(dict(self.required_gates))
        payload.update(dict(self.enabled_execution_gates))
        payload.update(dict(self.disabled_gates))
        return payload


def build_jarvis_pc_action_approval_binding() -> JarvisPcActionApprovalBinding:
    return JarvisPcActionApprovalBinding(
        binding_id="jarvis_pc_action_approval_binding_v1"
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
