from __future__ import annotations

from dataclasses import dataclass
from typing import Any


JARVIS_LIVE_RUNTIME_STATE_FILE = (
    "~/MAKSIMAR_RUNTIME/jarvis_live/state/jarvis_live_state.json"
)
JARVIS_LIVE_RUNTIME_HEARTBEAT_FILE = (
    "~/MAKSIMAR_RUNTIME/jarvis_live/state/jarvis_live_heartbeat.json"
)
JARVIS_LIVE_RUNTIME_PID_FILE = (
    "~/MAKSIMAR_RUNTIME/jarvis_live/state/jarvis_live.pid"
)
JARVIS_LIVE_RUNTIME_EVENT_LOG_FILE = (
    "~/MAKSIMAR_RUNTIME/jarvis_live/logs/jarvis_live_events.jsonl"
)


@dataclass(frozen=True, slots=True)
class JarvisLiveSessionSupervisorContract:
    supervisor_id: str = "jarvis_live_session_supervisor_v0_1"
    state_file: str = JARVIS_LIVE_RUNTIME_STATE_FILE
    heartbeat_file: str = JARVIS_LIVE_RUNTIME_HEARTBEAT_FILE
    pid_file: str = JARVIS_LIVE_RUNTIME_PID_FILE
    event_log_file: str = JARVIS_LIVE_RUNTIME_EVENT_LOG_FILE
    background_supervisor_allowed: bool = True
    venv_activation_hook_supported: bool = True
    pid_file_required: bool = True
    heartbeat_file_required: bool = True
    state_file_required: bool = True
    owner_visible_status_required: bool = True
    local_only_required: bool = True
    explicit_stop_command_required: bool = True
    audit_required: bool = True
    pc_control_allowed: bool = False
    mouse_control_allowed: bool = False
    keyboard_control_allowed: bool = False
    browser_control_allowed: bool = False
    app_launch_allowed: bool = False
    shell_execution_allowed: bool = False
    hidden_runtime_allowed: bool = False
    network_listener_allowed: bool = False
    remote_control_allowed: bool = False
    dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name in (
            "supervisor_id",
            "state_file",
            "heartbeat_file",
            "pid_file",
            "event_log_file",
        ):
            _require_non_empty(getattr(self, field_name), field_name)
        for field_name in (
            "background_supervisor_allowed",
            "venv_activation_hook_supported",
            "pid_file_required",
            "heartbeat_file_required",
            "state_file_required",
            "owner_visible_status_required",
            "local_only_required",
            "explicit_stop_command_required",
            "audit_required",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "pc_control_allowed",
            "mouse_control_allowed",
            "keyboard_control_allowed",
            "browser_control_allowed",
            "app_launch_allowed",
            "shell_execution_allowed",
            "hidden_runtime_allowed",
            "network_listener_allowed",
            "remote_control_allowed",
            "dashboard_execution_allowed",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "supervisor_id": self.supervisor_id,
            "state_file": self.state_file,
            "heartbeat_file": self.heartbeat_file,
            "pid_file": self.pid_file,
            "event_log_file": self.event_log_file,
            "background_supervisor_allowed": self.background_supervisor_allowed,
            "venv_activation_hook_supported": self.venv_activation_hook_supported,
            "pid_file_required": self.pid_file_required,
            "heartbeat_file_required": self.heartbeat_file_required,
            "state_file_required": self.state_file_required,
            "owner_visible_status_required": self.owner_visible_status_required,
            "local_only_required": self.local_only_required,
            "explicit_stop_command_required": self.explicit_stop_command_required,
            "audit_required": self.audit_required,
            "pc_control_allowed": self.pc_control_allowed,
            "mouse_control_allowed": self.mouse_control_allowed,
            "keyboard_control_allowed": self.keyboard_control_allowed,
            "browser_control_allowed": self.browser_control_allowed,
            "app_launch_allowed": self.app_launch_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "hidden_runtime_allowed": self.hidden_runtime_allowed,
            "network_listener_allowed": self.network_listener_allowed,
            "remote_control_allowed": self.remote_control_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
        }


def build_jarvis_live_session_supervisor_contract() -> (
    JarvisLiveSessionSupervisorContract
):
    return JarvisLiveSessionSupervisorContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")
