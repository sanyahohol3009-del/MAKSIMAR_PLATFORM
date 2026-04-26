from __future__ import annotations

from pathlib import Path


def test_tools_work_contains_preflight_before_runtime_start() -> None:
    work_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "work"
    content = work_file.read_text(encoding="utf-8")

    preflight_index = content.index("run_preflight")
    runtime_index = content.index("start_runtime")

    assert preflight_index < runtime_index


def test_tools_work_waits_for_runtime_readiness() -> None:
    work_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "work"
    content = work_file.read_text(encoding="utf-8")

    assert "wait_for_runtime_readiness" in content
    assert "wait_for_guard_chain" in content


def test_tools_work_uses_runtime_preflight_script() -> None:
    work_file = Path.home() / "MAKSIMAR_PLATFORM" / "tools" / "work"
    content = work_file.read_text(encoding="utf-8")

    assert "SUPERVISOR/runtime_preflight.py" in content
    assert "preflight_result.json" in content
