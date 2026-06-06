from __future__ import annotations

from MAKSIMAR_SERVER.AI_ORCHESTRATION.adapters.model_worker_binding_adapter import (
    build_model_worker_binding_read_model,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_model_worker_binding_adapter_is_read_only_dashboard_safe() -> None:
    read_model = build_model_worker_binding_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["role_count"] > 0
    assert read_model["alias_count"] > 0
    assert read_model["canonical_worker_ids"] == (
        "worker_ai_001",
        "worker_sim_001",
        "worker_voice_001",
    )
    assert read_model["reused_existing_worker_registry"] is True
    assert read_model["new_worker_registry_created"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["shell_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False


def test_jarvis_roadmap_marks_jl3_ready_and_keeps_download_blocked() -> None:
    status = build_jarvis_live_full_roadmap_status()
    per_batch = {
        str(entry["batch_id"]): entry
        for entry in status["per_batch_status"]
    }

    assert per_batch["JL-3"]["ready"] is True

    if status["next_batch"] is not None:
        assert status["next_batch"]["batch_id"] != "JL-3"

    assert status["model_download_allowed_now"] is False
    assert status["download_gate_status"]["model_download_allowed_now"] is False
