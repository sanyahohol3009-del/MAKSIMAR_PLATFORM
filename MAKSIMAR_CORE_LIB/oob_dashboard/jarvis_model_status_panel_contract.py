from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisModelStatusPanelContract:
    selected_model_role: str = ""
    selected_model_id: str = ""
    model_selected: bool = False
    model_download_allowed: bool = False
    model_runtime_allowed: bool = False
    model_download_status: str = "blocked"
    model_runtime_status: str = "blocked"
    blocked_reason: str = "No JARVIS-LIVE model is selected or downloadable yet."
    read_only: bool = True
    dashboard_safe: bool = True
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_false(self.model_selected, "model_selected")
        if self.selected_model_role != "":
            raise ValueError("selected_model_role must be empty until model selection is ready")
        if self.selected_model_id != "":
            raise ValueError("selected_model_id must be empty until model selection is ready")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.model_runtime_allowed, "model_runtime_allowed")
        _require_member(self.model_download_status, ("blocked",), "model_download_status")
        _require_member(self.model_runtime_status, ("blocked",), "model_runtime_status")
        _require_non_empty(self.blocked_reason, "blocked_reason")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "selected_model_role": self.selected_model_role,
            "selected_model_id": self.selected_model_id,
            "model_selected": self.model_selected,
            "model_download_allowed": self.model_download_allowed,
            "model_runtime_allowed": self.model_runtime_allowed,
            "model_download_status": self.model_download_status,
            "model_runtime_status": self.model_runtime_status,
            "blocked_reason": self.blocked_reason,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_jarvis_model_status_panel_contract() -> JarvisModelStatusPanelContract:
    return JarvisModelStatusPanelContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_member(value: str, allowed_values: tuple[str, ...], field_name: str) -> None:
    _require_non_empty(value, field_name)
    if value not in allowed_values:
        raise ValueError(f"{field_name} has unsupported value: {value}")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

