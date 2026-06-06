from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_full_roadmap_contract import (
    DRIFT_COMMAND_HINT,
    FORBIDDEN_PARALLEL_WORLD_ROOTS,
    FULL_AUTO_COMMAND_HINT,
    XRAY_COMMAND_HINT,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from tools.project_readiness_control.jarvis_live_full_roadmap_status import render_status


def test_jarvis_live_full_status_builder_does_not_import_tools() -> None:
    source = Path(
        "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/"
        "jarvis_live_full_roadmap_status_builder.py"
    ).read_text(encoding="utf-8")

    assert "tools.project_readiness_control" not in source
    assert "MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_full_roadmap_contract" in source


def test_jarvis_live_full_status_has_command_hints_but_does_not_execute_them() -> None:
    status = build_jarvis_live_full_roadmap_status()
    commands = status["required_control_commands"]

    assert commands["xray"] == XRAY_COMMAND_HINT
    assert commands["drift"] == DRIFT_COMMAND_HINT
    assert commands["full_auto"] == FULL_AUTO_COMMAND_HINT
    assert "python -m pytest tests/jarvis_live -q" in commands["jarvis_tests"]
    assert status["runtime_started"] is False
    assert status["model_download_started"] is False


def test_jarvis_live_full_status_has_no_forbidden_parallel_roots() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert status["no_parallel_world_guard_status"]["forbidden_parallel_world_roots"] == (
        FORBIDDEN_PARALLEL_WORLD_ROOTS
    )
    assert status["no_parallel_world_guard_status"]["forbidden_parallel_world_roots_present"] == ()
    assert all(not Path(root).exists() for root in FORBIDDEN_PARALLEL_WORLD_ROOTS)


def test_jarvis_live_full_status_cli_renderer_shows_next_and_commands_dynamically() -> None:
    status = build_jarvis_live_full_roadmap_status()
    rendered = render_status(status)

    ready_batches = ", ".join(status["ready_batches"])
    next_batch = status["next_batch"]
    assert next_batch is not None

    assert f"ready_batches={ready_batches}" in rendered
    assert f"next_batch={next_batch['batch_id']}" in rendered
    assert XRAY_COMMAND_HINT in rendered
    assert DRIFT_COMMAND_HINT in rendered
    assert FULL_AUTO_COMMAND_HINT in rendered


def test_jarvis_live_full_status_cli_renderer_reports_jl3_after_jl2_files_exist() -> None:
    status = build_jarvis_live_full_roadmap_status()
    rendered = render_status(status)

    if "JL-2" in status["ready_batches"]:
        assert "ready_batches=JL-0, JL-1, JL-2" in rendered
        assert "next_batch=JL-3" in rendered
