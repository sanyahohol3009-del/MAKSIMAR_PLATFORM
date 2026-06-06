from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisResourceStatusPanelContract:
    gpu_status: str = "unknown"
    ram_status: str = "unknown"
    gpu_pressure_status: str = "not_polled"
    ram_pressure_status: str = "not_polled"
    resource_snapshot_available: bool = False
    resource_polling_enabled: bool = False
    runtime_start_allowed: bool = False
    model_download_allowed: bool = False
    read_only: bool = True
    dashboard_safe: bool = True
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_member(self.gpu_status, ("unknown",), "gpu_status")
        _require_member(self.ram_status, ("unknown",), "ram_status")
        _require_member(self.gpu_pressure_status, ("not_polled",), "gpu_pressure_status")
        _require_member(self.ram_pressure_status, ("not_polled",), "ram_pressure_status")
        _require_false(self.resource_snapshot_available, "resource_snapshot_available")
        _require_false(self.resource_polling_enabled, "resource_polling_enabled")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "gpu_status": self.gpu_status,
            "ram_status": self.ram_status,
            "gpu_pressure_status": self.gpu_pressure_status,
            "ram_pressure_status": self.ram_pressure_status,
            "resource_snapshot_available": self.resource_snapshot_available,
            "resource_polling_enabled": self.resource_polling_enabled,
            "runtime_start_allowed": self.runtime_start_allowed,
            "model_download_allowed": self.model_download_allowed,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_jarvis_resource_status_panel_contract() -> JarvisResourceStatusPanelContract:
    return JarvisResourceStatusPanelContract()


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

