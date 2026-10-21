from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

import CONTROL_PLANE.api_server as api_server
import tools.jarvis_live_runtime.phase_1b_model_acceptance as model_acceptance
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceItem, IdentityContext, RequestDeadline,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    discover_capability_providers, load_capability_manifests,
)
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import (
    SemanticPolicyEvaluator, identity_context_from_http_payload,
)
from MAKSIMAR_CORE_LIB.security_layer.jarvis_speaker_profile_resolver import (
    resolve_family_profile,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import ExistingProjectUnderstandingAdapter


@pytest.mark.parametrize("payload,owner", [
    ({}, False),
    ({"identity": {"identity_id": "x", "source": "http", "profile_type": "unknown", "verified": False}}, False),
    ({"identity": {"identity_id": "x", "source": "http", "profile_type": "owner", "verified": False}}, False),
    ({"identity": {"identity_id": "owner", "source": "authenticated_http_session", "profile_type": "owner", "verified": True, "trusted_session": True}}, True),
    ({"identity": {"identity_id": "family", "source": "authenticated_http_session", "profile_type": "trusted_family", "verified": True, "trusted_session": True}}, False),
    ({"identity": {"identity_id": "owner", "source": "remote_http", "profile_type": "owner", "verified": True, "trusted_session": False}}, False),
    ({"identity": {"identity_id": "speaker", "source": "voice_unverified", "profile_type": "unknown", "verified": False}}, False),
])
def test_http_identity_is_fail_closed(payload, owner):
    assert identity_context_from_http_payload(payload).owner_verified is owner


def test_project_read_permission_does_not_grant_mutation():
    evaluator = SemanticPolicyEvaluator()
    identity = IdentityContext("anonymous", "http_unverified", "unknown", False, False)
    assert evaluator.evaluate(capability_id="project.read", risk_class="READ_ONLY", identity=identity, trace_id="t").granted
    denied = evaluator.evaluate(capability_id="project.read", risk_class="MUTATION", identity=identity, trace_id="t")
    assert not denied.granted and denied.denial_reason


def test_project_read_manifest_is_real_and_discovered_generically():
    manifests = load_capability_manifests()
    project = next(item for item in manifests if item["id"] == "project.read")
    assert project["provider"] == "existing_project_workspace_tools"
    assert project["network_policy"] == "DENY"
    assert discover_capability_providers("project.read")[0]["manifest_version"] == "2.0.0"


def test_duplicate_and_invalid_manifest_rejected(tmp_path):
    source = json.loads(Path("docs/architecture/open_source_integration/capability_manifests/project.read.v1.json").read_text())
    (tmp_path / "a.json").write_text(json.dumps(source))
    (tmp_path / "b.json").write_text(json.dumps(source))
    with pytest.raises(ValueError, match="duplicate"):
        load_capability_manifests(tmp_path, allow_noncanonical_source=True)
    source.pop("provider")
    (tmp_path / "b.json").unlink()
    (tmp_path / "a.json").write_text(json.dumps(source))
    with pytest.raises(ValueError, match="schema"):
        load_capability_manifests(tmp_path, allow_noncanonical_source=True)


def test_bounded_evidence_is_valid_json_and_reports_omissions():
    bounded, omitted = ExistingProjectUnderstandingAdapter._bounded_payload({"rows": ["x" * 4000] * 60})
    encoded = json.dumps(bounded)
    assert json.loads(encoded) == bounded
    assert omitted > 0 and len(encoded) < 100_000


def test_deadline_cancels_and_bounds_component():
    deadline = RequestDeadline(1.0)
    assert 0 < deadline.remaining(0.1) <= 0.1
    deadline.cancel()
    assert deadline.cancelled


def test_server_boundary_uses_canonical_owners_without_dynamic_tools_import():
    adapter = Path("MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py").read_text()
    assert "importlib.import_module" not in adapter
    assert "TEMPORARY_COMPATIBILITY_SHIM_final_brain" not in adapter
    assert "from tools.jarvis_live_runtime" not in adapter
    assert "MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools" in adapter
    assert "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models" in adapter


def test_control_plane_has_no_ollama_specific_understanding_logic():
    source = Path("CONTROL_PLANE/api_server.py").read_text()
    assert "OLLAMA_CHAT_URL" not in source
    assert "ollama_post_json" not in source


def test_no_mid_json_string_slice_remains():
    source = Path("MAKSIMAR_SERVER/AI_ORCHESTRATION/project_understanding_adapter.py").read_text()
    assert "[:12000]" not in source
    item = EvidenceItem("kind", "source", "{}", "scope", 1.0, "trace", "now", omitted_count=2, truncated=True)
    assert item.to_read_model()["omitted_count"] == 2


@pytest.mark.parametrize("payload", [
    {},
    {"identity": {"identity_id": "owner", "source": "authenticated_http_session", "profile_type": "owner", "verified": True, "trusted_session": True}},
    {"identity": {"identity_id": "owner", "source": "authenticated_http_session", "profile_type": "owner", "verified": False, "trusted_session": True}},
    {"identity": {"identity_id": "owner", "source": "remote_http", "profile_type": "owner", "verified": True, "trusted_session": False}},
])
def test_legacy_disabled_command_path_never_claims_pc_execution(payload):
    result = api_server.jarvis_live_command(payload)
    for field in (
        "owner_pc_control_allowed",
        "screen_observation_allowed",
        "keyboard_mouse_allowed",
        "browser_control_allowed",
        "direct_owner_action_allowed",
        "pc_control_allowed",
    ):
        assert field not in result


def test_legacy_disabled_stream_never_claims_pc_execution():
    body = list(api_server._legacy_disabled_stream())
    assert body and '"owner_pc_control_allowed"' not in body[0]
    assert '"pc_control_allowed"' not in body[0]


def test_deleted_project_read_direct_suite_has_exact_canonical_replacements():
    canonical = Path("tests/control_plane/test_canonical_semantic_turn_v2.py").read_text(encoding="utf-8")
    boundary = Path("tests/jarvis_live_runtime/test_project_workspace_tools_boundary_smoke.py").read_text(
        encoding="utf-8"
    )
    assert '"inspect_imports"' in canonical
    assert '"inspect_structure"' in canonical
    assert '("search",)' in canonical
    assert "test_project_path_guard_blocks_parent_escape" in boundary
    assert "test_read_file_snippet_is_read_only" in boundary
    assert "test_active_hot_path_has_no_legacy_phrase_or_marker_router" in canonical


def test_pc_runtime_truth_depends_on_executor_health_without_disabling_owner_autonomy():
    readiness_source = Path(
        "MAKSIMAR_SERVER/OBSERVABILITY/jarvis_live/jarvis_live_observability_read_model.py"
    ).read_text(encoding="utf-8")
    inventory_source = Path(
        "MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY/existing_capability_inventory.py"
    ).read_text(encoding="utf-8")
    # The published model-free contract adds a disabled branch; normal mode must
    # still reflect actual executor health, never owner identity alone.
    values = [value for node in ast.walk(ast.parse(readiness_source)) if isinstance(node, ast.Dict)
              for key, value in zip(node.keys, node.values)
              if isinstance(key, ast.Constant) and key.value == "pc_executor_available"]
    assert len(values) == 1
    expression = compile(ast.Expression(values[0]), "<readiness executor contract>", "eval")
    for model_free in (False, True):
        for windows_edge_alive in (False, True, None):
            actual = eval(expression, {"__builtins__": {}},
                          {"model_free": model_free, "windows_edge_alive": windows_edge_alive})
            assert actual is (False if model_free else windows_edge_alive)
    assert 'execution_policy="verified_owner_typed_allowlist_runtime_health_required"' in inventory_source


def test_model_acceptance_never_hardcodes_global_no_router_claim():
    source = Path("tools/jarvis_live_runtime/phase_1b_model_acceptance.py").read_text(encoding="utf-8")
    assert "marker_router_used" not in source
    assert '"adapter_boundary_router_observed": False' in source
    assert '"global_user_path_router_status": "UNKNOWN"' in source
    assert '"trace_derived_no_router_proven": False' in source
    assert 'record["adapter_boundary_router_observed"] is False' not in source


def test_real_model_harness_never_counts_transport_errors_as_pass_or_latency(monkeypatch, tmp_path):
    class FailingAdapter:
        def __init__(self, **_):
            pass

        def understand(self, **_):
            return {
                "ok": False, "content": "", "model_call_attempted": True,
                "model_call_succeeded": False, "model_call_used": False,
                "raw_output_present": False, "transport_error": "ConnectError",
                "error": "ConnectError", "raw_model_result": {"ok": False, "error": "ConnectError"},
            }

    monkeypatch.setattr(model_acceptance, "ExistingOllamaModelUnderstandingAdapter", FailingAdapter)
    result = model_acceptance.run(tmp_path / "truth.json")

    assert result["total"] == 77
    assert result["passed"] == 0
    assert result["counts"]["model_attempted"] == 77
    assert result["counts"]["model_succeeded"] == 0
    assert result["counts"]["nonempty_raw"] == 0
    assert result["counts"]["transport_errors"] == 77
    assert result["understanding_p50_seconds"] is None
    assert result["understanding_p95_seconds"] is None


def test_unresolved_binding_retains_bounded_reason_without_promoting_proposal():
    from CONTROL_PLANE import canonical_semantic_spine as spine
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import build_semantic_capability_registry_projection
    audit = {}
    reason = "No matching declared output contract. " * 12
    result = spine._bind_goalframe_goal(
        call=lambda **kwargs: {"ok":True,"final_valid":True,"model_call_attempted":True,"model_call_succeeded":True,"raw_output_present":True,"content": json.dumps({"status": "UNRESOLVED", "capability_id": None, "reason": reason})},
        goal={"goal_id": "g1", "semantic_domain": "memory", "effect_intent": "observe",
              "requested_outcome": "inspect current memory", "grounding": "inspect current memory"},
        registry_projection=build_semantic_capability_registry_projection(),
        deadline=RequestDeadline(1.0), binding_audit=audit,
    )
    assert result == (None, "UNRESOLVED")
    assert audit["binding_reason"] == reason[:160]
    assert audit["binding_status"] == "UNRESOLVED"
    assert audit["model_proposed_capability_id"] is None


@pytest.mark.parametrize("value", (None,False,True,"ABSENT"))
@pytest.mark.parametrize("raw_used", (False,True))
def test_acceptance_harness_requires_final_valid_and_owns_consumption_truth(monkeypatch,tmp_path,value,raw_used):
    c=model_acceptance.operation_contract("respond")
    payload={"schema_version":"request_understanding.v2","language":"ru","goals":[{"goal_id":"g1","description":"answer"}],
        "required_capabilities":[{"capability_id":"conversation.respond","purpose":"answer","required":True}],
        "response_requirements":[],"effect_type":"OBSERVE","target_scope":c["target_scope"],"reversibility":c["reversibility"],
        "external_side_effect":False,"unresolved_capabilities":[],"operation_requirements":[{
            "capability_id":"conversation.respond","operation_id":"respond","purpose":"answer","required_evidence":list(c["evidence_kinds"]),
            "effect_type":c["effect_type"],"target_scope":c["target_scope"],"reversibility":c["reversibility"],"external_side_effect":c["external_side_effect"],"risk_class":c["risk_class"],"required":True}],
        "current_topic":"conversation","unresolved_reference":"","risk_class":"READ_ONLY","confidence":.99,"reason_codes":["test"]}
    class Adapter:
        def __init__(self,**kwargs):pass
        def understand(self,**kwargs):
            r={"ok":True,"content":json.dumps(payload),"model_call_attempted":True,"model_call_succeeded":True,"model_call_used":raw_used,"raw_output_present":True}
            if value!="ABSENT":r["final_valid"]=value
            return r
    monkeypatch.setattr(model_acceptance,"ExistingOllamaModelUnderstandingAdapter",Adapter)
    monkeypatch.setattr(model_acceptance,"CONVERSATION",("hello",))
    for name in ("PROJECT","MULTI_CAPABILITY","UNAVAILABLE_OR_DENIED"):monkeypatch.setattr(model_acceptance,name,())
    result=model_acceptance.run(tmp_path/"verdict.json")
    assert result["total"]==1
    assert result["passed"]==int(value is True)
    assert result["results"][0]["model_call_used"]==(value is True)
    if value is not True:assert result["understanding_p50_seconds"] is None


@pytest.mark.parametrize("end_state", ["cancelled", "expired"])
def test_final_brain_sync_late_complete_is_not_returned(monkeypatch, end_state):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_brain_loop_server_adapter as final
    deadline = RequestDeadline(60)
    calls = []
    def answer(**payload):
        calls.append(payload)
        if end_state == "cancelled":
            deadline.cancel()
        else:
            deadline.expires_at = deadline.started_at - 1
        return {"status": "COMPLETE", "response_text": "withheld fixture"}
    monkeypatch.setattr(final, "grounded_final_brain_call", answer)
    with pytest.raises(TimeoutError, match="final_brain_deadline_exceeded"):
        final.ExistingFinalBrainAdapter().answer(deadline=deadline, user_text="fixture")
    assert len(calls) == 1


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("end_state", ["cancelled", "expired"])
def test_final_brain_pre_cancel_never_contacts_author(monkeypatch, stream, end_state):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_brain_loop_server_adapter as final
    deadline = RequestDeadline(60)
    if end_state == "cancelled":
        deadline.cancel()
    else:
        deadline.expires_at = deadline.started_at - 1
    def forbidden(**payload):
        pytest.fail("cancelled FinalBrain contacted author")
    monkeypatch.setattr(final, "grounded_final_brain_call", forbidden)
    monkeypatch.setattr(final, "grounded_final_brain_stream", forbidden)
    port = final.ExistingFinalBrainAdapter()
    if stream:
        events = list(port.stream_answer(deadline=deadline))
        assert [e["event"] for e in events] == ["error"]
        assert events[0]["error_kind"] == "final_brain_deadline_exceeded"
    else:
        with pytest.raises(TimeoutError, match="final_brain_deadline_exceeded"):
            port.answer(deadline=deadline)


@pytest.mark.parametrize("event_kind", ["chunk", "done", "error"])
@pytest.mark.parametrize("end_state", ["cancelled", "expired"])
def test_final_brain_stream_checks_deadline_before_each_event(monkeypatch, event_kind, end_state):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_brain_loop_server_adapter as final
    deadline = RequestDeadline(60)
    consumed = []
    def events(**payload):
        if end_state == "cancelled":
            deadline.cancel()
        else:
            deadline.expires_at = deadline.started_at - 1
        consumed.append(event_kind)
        yield {"event": event_kind, "response_text": "must not escape", "text": "must not escape"}
        pytest.fail("adapter kept consuming cancelled stream")
    monkeypatch.setattr(final, "grounded_final_brain_stream", events)
    result = list(final.ExistingFinalBrainAdapter().stream_answer(deadline=deadline))
    assert consumed == [event_kind]
    assert result == [{"event": "error", "error_kind": "final_brain_deadline_exceeded",
                       "error_message": "Final Brain deadline exceeded", "response_text": ""}]


def test_final_brain_cancellation_between_stream_events_withholds_done(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_brain_loop_server_adapter as final
    deadline = RequestDeadline(60)
    def events(**payload):
        yield {"event": "chunk", "text": "already emitted"}
        deadline.cancel()
        yield {"event": "done", "response_text": "must not escape"}
    monkeypatch.setattr(final, "grounded_final_brain_stream", events)
    result = list(final.ExistingFinalBrainAdapter().stream_answer(deadline=deadline))
    assert [e["event"] for e in result] == ["chunk", "error"]
    assert result[-1]["error_kind"] == "final_brain_deadline_exceeded"


@pytest.mark.parametrize("stream", [False, True])
def test_final_brain_uncancelled_result_and_provider_failure_preserved(monkeypatch, stream):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_brain_loop_server_adapter as final
    port = final.ExistingFinalBrainAdapter()
    result = {"status": "COMPLETE", "response_text": "unchanged fixture"}
    events = [{"event": "chunk", "text": "fixture"}, {"event": "done", **result}]
    if stream:
        monkeypatch.setattr(final, "grounded_final_brain_stream", lambda **kw: iter(events))
        assert list(port.stream_answer(deadline=RequestDeadline(60))) == events
    else:
        monkeypatch.setattr(final, "grounded_final_brain_call", lambda **kw: result)
        assert port.answer(deadline=RequestDeadline(60)) is result
    def failure(**payload):
        raise ConnectionError("controlled provider unavailable")
    monkeypatch.setattr(final, "grounded_final_brain_stream" if stream else "grounded_final_brain_call", failure)
    with pytest.raises(ConnectionError, match="controlled provider unavailable"):
        if stream:
            list(port.stream_answer(deadline=RequestDeadline(60)))
        else:
            port.answer(deadline=RequestDeadline(60))


@pytest.fixture
def shared_deadline_turn(monkeypatch):
    import time
    from CONTROL_PLANE import canonical_semantic_spine as spine
    clock = {"now": 100.0, "work": 0.0}
    seen = {"prepare": [], "execution": [], "final": []}
    monkeypatch.setattr(time, "monotonic", lambda: clock["now"])
    def prepare(**kwargs):
        seen["prepare"].append(kwargs["deadline"])
        return {}, {}
    def execution(**kwargs):
        seen["execution"].append(kwargs["request_deadline"])
        clock["now"] += clock["work"]
        return {"operation_status": "FINAL_BRAIN_PENDING", "final_brain_input": {}}
    class Final:
        def stream_answer(self, *, deadline, **kwargs):
            seen["final"].append((deadline, deadline.remaining()))
            yield {"event": "chunk", "text": "controlled fixture"}
            yield {"event": "error", "error_kind": "controlled_terminal", "response_text": ""}
    monkeypatch.setattr(spine, "_prepare_input", prepare)
    monkeypatch.setattr(spine, "_run_canonical_semantic_turn_after_input", execution)
    kwargs = dict(text="fixture", project_port=None, conversation_port=None, model_port=None,
                  final_brain_port=Final(), permission_port=None, identity=None)
    return spine, clock, seen, kwargs


@pytest.mark.parametrize("spent,expected_final", [(2.0, True), (5.0, False), (6.0, False)])
def test_stream_spends_original_turn_budget_without_new_final_deadline(shared_deadline_turn, spent, expected_final):
    spine, clock, seen, kwargs = shared_deadline_turn
    clock["work"] = spent
    events = list(spine.stream_canonical_semantic_turn(**kwargs, total_timeout_seconds=5))
    token = seen["prepare"][0]
    assert seen["execution"] == [token]
    if expected_final:
        assert seen["final"] == [(token, 5.0 - spent)]
        assert [e["event"] for e in events] == ["accepted", "status", "chunk", "error"]
    else:
        assert not seen["final"]
        assert events[-1]["error_kind"] == "final_brain_deadline_exceeded"
        assert not any(e["event"] in {"chunk", "done"} for e in events)
    assert token.cancelled


@pytest.mark.parametrize("end_state", ["cancelled", "expired"])
def test_slow_or_cancelled_stream_before_turn_never_calls_understanding(shared_deadline_turn, end_state):
    spine, clock, seen, kwargs = shared_deadline_turn
    token = RequestDeadline(5)
    stream = spine.stream_canonical_semantic_turn(**kwargs, request_deadline=token, total_timeout_seconds=5)
    assert next(stream)["event"] == "accepted"
    if end_state == "cancelled":
        token.cancel()
    else:
        clock["now"] += 6
    events = list(stream)
    assert events[-1]["event"] == "error"
    assert not seen["prepare"] and not seen["execution"] and not seen["final"]


@pytest.mark.parametrize("stage", ["accepted", "status", "chunk"])
def test_stream_close_cancels_only_its_own_request(shared_deadline_turn, stage):
    spine, _, seen, kwargs = shared_deadline_turn
    first, second = RequestDeadline(5), RequestDeadline(5)
    stream = spine.stream_canonical_semantic_turn(**kwargs, request_deadline=first, total_timeout_seconds=5)
    while next(stream)["event"] != stage:
        pass
    stream.close()
    assert first.cancelled and not second.cancelled
    if stage == "accepted":
        assert not seen["prepare"]


@pytest.mark.parametrize("mode", ["sync", "deferred"])
def test_direct_canonical_turn_reuses_supplied_token_and_attempt_policy(shared_deadline_turn, mode):
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import UnderstandingAttemptPolicy
    spine, _, seen, kwargs = shared_deadline_turn
    policy = UnderstandingAttemptPolicy(max_model_attempts=3)
    token = RequestDeadline(5, understanding_attempt_policy=policy)
    result = spine.run_canonical_semantic_turn(**kwargs, request_deadline=token,
        total_timeout_seconds=5, understanding_attempt_policy=policy, defer_final_brain=mode == "deferred")
    assert seen["prepare"] == seen["execution"] == [token]
    assert token.understanding_attempt_policy is policy
    assert not token.cancelled and result["understanding_model_attempt_count"] == 0


@pytest.mark.parametrize("mutation,error", [("type", "canonical_request_deadline_invalid"),
    ("extended", "canonical_request_deadline_exceeds_turn_budget"),
    ("policy", "canonical_request_deadline_attempt_policy_mismatch")])
def test_invalid_or_extended_shared_deadline_fails_before_effects(shared_deadline_turn, mutation, error):
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import UnderstandingAttemptPolicy
    spine, _, seen, kwargs = shared_deadline_turn
    token = RequestDeadline(100 if mutation == "extended" else 5)
    extra = {}
    if mutation == "type":
        token = object()
    elif mutation == "policy":
        extra["understanding_attempt_policy"] = UnderstandingAttemptPolicy(max_model_attempts=1)
    with pytest.raises(ValueError, match=error):
        spine.run_canonical_semantic_turn(**kwargs, request_deadline=token, total_timeout_seconds=5, **extra)
    assert not seen["prepare"] and not seen["execution"] and not seen["final"]


def test_spine_withholds_final_event_after_original_budget_expires(shared_deadline_turn, monkeypatch):
    spine, clock, seen, kwargs = shared_deadline_turn
    class Final:
        def stream_answer(self, *, deadline, **payload):
            seen["final"].append(deadline)
            yield {"event": "chunk", "text": "already emitted"}
            clock["now"] += 6
            yield {"event": "done", "response_text": "must not escape"}
    kwargs["final_brain_port"] = Final()
    def forbidden(*args):
        pytest.fail("expired completion was recorded")
    monkeypatch.setattr(spine, "_record_stream_completed_conversation_response", forbidden)
    events = list(spine.stream_canonical_semantic_turn(**kwargs, total_timeout_seconds=5))
    assert [e["event"] for e in events] == ["accepted", "status", "chunk", "error"]
    assert events[-1]["error_kind"] == "final_brain_deadline_exceeded"
