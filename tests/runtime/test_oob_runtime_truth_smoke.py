from __future__ import annotations

from tools.monitor import oob_foundation_monitor as monitor


def test_runtime_truth_status_returns_known_value() -> None:
    value = monitor.runtime_truth_status()
    assert value in {"UP", "DOWN", "STALE", "DEGRADED"}


def test_render_screen_contains_runtime_truth_block() -> None:
    screen = monitor.render_screen()

    assert "RUNTIME TRUTH" in screen
    assert "runtime_truth:" in screen
    assert "runtime_heartbeat:" in screen
    assert "guard_heartbeat:" in screen
    assert "core_guard_heartbeat:" in screen
    assert "kernel_heartbeat:" in screen
