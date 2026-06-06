from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.external_task_broker_audit_binding import (
    build_external_task_broker_audit_binding_read_model,
)


def test_external_task_broker_audit_binding_is_proposal_only() -> None:
    read_model = build_external_task_broker_audit_binding_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["broker_count"] == 2
    assert read_model["proposal_only"] is True
    assert read_model["audit_event_kind"] == "external_task_broker_proposal"
    assert read_model["audit_required"] is True
    assert read_model["approval_required"] is True
    assert read_model["preview_required"] is True
    assert read_model["allowlist_required"] is True
    assert read_model["direct_execution_allowed"] is False
    assert read_model["local_mutation_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["pc_control_allowed"] is False


def test_jl9_ready_keeps_external_brokers_proposal_only() -> None:
    status = build_jarvis_live_full_roadmap_status()
    per_batch = {str(entry["batch_id"]): entry for entry in status["per_batch_status"]}

    assert per_batch["JL-9"]["ready"] is True

    if status["next_batch"] is not None:
        assert status["next_batch"]["batch_id"] != "JL-9"

    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False


def test_external_task_broker_sources_have_no_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    paths = (
        root / "MAKSIMAR_CORE_LIB/ai_orchestration/external_task_broker_contract.py",
        root / "MAKSIMAR_SERVER/AI_ORCHESTRATION/external_task_broker_read_model.py",
        root / "MAKSIMAR_SERVER/PROPOSAL_AUDIT/external_task_broker_audit_binding.py",
    )
    forbidden = (
        "requests",
        "httpx",
        "openai",
        "google.generativeai",
        "subprocess",
        "os.system",
        "shell=true",
        "webbrowser",
        "socket",
        "pyautogui",
        "keyboard",
        "mouse",
        "git commit",
        "git push",
    )

    for path in paths:
        source = path.read_text(encoding="utf-8").lower()
        for marker in forbidden:
            assert marker not in source

