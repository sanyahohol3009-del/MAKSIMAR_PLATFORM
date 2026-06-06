from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SCREEN_VISION_CANDIDATE_ROLES: tuple[str, ...] = (
    "screen_observer",
    "vision_ocr_candidate",
    "text_region_candidate",
    "ui_element_candidate",
    "context_snapshot_candidate",
)

SCREEN_VISION_SOURCE_SURFACES: tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/mobile_screen_observer",
    "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME",
    "MAKSIMAR_CORE_LIB/security_layer",
    "MAKSIMAR_CORE_LIB/oob_dashboard",
)


@dataclass(frozen=True, slots=True)
class ScreenVisionCandidateRole:
    role_id: str
    source_surface: str
    status: str = "candidate_only"

    def __post_init__(self) -> None:
        _require_member(self.role_id, SCREEN_VISION_CANDIDATE_ROLES, "role_id")
        _require_member(self.source_surface, SCREEN_VISION_SOURCE_SURFACES, "source_surface")
        _require_member(self.status, ("candidate_only",), "status")

    def to_read_model(self) -> dict[str, str]:
        return {
            "role_id": self.role_id,
            "source_surface": self.source_surface,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class ScreenVisionCandidateContract:
    contract_id: str
    candidate_roles: tuple[ScreenVisionCandidateRole, ...]
    source_surfaces: tuple[str, ...]
    read_only: bool = True
    dashboard_safe: bool = True
    screen_capture_runtime_enabled: bool = False
    ocr_runtime_enabled: bool = False
    pixel_decode_allowed: bool = False
    screenshot_allowed: bool = False
    screen_recording_allowed: bool = False
    mouse_control_allowed: bool = False
    keyboard_control_allowed: bool = False
    app_control_allowed: bool = False
    pc_control_allowed: bool = False
    model_download_allowed: bool = False
    runtime_start_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if tuple(role.role_id for role in self.candidate_roles) != SCREEN_VISION_CANDIDATE_ROLES:
            raise ValueError("candidate_roles must cover every screen vision role in order")
        if self.source_surfaces != SCREEN_VISION_SOURCE_SURFACES:
            raise ValueError("source_surfaces must match existing screen/security/dashboard surfaces")
        _require_true(self.read_only, "read_only")
        _require_true(self.dashboard_safe, "dashboard_safe")
        _require_false(self.screen_capture_runtime_enabled, "screen_capture_runtime_enabled")
        _require_false(self.ocr_runtime_enabled, "ocr_runtime_enabled")
        _require_false(self.pixel_decode_allowed, "pixel_decode_allowed")
        _require_false(self.screenshot_allowed, "screenshot_allowed")
        _require_false(self.screen_recording_allowed, "screen_recording_allowed")
        _require_false(self.mouse_control_allowed, "mouse_control_allowed")
        _require_false(self.keyboard_control_allowed, "keyboard_control_allowed")
        _require_false(self.app_control_allowed, "app_control_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "candidate_roles": tuple(role.to_read_model() for role in self.candidate_roles),
            "candidate_role_ids": tuple(role.role_id for role in self.candidate_roles),
            "source_surfaces": self.source_surfaces,
            "read_only": self.read_only,
            "dashboard_safe": self.dashboard_safe,
            "screen_capture_runtime_enabled": self.screen_capture_runtime_enabled,
            "ocr_runtime_enabled": self.ocr_runtime_enabled,
            "pixel_decode_allowed": self.pixel_decode_allowed,
            "screenshot_allowed": self.screenshot_allowed,
            "screen_recording_allowed": self.screen_recording_allowed,
            "mouse_control_allowed": self.mouse_control_allowed,
            "keyboard_control_allowed": self.keyboard_control_allowed,
            "app_control_allowed": self.app_control_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "model_download_allowed": self.model_download_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_screen_vision_candidate_contract() -> ScreenVisionCandidateContract:
    return ScreenVisionCandidateContract(
        contract_id="screen_vision_candidate_contract_v0_1",
        candidate_roles=(
            ScreenVisionCandidateRole(
                "screen_observer",
                "MAKSIMAR_CORE_LIB/mobile_screen_observer",
            ),
            ScreenVisionCandidateRole(
                "vision_ocr_candidate",
                "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME",
            ),
            ScreenVisionCandidateRole(
                "text_region_candidate",
                "MAKSIMAR_CORE_LIB/mobile_screen_observer",
            ),
            ScreenVisionCandidateRole(
                "ui_element_candidate",
                "MAKSIMAR_CORE_LIB/mobile_screen_observer",
            ),
            ScreenVisionCandidateRole(
                "context_snapshot_candidate",
                "MAKSIMAR_CORE_LIB/oob_dashboard",
            ),
        ),
        source_surfaces=SCREEN_VISION_SOURCE_SURFACES,
    )


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

