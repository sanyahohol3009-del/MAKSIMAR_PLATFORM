from __future__ import annotations

import pytest
import CONTROL_PLANE.api_server as api_server
from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store


@pytest.fixture(autouse=True)
def isolate_mocked_hotpath_memory(monkeypatch, tmp_path):
    # Exercise real capture while preventing mocked chat from entering user data.
    monkeypatch.setattr(session_memory_store, "SESSION_MEMORY_ROOT", tmp_path / "session_memory")
    monkeypatch.setattr(session_memory_store, "SESSION_STATE_PATH", tmp_path / "session_memory" / "state.json")
    monkeypatch.setattr(api_server, "CANONICAL_SESSION_CONTEXT", session_memory_store.CanonicalSessionContextStore())


def _canonical_result(**overrides):
    result = {
        "response_text": "Готово.",
        "operation_status": "COMPLETE",
        "orchestration_path": "canonical_semantic_turn_v2",
        "trace_id": "trace-model-selection",
        "understanding_schema_version": "request_understanding.v2",
        "understanding": {"current_topic": "capabilities", "unresolved_reference": ""},
        "selected_capabilities": ("conversation.respond",),
        "selected_provider_operation": ("respond",),
        "selection_source": "model_semantic_registry",
        "trace": {"trace_id": "trace-model-selection"},
    }
    result.update(overrides)
    return result


def test_hot_response_projects_selected_capability_fields(monkeypatch) -> None:
    monkeypatch.setattr(
        api_server,
        "run_canonical_semantic_turn",
        lambda **_: _canonical_result(selected_capability_id="conversation.respond"),
    )
    payload = api_server.jarvis_live_hot({"text": "что ты умеешь", "session_id": "test"})
    assert payload["selection_source"] == "model_semantic_registry"
    assert payload["orchestration_path"] == "canonical_semantic_turn_v2"


def test_hotpath_passes_voice_text_to_semantic_spine_without_preselection(monkeypatch) -> None:
    captured = {}
    expected_projection = api_server._semantic_capability_projection()
    monkeypatch.setattr(api_server, "_semantic_capability_projection", lambda: expected_projection)

    def canonical(**kwargs):
        captured.update(kwargs)
        return _canonical_result(operation_status="UNRESOLVED_OPERATION")

    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", canonical)
    payload = api_server.jarvis_live_hot({"text": "Жарис закрою опером точка", "session_id": "test"})
    assert captured["text"] == "Жарис закрою опером точка"
    assert payload["selected_capability_id"] == "conversation.respond"
    assert captured["registry_projection"] is expected_projection
    assert {"conversation.respond", "project.read", "mempalace_search"}.issubset(
        {entry["capability_id"] for entry in expected_projection["entries"]})
    assert payload["selection_source"] == "model_semantic_registry"


def test_hot_response_preserves_canonical_model_selection_source(monkeypatch) -> None:
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: _canonical_result())
    payload = api_server.jarvis_live_hot({"text": "используй smolagents для плана агента", "session_id": "test"})
    assert payload["orchestration_path"] == "canonical_semantic_turn_v2"
    assert payload["selection_source"] == "model_semantic_registry"


def test_hot_response_projects_canonical_route_without_local_term_precedence(monkeypatch) -> None:
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: _canonical_result())
    payload = api_server.jarvis_live_hot({"text": "проверь весь проект и агентов", "session_id": "test"})
    assert payload["route"] == "CANONICAL_SEMANTIC_TURN"


def test_hotpath_permanent_memory_write_is_guarded(monkeypatch) -> None:
    monkeypatch.setattr(
        api_server,
        "run_canonical_semantic_turn",
        lambda **_: _canonical_result(operation_status="APPROVAL_REQUIRED"),
    )
    payload = api_server.jarvis_live_hot({"text": "Запиши это в постоянную память", "session_id": "test"})
    assert payload["approval_required"] is True
    assert payload["canonical_memory_write_allowed"] is False


def test_mocked_hotpath_capture_writes_the_isolated_canonical_journal(monkeypatch, tmp_path):
    import json
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: _canonical_result())
    api_server.jarvis_live_hot({"text": "isolated fixture only", "session_id": "isolated_test"})
    source = session_memory_store._session_turn_log_path()
    assert source.is_relative_to(tmp_path) and source.is_file()
    rows = [json.loads(line) for line in source.read_text().splitlines()]
    assert len(rows) == 1 and rows[0]["trace_id"] == "trace-model-selection"


@pytest.mark.parametrize("compute_provider", ["codex_cli", "local_model"])
def test_accepted_proposal_delivery_does_not_become_verified_execution(monkeypatch, compute_provider):
    import hashlib
    import json
    from types import SimpleNamespace
    observation = json.dumps({"proposal": "Proposed design; no action executed", "proposal_only": True,
        "compute_provider": compute_provider})
    item = {"kind": "code_proposal", "observation": observation,
        "content_hash": "sha256:" + hashlib.sha256(observation.encode()).hexdigest(),
        "source_reference": "proposal://isolated-fixture", "observed_at": "2026-10-12T16:00:00Z",
        "step_id": "proposal_step"}
    result = _canonical_result(evidence_bundle={"status": "COMPLETE", "items": [item],
        "receipts": [{"schema_version": "execution_receipt.v1", "request_id": "proposal_request",
            "trace_id": "trace-model-selection", "step_id": "proposal_step", "receipt_id": "proposal:delivery",
            "capability_id": "code.proposal.generate", "operation_id": "generate_code_proposal",
            "provider_id": "existing_model_role_adapter", "status": "COMPLETE"}]})
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: result)
    monkeypatch.setattr(api_server, "audit_proposal_runtime", lambda _: SimpleNamespace(
        verdict="ACCEPTED_FOR_EXPERIMENT", to_read_model=lambda: {"verdict": "ACCEPTED_FOR_EXPERIMENT"}))
    captured = api_server.jarvis_live_hot({"text": "isolated proposed design", "session_id": "proposal_test"})["result"]
    experience = captured["proposal_learning"]
    assert experience["actor"] == ("CODEX" if compute_provider == "codex_cli" else "JARVIS")
    assert experience["verification_status"] == "PENDING"
    assert experience["training_eligible"] is False and experience["training_export_allowed"] is False
    assert experience["verification_refs"] == ()
    assert captured["learning_bundle"]["accepted"] is True
    assert captured["learning_bundle"]["training_eligible"] is False
    rows = [json.loads(line) for line in session_memory_store._session_turn_log_path().read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["artifact"]["learning_experience"]["verification_status"] == "PENDING"
    assert rows[0]["artifact"]["execution_receipts"][0]["receipt_id"] == "proposal:delivery"
