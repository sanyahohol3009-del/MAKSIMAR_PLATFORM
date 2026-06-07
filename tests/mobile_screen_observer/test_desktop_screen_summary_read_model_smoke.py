from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.AI_ORCHESTRATION.screen_summary_to_model_context_binding import (
    build_screen_summary_to_model_context_binding,
)
from MAKSIMAR_SERVER.MOBILE_SCREEN_OBSERVER_RUNTIME.desktop_screen_summary_read_model import (
    build_desktop_screen_summary_read_model,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_desktop_screen_summary_read_model_is_empty_and_control_free() -> None:
    read_model = build_desktop_screen_summary_read_model()
    binding = build_screen_summary_to_model_context_binding().to_read_model()

    assert read_model["screen_summary_available"] is False
    assert read_model["screen_text"] == ""
    assert read_model["visible_apps"] == []
    assert read_model["screenshot_runtime_started"] is False
    assert read_model["continuous_screen_observer_started"] is False
    assert read_model["mouse_control_allowed"] is False
    assert read_model["keyboard_control_allowed"] is False
    assert read_model["click_allowed"] is False
    assert read_model["typing_allowed"] is False
    assert read_model["app_launch_allowed"] is False
    assert read_model["browser_control_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["model_context_binding_allowed"] is True
    assert binding["model_context_binding_allowed"] is True
    assert binding["direct_model_action_allowed"] is False
    assert binding["tool_call_allowed"] is False
    assert binding["pc_control_allowed"] is False


def test_jl13_ready_moves_next_batch_to_jl14_and_keeps_gates_closed() -> None:
    status = build_jarvis_live_full_roadmap_status()
    per_batch = {str(entry["batch_id"]): entry for entry in status["per_batch_status"]}

    assert per_batch["JL-13"]["ready"] is True
    assert status["next_batch"]["batch_id"] == "JL-14"
    assert status["model_download_allowed_now"] is True
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False


def test_desktop_screen_summary_sources_have_no_runtime_control_imports() -> None:
    root = Path(__file__).resolve().parents[2]
    paths = (
        root
        / "MAKSIMAR_SERVER/MOBILE_SCREEN_OBSERVER_RUNTIME/desktop_screen_summary_read_model.py",
        root
        / "MAKSIMAR_SERVER/AI_ORCHESTRATION/screen_summary_to_model_context_binding.py",
    )
    for path in paths:
        lowered = path.read_text(encoding="utf-8").lower()
        for marker in (
            "mss",
            "pil",
            "pyautogui",
            "pynput",
            "xdotool",
            "powershell",
            "subprocess",
            "os.system",
            "webbrowser",
            "socket",
        ):
            assert marker not in lowered

