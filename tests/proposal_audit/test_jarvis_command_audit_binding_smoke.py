from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.jarvis_action_allowlist_contract import (
    ALLOWED_JARVIS_ACTION_CANDIDATES,
    FORBIDDEN_JARVIS_ACTIONS,
)
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.jarvis_command_audit_binding import (
    build_jarvis_command_audit_binding_read_model,
)


def test_jarvis_command_audit_binding_is_proposal_only() -> None:
    read_model = build_jarvis_command_audit_binding_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["proposal_only"] is True
    assert read_model["execution_enabled"] is False
    assert read_model["audit_required"] is True
    assert read_model["approval_required"] is True
    assert read_model["preview_required"] is True
    assert read_model["allowlist_required"] is True
    assert read_model["audit_event_kind"] == "jarvis_command_proposal"
    assert read_model["allowed_action_ids"] == ALLOWED_JARVIS_ACTION_CANDIDATES
    assert read_model["forbidden_actions"] == FORBIDDEN_JARVIS_ACTIONS


def test_jarvis_command_audit_binding_source_has_no_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root / "MAKSIMAR_SERVER/PROPOSAL_AUDIT/jarvis_command_audit_binding.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()

    for marker in (
        "subprocess",
        "os.system",
        "shell=true",
        "pyautogui",
        "keyboard",
        "mouse",
        "webbrowser.open",
        "requests",
        "socket",
        "git commit",
        "git push",
    ):
        assert marker not in lowered



def test_proposal_runtime_audit_does_not_classify_authority_from_prose(monkeypatch) -> None:
    from MAKSIMAR_SERVER.PROPOSAL_AUDIT import audit_proposal_runtime
    from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import self_expansion_gate
    monkeypatch.setattr(self_expansion_gate, "build_self_expansion_gate", lambda: {"gate_ready": True})
    fields = {"proposal_id": "bounded_proposal", "rollback_plan": "Discard proposal artifact",
              "validation_plan": "Review without execution", "affected_components": ("existing_owner",)}
    descriptions = ("Describe the architecture", "Explain how to run docker and powershell safely",
                    "Review a migration that may delete files", "Explain why self-approve or read secrets must be governed",
                    "Предложение: запусти shell, удали файлы; никаких действий не выполнено")
    outcomes = [audit_proposal_runtime({**fields, "proposal": text}) for text in descriptions]
    assert {result.verdict for result in outcomes} == {"ACCEPTED_FOR_EXPERIMENT"}
    assert all(result.reasons == () for result in outcomes)
    assert all(result.sandbox_required and not result.production_mutation_allowed for result in outcomes)


def test_proposal_runtime_audit_retains_typed_mutation_and_quality_checks(monkeypatch) -> None:
    from MAKSIMAR_SERVER.PROPOSAL_AUDIT import audit_proposal_runtime
    from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import self_expansion_gate
    monkeypatch.setattr(self_expansion_gate, "build_self_expansion_gate", lambda: {"gate_ready": True})
    fields = {"proposal_id": "bounded_proposal", "proposal": "Ordinary explanation",
              "rollback_plan": "Discard", "validation_plan": "Inspect", "affected_components": ("owner",)}
    for field in ("production_mutation", "auto_apply"):
        rejected = audit_proposal_runtime({**fields, field: True})
        assert rejected.verdict == "REJECTED"
        assert "production_mutation_requested" in rejected.reasons
        assert not rejected.production_mutation_allowed
    incomplete = audit_proposal_runtime({"proposal": "Ordinary explanation"})
    assert incomplete.verdict == "REVISE"
    assert set(incomplete.reasons) == {"missing_rollback", "missing_validation", "missing_grounded_scope"}
    monkeypatch.setattr(self_expansion_gate, "build_self_expansion_gate", lambda: {"gate_ready": False})
    unavailable = audit_proposal_runtime(fields)
    assert unavailable.verdict == "REVISE"
    assert "self_expansion_gate_not_ready" in unavailable.reasons
