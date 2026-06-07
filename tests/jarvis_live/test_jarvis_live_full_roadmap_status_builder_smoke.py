from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_jarvis_live_full_status_tracks_ready_batches_and_next_batch_dynamically() -> None:
    status = build_jarvis_live_full_roadmap_status()

    assert status["total_batches"] == 15
    assert "JL-0" in status["ready_batches"]
    assert "JL-1" in status["ready_batches"]

    expected_next = next(
        (
            entry
            for entry in status["per_batch_status"]
            if entry["ready"] is False
        ),
        None,
    )

    if expected_next is None:
        assert status["next_batch"] is None
    else:
        assert status["next_batch"] is not None
        assert status["next_batch"]["batch_id"] == expected_next["batch_id"]


def test_jarvis_live_full_status_exposes_totals_and_gates() -> None:
    status = build_jarvis_live_full_roadmap_status()
    ready_batches = set(status["ready_batches"])

    assert status["expected_file_count_total"] > 0
    assert status["existing_file_count_total"] >= 10
    if status["next_batch"] is None:
        assert status["missing_file_count_total"] == 0
    else:
        assert status["missing_file_count_total"] > 0
    assert status["download_gate_status"]["storage_boundary_ready"] == ("JL-4" in ready_batches)
    assert status["download_gate_status"]["vendor_boundary_ready"] == ("JL-10" in ready_batches)
    assert status["model_download_allowed_now"] == ("JL-10" in ready_batches)
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


def test_jarvis_live_full_status_keeps_runtime_voice_and_pc_gates_blocked() -> None:
    status = build_jarvis_live_full_roadmap_status()
    ready_batches = set(status["ready_batches"])

    assert status["model_download_allowed_now"] == ("JL-10" in ready_batches)
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False
    assert status["download_gate_status"]["model_download_allowed_now"] == ("JL-10" in ready_batches)
    assert status["voice_gate_status"]["first_voice_batch"] == "JL-11"
    assert status["pc_control_gate_status"]["first_pc_control_batch"] == "JL-14"
