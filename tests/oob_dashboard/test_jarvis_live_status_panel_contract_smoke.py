from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_live_status_panel_contract import (
    build_jarvis_live_status_panel_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_jarvis_live_status_panel_is_read_only_and_blocked() -> None:
    roadmap_status = build_jarvis_live_full_roadmap_status()
    panel = build_jarvis_live_status_panel_contract(roadmap_status).to_read_model()

    assert panel["read_only"] is True
    assert panel["dashboard_safe"] is True
    assert panel["dashboard_execution_allowed"] is False
    assert panel["model_download_allowed"] is False
    assert panel["runtime_start_allowed"] is False
    assert panel["voice_allowed"] is False
    assert panel["pc_control_allowed"] is False
    assert panel["blocked_reason"]
    assert panel["next_roadmap_batch"]


def test_jl8_ready_moves_next_batch_to_jl9_and_gates_stay_closed() -> None:
    roadmap_status = build_jarvis_live_full_roadmap_status()
    per_batch = {
        str(entry["batch_id"]): entry
        for entry in roadmap_status["per_batch_status"]
    }

    assert per_batch["JL-8"]["ready"] is True
    assert roadmap_status["next_batch"]["batch_id"] == "JL-9"
    assert roadmap_status["model_download_allowed_now"] is False
    assert roadmap_status["runtime_start_allowed_now"] is False
    assert roadmap_status["voice_allowed_now"] is False
    assert roadmap_status["pc_control_allowed_now"] is False

