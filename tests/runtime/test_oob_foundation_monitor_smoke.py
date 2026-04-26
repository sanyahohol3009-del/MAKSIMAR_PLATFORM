from __future__ import annotations

from tools.monitor.oob_foundation_monitor import render_screen


def test_render_screen_contains_main_sections() -> None:
    screen = render_screen()

    assert "MAKSIMAR OOB FOUNDATION MONITOR" in screen
    assert "SESSIONS" in screen
    assert "HEARTBEATS" in screen
    assert "RUNTIME ACCESS" in screen
    assert "LOG TAILS" in screen
