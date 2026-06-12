from pathlib import Path


def test_stop_cleans_stale_pid_and_marks_runtime_dead() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_stop.py").read_text(
        encoding="utf-8"
    )

    assert "stale_pid_removed" in source
    assert "PID_FILE.unlink(missing_ok=True)" in source
    assert '"runtime_alive": False' in source
    assert '"runtime_dead_reason": "stopped"' in source
    assert '"supervisor_running": False' in source
    assert "killall" not in source
    assert "pkill" not in source
    assert "shell=True" not in source
