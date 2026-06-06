from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_roadmap_status_builder import (
    build_jarvis_live_roadmap_status,
)
from tools.project_readiness_control.jarvis_live_roadmap_expected_files import (
    JARVIS_LIVE_ROADMAP_EXPECTED_FILES,
)


def test_jarvis_live_roadmap_status_builder_is_read_only_and_ready() -> None:
    status = build_jarvis_live_roadmap_status()

    assert status["summary_id"] == "jarvis_live_roadmap_status_v0_1"
    assert status["roadmap_id"] == "JARVIS-LIVE"
    assert status["batch_id"] == "JL-0"
    assert status["read_only"] is True
    assert status["dashboard_safe"] is True
    assert status["runtime_start_allowed"] is False
    assert status["model_download_allowed"] is False
    assert status["microphone_enabled"] is False
    assert status["stt_runtime_enabled"] is False
    assert status["tts_playback_enabled"] is False
    assert status["app_control_allowed"] is False
    assert status["shell_control_allowed"] is False


def test_jarvis_live_roadmap_status_tracks_expected_files() -> None:
    status = build_jarvis_live_roadmap_status()

    assert status["expected_file_count"] == len(JARVIS_LIVE_ROADMAP_EXPECTED_FILES)
    assert status["expected_file_count"] == 6
    assert status["missing_expected_file_count"] == 0
    assert status["roadmap_ready"] is True
    assert (
        "docs/architecture/jarvis_live/jarvis_live_no_drift_rules_v0.md"
        in status["expected_paths"]
    )
