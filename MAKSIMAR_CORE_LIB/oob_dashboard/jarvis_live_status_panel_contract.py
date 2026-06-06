from __future__ import annotations

from dataclasses import dataclass
from typing import Any


DEFAULT_BLOCKED_REASON = (
    "JARVIS-LIVE remains disabled until approval, audit, allowlist, runtime, "
    "and dashboard gates are complete."
)


@dataclass(frozen=True, slots=True)
class JarvisLiveStatusPanelContract:
    panel_id: str
    panel_title: str
    voice_status: str
    model_download_allowed: bool
    runtime_start_allowed: bool
    voice_allowed: bool
    pc_control_allowed: bool
    approval_status: str
    blocked_reason: str
    next_roadmap_batch: str
    read_only: bool = True
    dashboard_safe: bool = True
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.panel_title, "panel_title")
        _require_non_empty(self.voice_status, "voice_status")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.voice_allowed, "voice_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_non_empty(self.approval_status, "approval_status")
        _require_non_empty(self.blocked_reason, "blocked_reason")
        _require_non_empty(self.next_roadmap_batch, "next_roadmap_batch")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "panel_id": self.panel_id,
            "panel_title": self.panel_title,
            "voice_status": self.voice_status,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "voice_allowed": self.voice_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "approval_status": self.approval_status,
            "blocked_reason": self.blocked_reason,
            "next_roadmap_batch": self.next_roadmap_batch,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_jarvis_live_status_panel_contract(
    status_payload: dict[str, Any] | None = None,
) -> JarvisLiveStatusPanelContract:
    payload = {} if status_payload is None else status_payload
    next_batch = payload.get("next_batch")
    next_batch_id = "JL-8"
    if isinstance(next_batch, dict):
        next_batch_id = str(next_batch.get("batch_id", next_batch_id))

    return JarvisLiveStatusPanelContract(
        panel_id="jarvis_live_status_panel",
        panel_title="JARVIS-LIVE Status",
        voice_status="blocked",
        model_download_allowed=bool(payload.get("model_download_allowed_now", False)),
        runtime_start_allowed=bool(payload.get("runtime_start_allowed_now", False)),
        voice_allowed=bool(payload.get("voice_allowed_now", False)),
        pc_control_allowed=bool(payload.get("pc_control_allowed_now", False)),
        approval_status="required",
        blocked_reason=DEFAULT_BLOCKED_REASON,
        next_roadmap_batch=next_batch_id,
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

