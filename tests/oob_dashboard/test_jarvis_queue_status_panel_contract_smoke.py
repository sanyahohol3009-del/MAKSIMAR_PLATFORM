from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_queue_status_panel_contract import (
    build_jarvis_queue_status_panel_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model import (
    build_jarvis_live_observability_read_model,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_jarvis_queue_status_panel_is_read_only_and_blocked() -> None:
    panel = build_jarvis_queue_status_panel_contract().to_read_model()

    assert panel["read_only"] is True
    assert panel["dashboard_safe"] is True
    assert panel["queue_status"] == "blocked"
    assert panel["queue_pressure"] == "none"
    assert panel["queue_length"] == 0
    assert panel["active_task_count"] == 0
    assert panel["queued_task_count"] == 0
    assert panel["queue_execution_allowed"] is False
    assert panel["dashboard_execution_allowed"] is False


def test_jarvis_live_observability_read_model_aggregates_panels() -> None:
    roadmap_status = build_jarvis_live_full_roadmap_status()
    read_model = build_jarvis_live_observability_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["model_download_allowed"] == roadmap_status["model_download_allowed_now"]
    assert "live_status_panel" in read_model
    assert "model_status_panel" in read_model
    assert "resource_status_panel" in read_model
    assert "queue_status_panel" in read_model
    assert read_model["gates"]["model_download_allowed"] == roadmap_status["model_download_allowed_now"]
    assert read_model["gates"]["runtime_start_allowed"] is False
    assert read_model["gates"]["voice_allowed"] is False
    assert read_model["gates"]["pc_control_allowed"] is False


def test_observability_source_has_no_execution_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root
        / "MAKSIMAR_SERVER/OBSERVABILITY/jarvis_live/jarvis_live_observability_read_model.py"
    ).read_text(encoding="utf-8").lower()

    forbidden = (
        "subprocess",
        "os.system",
        "shell=true",
        "start_runtime(",
        "execute_action(",
        "run_task(",
        "webbrowser",
        "pyautogui",
        "keyboard.",
        "mouse.",
    )

    for marker in forbidden:
        assert marker not in source
