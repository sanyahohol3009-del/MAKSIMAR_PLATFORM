from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class IOSModelRuntimeStatus:
    status_id: str
    platform: str
    status_read_model_only: bool
    runtime_installed: bool
    runtime_started: bool
    model_loaded: bool
    model_downloaded: bool
    model_download_allowed: bool
    degraded_mode_available: bool
    server_senior_required: bool
    junior_runtime_ready: bool
    local_inference_started: bool
    no_runtime_side_effects: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "status_id", _ensure_non_empty(self.status_id, "status_id"))
        object.__setattr__(self, "platform", _ensure_non_empty(self.platform, "platform"))
        if self.platform != "ios":
            raise ValueError("platform must be ios")
        for field_name in (
            "status_read_model_only",
            "degraded_mode_available",
            "server_senior_required",
            "no_runtime_side_effects",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "runtime_installed",
            "runtime_started",
            "model_loaded",
            "model_downloaded",
            "model_download_allowed",
            "junior_runtime_ready",
            "local_inference_started",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "status_id": self.status_id,
            "platform": self.platform,
            "status_read_model_only": self.status_read_model_only,
            "runtime_installed": self.runtime_installed,
            "runtime_started": self.runtime_started,
            "model_loaded": self.model_loaded,
            "model_downloaded": self.model_downloaded,
            "model_download_allowed": self.model_download_allowed,
            "degraded_mode_available": self.degraded_mode_available,
            "server_senior_required": self.server_senior_required,
            "junior_runtime_ready": self.junior_runtime_ready,
            "local_inference_started": self.local_inference_started,
            "no_runtime_side_effects": self.no_runtime_side_effects,
        }


def build_ios_model_runtime_status() -> IOSModelRuntimeStatus:
    return IOSModelRuntimeStatus(
        status_id="ios_model_runtime_status_v0_1",
        platform="ios",
        status_read_model_only=True,
        runtime_installed=False,
        runtime_started=False,
        model_loaded=False,
        model_downloaded=False,
        model_download_allowed=False,
        degraded_mode_available=True,
        server_senior_required=True,
        junior_runtime_ready=False,
        local_inference_started=False,
        no_runtime_side_effects=True,
    )
