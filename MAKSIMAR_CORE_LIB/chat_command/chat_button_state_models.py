from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_BUTTON_STATES = ("visible_disabled", "visible_requires_approval", "hidden", "blocked")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


@dataclass(frozen=True)
class ChatButtonStateModel:
    button_id: str
    label: str
    target_intent_id: str
    button_state: str
    display_only: bool
    approval_required: bool
    control_plane_handoff_required: bool
    direct_execution_allowed: bool
    dashboard_control_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "button_id", _ensure_non_empty(self.button_id, "button_id"))
        object.__setattr__(self, "label", _ensure_non_empty(self.label, "label"))
        object.__setattr__(self, "target_intent_id", _ensure_non_empty(self.target_intent_id, "target_intent_id"))
        object.__setattr__(
            self,
            "button_state",
            _ensure_allowed(self.button_state, "button_state", _ALLOWED_BUTTON_STATES),
        )

        if not self.display_only:
            raise ValueError("display_only must be True")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.control_plane_handoff_required:
            raise ValueError("control_plane_handoff_required must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.dashboard_control_allowed:
            raise ValueError("dashboard_control_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
