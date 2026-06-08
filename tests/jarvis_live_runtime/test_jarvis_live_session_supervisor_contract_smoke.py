import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_live_session_supervisor_contract import (
    JarvisLiveSessionSupervisorContract,
    build_jarvis_live_session_supervisor_contract,
)


def test_session_supervisor_contract_gates_are_safe_by_default() -> None:
    model = build_jarvis_live_session_supervisor_contract().to_read_model()

    for key in (
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
        assert model[key] is True

    for key in (
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
        assert model[key] is False

    assert model["state_file"].endswith("jarvis_live_state.json")
    assert model["heartbeat_file"].endswith("jarvis_live_heartbeat.json")
    assert model["pid_file"].endswith("jarvis_live.pid")


def test_session_supervisor_contract_rejects_dangerous_flags() -> None:
    with pytest.raises(ValueError):
        JarvisLiveSessionSupervisorContract(pc_control_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveSessionSupervisorContract(network_listener_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveSessionSupervisorContract(background_supervisor_allowed=False)
