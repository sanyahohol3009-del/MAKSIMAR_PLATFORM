from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.AI_ORCHESTRATION.live_model_download_gate_contract import (
    build_live_model_download_gate_contract,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.live_sandbox_runtime_policy import (
    build_live_sandbox_runtime_policy,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def test_live_model_download_gate_allows_controlled_planning_only() -> None:
    read_model = build_live_model_download_gate_contract().to_read_model()
    runtime_policy = build_live_sandbox_runtime_policy().to_read_model()

    assert read_model["storage_boundary_ready"] is True
    assert read_model["vendor_boundary_ready"] is True
    assert read_model["model_download_gate_ready"] is True
    assert read_model["controlled_download_allowed"] is True
    assert read_model["actual_download_started"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["model_execution_allowed"] is False
    assert read_model["voice_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["approval_required"] is True
    assert read_model["audit_required"] is True
    assert read_model["preview_required"] is True
    assert runtime_policy["controlled_download_allowed"] is True
    assert runtime_policy["actual_download_started"] is False
    assert runtime_policy["runtime_start_allowed"] is False
    assert runtime_policy["model_execution_allowed"] is False


def test_live_model_download_gate_roots_and_blocked_targets_are_correct() -> None:
    read_model = build_live_model_download_gate_contract().to_read_model()

    assert all(
        root.startswith("~/MAKSIMAR_RUNTIME/runtime_")
        for root in read_model["allowed_runtime_roots"]
    )
    for blocked in (
        "git repo",
        "MAKSIMAR_CORE_LIB",
        "MAKSIMAR_SERVER",
        "memory_engine canonical truth",
        "oob_dashboard",
        "tests",
        "docs",
    ):
        assert blocked in read_model["blocked_storage_targets"]


def test_jl10_ready_moves_next_batch_to_jl11_and_only_download_gate_opens() -> None:
    status = build_jarvis_live_full_roadmap_status()
    per_batch = {str(entry["batch_id"]): entry for entry in status["per_batch_status"]}

    assert per_batch["JL-10"]["ready"] is True
    if status["next_batch"] is not None:
        assert status["next_batch"]["batch_id"] != "JL-10"
    assert status["model_download_allowed_now"] is True
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False


def test_live_model_download_gate_sources_have_no_download_or_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    paths = (
        root / "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_model_download_gate_contract.py",
        root / "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_sandbox_runtime_policy.py",
        root / "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_sandbox_vendor_boundary_contract.py",
    )
    forbidden = (
        "requests",
        "httpx",
        "subprocess",
        "os.system",
        "curl",
        "wget",
        "ollama pull",
        "git clone",
        "pip install",
    )

    for path in paths:
        source = path.read_text(encoding="utf-8").lower()
        for marker in forbidden:
            assert marker not in source

