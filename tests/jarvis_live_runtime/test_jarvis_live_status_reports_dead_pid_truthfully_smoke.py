from pathlib import Path


def test_status_source_reports_dead_pid_truthfully() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_status.py").read_text(
        encoding="utf-8"
    )

    assert "runtime_alive=" in source
    assert "runtime_dead_reason=" in source
    assert "latest_state_is_stale=" in source
    assert "state_truth_source=" in source
    assert "pid_missing" in source
    assert "pid_not_running" in source
    assert "heartbeat_stale" in source
    assert "voice_loop_enabled_state=" in source
    assert "always_listening_enabled_state=" in source
    assert "voice_loop_enabled_state and runtime_alive" in source
    assert "always_listening_enabled_state and runtime_alive" in source
    assert "background_stdout_log=" in source
    assert "background_stderr_log=" in source
    assert "pc_control_allowed=false" in source
