from __future__ import annotations

from pathlib import Path


def test_tools_work_starts_oob_dashboard() -> None:
    work_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "work"
    content = work_file.read_text(encoding="utf-8")

    assert "oob_dashboard_ctl" in content
    assert "start_oob_dashboard" in content


def test_tools_rest_stops_oob_dashboard_last() -> None:
    rest_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "rest"
    content = rest_file.read_text(encoding="utf-8")

    assert "stopping OOB dashboard last" in content
    assert "oob_dashboard_ctl" in content
