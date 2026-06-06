from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisQueueStatusPanelContract:
    queue_status: str = "blocked"
    queue_pressure: str = "none"
    queue_length: int = 0
    active_task_count: int = 0
    queued_task_count: int = 0
    queue_execution_allowed: bool = False
    runtime_start_allowed: bool = False
    model_download_allowed: bool = False
    read_only: bool = True
    dashboard_safe: bool = True
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_member(self.queue_status, ("blocked",), "queue_status")
        _require_member(self.queue_pressure, ("none",), "queue_pressure")
        _require_zero(self.queue_length, "queue_length")
        _require_zero(self.active_task_count, "active_task_count")
        _require_zero(self.queued_task_count, "queued_task_count")
        _require_false(self.queue_execution_allowed, "queue_execution_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "queue_status": self.queue_status,
            "queue_pressure": self.queue_pressure,
            "queue_length": self.queue_length,
            "active_task_count": self.active_task_count,
            "queued_task_count": self.queued_task_count,
            "queue_execution_allowed": self.queue_execution_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "model_download_allowed": self.model_download_allowed,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_jarvis_queue_status_panel_contract() -> JarvisQueueStatusPanelContract:
    return JarvisQueueStatusPanelContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_member(value: str, allowed_values: tuple[str, ...], field_name: str) -> None:
    _require_non_empty(value, field_name)
    if value not in allowed_values:
        raise ValueError(f"{field_name} has unsupported value: {value}")


def _require_zero(value: int, field_name: str) -> None:
    if value != 0:
        raise ValueError(f"{field_name} must remain zero")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

