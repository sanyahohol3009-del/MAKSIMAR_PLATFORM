from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_OBSERVER_MODES = ("normal_observer", "family_child_control_reference")


@dataclass(frozen=True)
class MobileScreenPolicyContract:
    """Executable policy contract for normal mobile screen observer mode."""

    policy_id: str
    observer_mode: str
    read_only_required: bool
    consent_required: bool
    audit_required: bool
    remote_assistance_disabled_by_default: bool
    direct_screen_capture_allowed: bool
    screenshot_allowed: bool
    screen_recording_allowed: bool
    touch_injection_allowed: bool
    keyboard_injection_allowed: bool
    app_control_allowed: bool
    screen_time_enforcement_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if self.observer_mode not in _ALLOWED_OBSERVER_MODES:
            raise ValueError(f"observer_mode must be one of {_ALLOWED_OBSERVER_MODES}")
        if not self.read_only_required:
            raise ValueError("read_only_required must be True")
        if not self.consent_required:
            raise ValueError("consent_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.remote_assistance_disabled_by_default:
            raise ValueError("remote_assistance_disabled_by_default must be True")
        forbidden = {
            "direct_screen_capture_allowed": self.direct_screen_capture_allowed,
            "screenshot_allowed": self.screenshot_allowed,
            "screen_recording_allowed": self.screen_recording_allowed,
            "touch_injection_allowed": self.touch_injection_allowed,
            "keyboard_injection_allowed": self.keyboard_injection_allowed,
            "app_control_allowed": self.app_control_allowed,
            "screen_time_enforcement_allowed": self.screen_time_enforcement_allowed,
            "external_network_access_allowed": self.external_network_access_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError(f"normal observer forbids enabled capabilities: {enabled}")

    def permits_normal_observer_remote_control(self) -> bool:
        return False
