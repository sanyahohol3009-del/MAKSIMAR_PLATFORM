from __future__ import annotations

from SUPERVISOR.runtime_preflight import run_preflight


def test_run_preflight_returns_report() -> None:
    report = run_preflight()

    assert report.preflight_id
    assert report.checked_at
    assert isinstance(report.ok, bool)
    assert isinstance(report.stale_tmux_found, bool)
    assert isinstance(report.stale_pid_found, bool)
    assert isinstance(report.stale_heartbeat_found, bool)
    assert isinstance(report.port_conflict_found, bool)
    assert isinstance(report.previous_crash_found, bool)
    assert isinstance(report.details, dict)


def test_preflight_contains_core_sections() -> None:
    report = run_preflight()
    details = report.details

    assert "python" in details
    assert "directories" in details
    assert "imports" in details
    assert "tmux" in details
    assert "heartbeat" in details
    assert "pids" in details
    assert "port" in details
    assert "previous_crash" in details
