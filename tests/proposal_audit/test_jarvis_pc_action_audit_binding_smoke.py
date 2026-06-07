from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    build_jarvis_pc_action_adapter_contract,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_approval_binding import (
    build_jarvis_pc_action_approval_binding,
)


def test_jarvis_pc_action_audit_binding_requirements_are_visible() -> None:
    adapter = build_jarvis_pc_action_adapter_contract().to_read_model()
    approval = build_jarvis_pc_action_approval_binding().to_read_model()

    assert adapter["audit_required"] is True
    assert adapter["approval_required"] is True
    assert adapter["allowlist_required"] is True
    assert approval["audit_record_required"] is True
    assert approval["owner_approval_required"] is True
    assert approval["bypass_approval_allowed"] is False
    assert approval["bypass_audit_allowed"] is False
    assert approval["pc_control_allowed"] is False

    root = Path(__file__).resolve().parents[2]
    text = (root / "WORKFLOW_ENGINE/config/jarvis_pc_action_allowlist.yaml").read_text(
        encoding="utf-8"
    )
    assert text.count("requires_audit: true") == 5
    assert text.count("requires_approval: true") == 5


def test_jl14_ready_finishes_printed_roadmap_without_opening_pc_control() -> None:
    status = build_jarvis_live_full_roadmap_status()
    per_batch = {str(entry["batch_id"]): entry for entry in status["per_batch_status"]}

    assert per_batch["JL-14"]["ready"] is True
    assert status["next_batch"] is None
    assert status["model_download_allowed_now"] is True
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False

