from __future__ import annotations

import CONTROL_PLANE.api_server as api_server
import pytest
import hashlib
import json
from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store
from MAKSIMAR_CORE_LIB.security_layer.host_principal import bootstrap_local_owner_token


@pytest.fixture(autouse=True)
def isolate_existing_hot_endpoint_state(monkeypatch, tmp_path):
    """Contract tests must never append fixtures to the owner's live journal."""
    from MAKSIMAR_CORE_LIB.security_layer import host_principal
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "1")
    monkeypatch.setattr(session_memory_store, "SESSION_MEMORY_ROOT", tmp_path / "session_memory")
    monkeypatch.setattr(session_memory_store, "SESSION_STATE_PATH", tmp_path / "session_memory" / "state.json")
    monkeypatch.setattr(api_server, "CANONICAL_SESSION_CONTEXT", session_memory_store.CanonicalSessionContextStore())
    # Auth/session contracts do not probe Windows, providers or live runtime health.
    # Individual projection tests can supply their own controlled readiness result.
    monkeypatch.setattr(api_server, "_legacy_runtime_readiness_payload", lambda: {})
    monkeypatch.setenv("JARVIS_HOST_AUTH_SECRET", "isolated-hot-contract-test-secret")
    monkeypatch.setattr(host_principal, "HOST_SECRET_PATH", tmp_path / "security" / "host_secret")
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model
    monkeypatch.setattr(jarvis_live_observability_read_model, "_IN_FLIGHT_TRACE_FILE", tmp_path / "trace.jsonl")


def canonical_result(*, status="COMPLETE", effect="OBSERVE", capability="conversation.respond",
                     operation="respond", receipt=None):
    trace_id = "trace_hot_contract"
    return {
        "handled": True,
        "orchestration_path": "canonical_semantic_turn_v2",
        "trace_id": trace_id,
        "understanding_schema_version": "request_understanding.v2",
        "understanding": {
            "effect_type": effect, "current_topic": "test topic",
            "required_capabilities": ({"capability_id": capability, "required": True},),
            "operation_requirements": ({"operation_id": operation, "required": True},),
        },
        "selected_capabilities": (capability,),
        "selected_provider_operation": (operation,),
        "selection_source": "model_semantic_registry",
        "fallback_used": False,
        "fallback_reason": "",
        "capability_status": "AVAILABLE",
        "operation_status": status,
        "response_text": "Непустой grounded ответ.",
        "permission_decision": {"capability_id": capability, "granted": status == "COMPLETE",
                                "approval_required": status == "APPROVAL_REQUIRED"},
        "evidence_bundle": {"trace_id": trace_id, "items": (), "receipts": (receipt,) if receipt else ()},
        "execution_plan": {"steps": ({"capability_id": capability, "operation": operation},)
                                      if capability == "pc.control" else ()},
        "trace": {"trace_id": trace_id, "route": "canonical_semantic_turn_v2"},
        "project_tools_used": capability == "project.read",
    }


def trusted_owner_payload():
    session_id = "trusted_owner_contract"
    return {
        "text": "обычный semantic turn", "session_id": session_id,
        "host_auth_token": bootstrap_local_owner_token(session_id=session_id),
        "identity": {
            "identity_id": "aleksandr", "source": "local_terminal_session",
            "profile_type": "owner", "verified": True, "trusted_session": True,
        },
    }


@pytest.mark.parametrize("streaming", [False, True])
def test_both_hot_modes_persist_qualified_evidence_and_receipts_across_restart(monkeypatch, tmp_path, streaming):
    monkeypatch.setattr(session_memory_store, "SESSION_MEMORY_ROOT", tmp_path)
    monkeypatch.setattr(api_server, "CANONICAL_SESSION_CONTEXT", session_memory_store.CanonicalSessionContextStore())
    request = trusted_owner_payload()
    request["trace_id"] = "trace_hot_contract"
    canonical = canonical_result(capability="mempalace_search", operation="search_mempalace")
    binding = {"request_id": "request_capture", "trace_id": "trace_hot_contract", "step_id": "s1",
               "capability_id": "mempalace_search", "operation_id": "search_mempalace", "provider_id": "memory.retrieve"}
    observation = json.dumps({"retrieval": {"results": [{"source_readback": [{"source_path": "docs/real.md", "freshness": "FRESH"}]}]}})
    item = {**binding, "kind": "mempalace_search", "observation": observation,
            "content_hash": "sha256:" + hashlib.sha256(observation.encode()).hexdigest(),
            "observed_at": "2026-10-11T12:30:00Z", "source_reference": "native://drawer1"}
    receipt = {**binding, "schema_version": "execution_receipt.v1", "status": "COMPLETE", "receipt_id": "receipt_capture"}
    canonical["evidence_bundle"] = {"status": "COMPLETE", "items": [item], "receipts": [receipt]}
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: canonical)
    captured = {}
    def stream(**kwargs):
        captured.update(kwargs)
        yield {"event": "chunk", "chunk": "Непустой grounded ответ."}
        yield {"event": "done", "trace_id": canonical["trace_id"], "result": canonical}
    monkeypatch.setattr(api_server, "stream_canonical_semantic_turn", stream)
    if streaming:
        events = [json.loads(line) for line in api_server._hot_stream_lines(request)]
        result = events[-1]["result"]
        assert captured["session_id"] == request["session_id"] and captured["trace_id"] == request["trace_id"]
    else:
        result = api_server.jarvis_live_hot(request)["result"]
    records = [json.loads(line) for line in (tmp_path / session_memory_store.SESSION_TURN_LOG_NAME).read_text().splitlines()]
    assert len(records) == 1
    projection = session_memory_store.canonical_experience_projection(records[0])
    assert projection["verification_status"] == "VERIFIED"
    assert projection["audit_verdict"] == "EXECUTION_RECEIPTS_VERIFIED"
    assert projection["execution_receipts"] == (receipt,)
    assert records[0]["artifact"]["retrieval_trace"]["sources"][0]["source_path"] == "docs/real.md"
    assert records[0]["artifact"]["retrieval_trace"]["payload_copied"] is False
    identity = api_server._identity_from_hot_payload(request, request["session_id"])
    restored = session_memory_store.CanonicalSessionContextStore().read(request["session_id"], identity)
    assert restored["bounded_chronological_turns"][-1]["trace_id"] == "trace_hot_contract"
    assert result["learning_bundle"]["accepted"] is True


def test_hot_endpoint_separates_owner_eligibility_from_current_turn_pc_authorization(monkeypatch):
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: canonical_result())
    payload = api_server.jarvis_live_hot(trusted_owner_payload())

    assert payload["route"] == "CANONICAL_SEMANTIC_TURN"
    assert payload["legacy_command_path_used"] is False
    assert payload["response_text"]
    assert payload["result"]["selection_source"] == "model_semantic_registry"
    assert payload["result"]["fallback_used"] is False
    assert payload["result"]["session_event"]["trace_id"] == payload["result"]["trace_id"]
    assert payload["owner_pc_action_eligible"] is True
    assert payload["policy_execution_allowed"] is False
    assert payload["pc_executor_available"] is None
    assert payload["pc_operation_authorized_for_this_turn"] is False
    assert payload["executed"] is False
    assert payload["execution_receipt"] is None
    assert payload["pc_control_allowed"] is False


def test_hot_endpoint_ignores_caller_identity_claims_without_host_principal(monkeypatch):
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: canonical_result())
    payload = api_server.jarvis_live_hot({
        "text": "увеличь громкость", "session_id": "spoof_contract",
        "identity": {
            "identity_id": "fake-owner", "source": "local_terminal_session",
            "profile_type": "owner", "verified": True, "trusted_session": True,
        },
    })
    assert payload["owner_pc_action_eligible"] is False
    assert payload["pc_operation_authorized_for_this_turn"] is False


def test_hot_endpoint_expected_capability_is_validation_not_selection_force(monkeypatch):
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: canonical_result())
    request = trusted_owner_payload()
    request["expected_capability_id"] = "content.metadata.generate"
    payload = api_server.jarvis_live_hot(request)
    assert payload["operation_status"] == "SAFETY_VALIDATION_FAILED"
    assert payload["selected_capabilities"] == ("conversation.respond",)
    assert payload["result"]["expected_capability_validation"]["status"] == "MISMATCH"


@pytest.mark.parametrize("identity", [
    None,
    {"identity_id": "aleksandr", "source": "local_terminal_session", "profile_type": "owner", "verified": False, "trusted_session": True},
    {"identity_id": "unknown", "source": "voice_unverified", "profile_type": "unknown", "verified": False},
    {"identity_id": "aleksandr", "source": "remote_http", "profile_type": "owner", "verified": True, "trusted_session": False},
])
def test_anonymous_or_untrusted_http_never_receives_owner_rights(monkeypatch, identity):
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", lambda **_: canonical_result())
    request = {"text": "status", "session_id": "untrusted_contract"}
    if identity is not None:
        request["identity"] = identity
    payload = api_server.jarvis_live_hot(request)
    assert payload["owner_pc_action_eligible"] is False
    assert payload["policy_execution_allowed"] is False
    assert payload["pc_executor_available"] is None
    assert payload["pc_operation_authorized_for_this_turn"] is False
    assert payload["executed"] is False
    assert payload["execution_receipt"] is None
    assert payload["pc_control_allowed"] is False


def test_typed_pc_step_projects_policy_health_authorization_and_valid_receipt(monkeypatch):
    receipt = {"trace_id": "trace_hot_contract", "status": "EXECUTED", "operation_id": "open_browser"}
    monkeypatch.setattr(
        api_server, "run_canonical_semantic_turn",
        lambda **_: canonical_result(capability="pc.control", operation="open_browser", receipt=receipt),
    )
    monkeypatch.setattr(api_server, "_legacy_runtime_readiness_payload",
                        lambda: {"pc_executor_available": True})

    payload = api_server.jarvis_live_hot(trusted_owner_payload())

    assert payload["owner_pc_action_eligible"] is True
    assert payload["policy_execution_allowed"] is True
    assert payload["pc_executor_available"] is True
    assert payload["pc_operation_authorized_for_this_turn"] is True
    assert payload["executed"] is True
    assert payload["execution_receipt"] == receipt
    assert payload["pc_control_allowed"] is True


def test_requested_mutation_remains_mutation_and_is_not_executed_as_read_only(monkeypatch):
    monkeypatch.setattr(
        api_server, "run_canonical_semantic_turn",
        lambda **_: canonical_result(status="APPROVAL_REQUIRED", effect="MUTATE", capability="project.files.write"),
    )
    payload = api_server.jarvis_live_hot(trusted_owner_payload())
    result = payload["result"]
    assert result["understanding"]["effect_type"] == "MUTATE"
    assert result["selected_capabilities"] == ("project.files.write",)
    assert result["approval_required"] is True
    assert result["direct_allowed"] is False
    assert result["canonical_memory_write_allowed"] is False


@pytest.mark.parametrize("streaming", [False, True], ids=["command", "stream"])
def test_terminal_signed_context_reaches_both_canonical_modes(monkeypatch, tmp_path, streaming):
    from tools.jarvis_live_runtime import jarvis_live_terminal_chat as terminal
    from MAKSIMAR_CORE_LIB.security_layer import host_principal
    observed = []
    def result(**kwargs):
        observed.append(kwargs["identity"])
        return canonical_result()
    def stream(**kwargs):
        observed.append(kwargs["identity"])
        yield {"event": "done", "result": canonical_result()}
    monkeypatch.setattr(api_server, "run_canonical_semantic_turn", result)
    monkeypatch.setattr(api_server, "stream_canonical_semantic_turn", stream)
    request = terminal._build_hot_payload("signed terminal context")
    verified = host_principal.identity_from_host_token(request["host_auth_token"])
    assert verified is not None
    assert verified[0].session_id == request["session_id"] == terminal.SESSION_ID
    if streaming:
        request["stream"] = True
        events = [json.loads(line) for line in api_server._hot_stream_lines(request)]
        response = events[-1]["result"]
        assert events[-1]["event"] == "done"
        assert response["session_event"]["session_id"] == terminal.SESSION_ID
        # Streaming retains the canonical result shape, not the sync HTTP envelope.
        pc_truth = api_server._pc_turn_truth(response, verified[1])
    else:
        response = api_server.jarvis_live_hot(request)
        pc_truth = response
    assert len(observed) == 1
    assert observed[0] == verified[1] and observed[0].owner_authorized
    assert pc_truth["owner_pc_action_eligible"] is True
    assert pc_truth["pc_operation_authorized_for_this_turn"] is False
    assert pc_truth["executed"] is False
    assert pc_truth["execution_receipt"] is None
    # The existing trace and memory owners must not persist the credential.
    for path in tmp_path.rglob("*.json*"):
        assert request["host_auth_token"] not in path.read_text()


@pytest.mark.parametrize("case", ["missing", "forged", "expired", "wrong_session", "non_owner", "json_owner"])
def test_existing_hot_auth_negative_contexts_never_grant_owner(case):
    from MAKSIMAR_CORE_LIB.security_layer import host_principal as host
    session = "isolated_auth_negative"
    request = {"session_id": session}
    if case not in {"missing", "json_owner"}:
        principal = host.HostPrincipal("synthetic-owner", "other" if case == "wrong_session" else session,
                                       "child" if case == "non_owner" else "owner")
        token = host.issue_host_token(principal, ttl_seconds=-1 if case == "expired" else 300)
        request["host_auth_token"] = token + ".invalid" if case == "forged" else token
    if case == "json_owner":
        request["identity"] = {"identity_id": "aleksandr", "source": "local_terminal_session",
                               "profile_type": "owner", "verified": True, "trusted_session": True}
    identity = api_server._identity_from_hot_payload(request, session)
    assert identity.owner_authorized is False
    assert identity.identity_id == "anonymous"


def test_existing_host_principal_other_owner_binding_debt_is_explicit():
    from MAKSIMAR_CORE_LIB.security_layer import host_principal as host
    # Characterization of OPEN hardening debt, not evidence of OS-owner binding.
    token = host.issue_host_token(host.HostPrincipal("different-signed-owner", "debt_session"))
    identity = api_server._identity_from_hot_payload({"host_auth_token": token}, "debt_session")
    assert identity.identity_id == "different-signed-owner"
    assert identity.owner_authorized is True


def test_existing_non_ascii_signature_debt_is_explicit():
    from MAKSIMAR_CORE_LIB.security_layer import host_principal as host
    # Reachable malformed JSON token; the unchanged owner still raises here.
    with pytest.raises(TypeError):
        host.verify_host_token("body.подпись")
