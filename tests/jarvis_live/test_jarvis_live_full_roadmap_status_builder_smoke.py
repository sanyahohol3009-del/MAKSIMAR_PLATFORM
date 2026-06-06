from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_jarvis_live_full_status_marks_jl0_and_jl1_ready_and_jl2_next() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert status["total_batches"] == 15
    assert "JL-0" in status["ready_batches"]
    assert "JL-1" in status["ready_batches"]
    assert status["next_batch"]["batch_id"] == "JL-2"
    assert status["blocked_batches"][0] == "JL-2"


def test_jarvis_live_full_status_exposes_totals_and_gates() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert status["expected_file_count_total"] > 0
    assert status["existing_file_count_total"] >= 10
    assert status["missing_file_count_total"] > 0
    assert status["download_gate_status"]["storage_boundary_ready"] is False
    assert status["download_gate_status"]["vendor_boundary_ready"] is False
    assert status["model_download_allowed_now"] is False
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False
    assert status["no_parallel_world_guard_status"]["ready"] is True


def test_jarvis_live_full_status_builder_is_dashboard_safe_read_only() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert status["read_only"] is True
    assert status["dashboard_safe"] is True
    assert status["runtime_started"] is False
    assert status["model_download_started"] is False
    assert status["audio_runtime_started"] is False
    assert status["pc_control_started"] is False
