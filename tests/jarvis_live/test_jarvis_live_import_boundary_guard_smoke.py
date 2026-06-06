from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_roadmap_expected_files_contract import (
    FORBIDDEN_PARALLEL_WORLD_ROOTS,
    list_jarvis_live_roadmap_expected_paths,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_roadmap_status_builder import (
    build_jarvis_live_roadmap_status,
)
from tools.project_readiness_control import jarvis_live_roadmap_expected_files as wrapper


STATUS_BUILDER_PATH = Path(
    "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/"
    "jarvis_live_roadmap_status_builder.py"
)


def test_jarvis_live_status_builder_uses_core_contract_not_tools() -> None:
    source = STATUS_BUILDER_PATH.read_text(encoding="utf-8")

    assert "tools.project_readiness_control" not in source
    assert (
        "MAKSIMAR_CORE_LIB.ai_orchestration."
        "jarvis_live_roadmap_expected_files_contract"
    ) in source


def test_jarvis_live_status_builder_still_blocks_runtime_and_control() -> None:
    status = build_jarvis_live_roadmap_status()

    assert status["roadmap_ready"] is True
    assert status["runtime_start_allowed"] is False
    assert status["model_download_allowed"] is False
    assert status["microphone_enabled"] is False
    assert status["stt_runtime_enabled"] is False
    assert status["tts_playback_enabled"] is False
    assert status["app_control_allowed"] is False
    assert status["shell_control_allowed"] is False
    assert status["forbidden_parallel_world_roots_present"] == ()


def test_jarvis_live_tools_wrapper_exports_core_expected_paths() -> None:
    assert (
        wrapper.list_jarvis_live_roadmap_expected_paths()
        == list_jarvis_live_roadmap_expected_paths()
    )
    assert wrapper.FORBIDDEN_PARALLEL_WORLD_ROOTS == FORBIDDEN_PARALLEL_WORLD_ROOTS


def test_jarvis_live_no_new_parallel_roots_are_introduced() -> None:
    status = build_jarvis_live_roadmap_status()

    assert status["forbidden_parallel_world_roots"] == FORBIDDEN_PARALLEL_WORLD_ROOTS
    assert status["forbidden_parallel_world_roots_present"] == ()
    assert all(not Path(root).exists() for root in FORBIDDEN_PARALLEL_WORLD_ROOTS)
