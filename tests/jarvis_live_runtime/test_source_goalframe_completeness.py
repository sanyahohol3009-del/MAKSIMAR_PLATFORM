"""Controlled verifier judgments; no inference and no claim of natural infallibility."""
import copy
import json
import pytest
from CONTROL_PLANE import canonical_semantic_spine as spine
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    RequestDeadline, UnderstandingAttemptPolicy, validate_source_candidate_verdict,
    hydrate_response_requirements, validate_response_obligation_coverage)
from MAKSIMAR_SERVER.AI_ORCHESTRATION import model_understanding_adapter as adapter
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import build_semantic_capability_registry_projection

SOURCE = "Explain the recorded origin, rationale and execution of record A."
SOURCE_SIX = "Explain record A: origin, rationale, execution, evidence, review and learning qualification."
KINDS = ("PROVENANCE", "RATIONALE", "EXECUTION", "EVIDENCE", "REVIEW_STATUS", "LEARNING_QUALIFICATION")


def candidate(count=3, source_text=SOURCE):
    return {"goals": [{"goal_id": "g1", "semantic_domain": "memory", "effect_intent": "retrieve",
        "requested_outcome": "Read record A", "grounding": source_text, "ambiguity": "",
        "goal_role": "PRIMARY_OUTCOME", "parent_goal_id": None, "subgoal_justification_kind": "NONE",
        "memory_filter": {"query_kind": "PROVENANCE", "time_basis": "ANY_TIME", "time_start": "", "time_end": ""},
        "subject_constraints": {"scope": "SUBJECT", "actor": "actor_a", "experience_id": "experience_a"}}],
        "execution_restriction": "NONE", "execution_restriction_source": "",
        "response_requirements": [{"applies_to_goal_ids": ["g1"], "description": kind,
            "memory_query_kind": "PROVENANCE", "requirement_kind": kind} for kind in KINDS[:count]]}


def verdict(status="COMPLETE", count=3):
    return {"status": status, "supported": ["goal:g1"] + [f"requirement:{i}" for i in range(count)],
        "missing": ["independent source facet C"] if status == "INCOMPLETE" else [],
        "contradictions": ["wrong source semantics or duplicate facet"] if status == "INVALID" else [],
        "unsupported_claims": [], "reason": "Controlled independent semantic judgment"}


def install(monkeypatch, *, candidates=None, verdicts=None, binding_failure=False, repair_exception=False, source_text=SOURCE):
    candidates = iter(candidates or [candidate()]); verdicts = iter(verdicts or [verdict()])
    calls = []; understanding_calls = []
    def post(url, payload, **kwargs):
        calls.append(copy.deepcopy(payload))
        props = payload["format"]["properties"]
        if "goals" in props:
            understanding_calls.append(1)
            if repair_exception and len(understanding_calls) > 1:
                raise RuntimeError("controlled repair failure")
            content = next(candidates)
        elif "supported" in props:
            inputs = json.loads(payload["messages"][1]["content"])
            assert inputs["source"] == source_text
            assert inputs["candidate"] != inputs["source"]
            assert "expected_requirements" not in inputs
            content = next(verdicts)
        elif "capability_id" in props:
            content = {"status": "UNRESOLVED", "capability_id": None, "reason": "controlled binding failure"} if binding_failure else {"status": "BOUND", "capability_id": "runtime_history_store", "reason": "canonical reader"}
        else:
            raise AssertionError("unexpected model stage: " + str(props))
        return {"model": payload["model"], "done": True, "done_reason": "stop",
                "message": {"content": content if isinstance(content, str) else json.dumps(content)}}
    monkeypatch.setattr(adapter, "ollama_post_json", post)
    port = adapter.ExistingOllamaModelUnderstandingAdapter(json_schema=spine.REQUEST_UNDERSTANDING_JSON_SCHEMA,
                                                        candidate_json_schema=spine.CANDIDATE_DISCOVERY_JSON_SCHEMA)
    return port, calls


def run(port, limit=None, parent=False, source_text=SOURCE):
    deadline = RequestDeadline(60, understanding_attempt_policy=UnderstandingAttemptPolicy(max_model_attempts=limit, schema_max_attempts=1))
    audit = {}; kwargs = dict(model_port=port, deadline=deadline, original_text=source_text, session_context={},
        registry_projection=build_semantic_capability_registry_projection(), audit_trace=audit)
    if parent:
        from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
        result = spine._model_selected_registry_details(**kwargs, request_id="controlled", input_preparation={},
            identity=IdentityContext("fixture", "fixture_session", "owner", True, True, "Fixture", "JARVIS"))
    else:
        result = spine._model_selected_registry_details_goalframe(**kwargs)
    return result, audit, deadline


@pytest.mark.parametrize("count", [3, 6])
def test_complete_independent_verdict_continues_existing_binding(monkeypatch, count):
    source = SOURCE_SIX if count == 6 else SOURCE
    proposed = candidate(count, source_text=source)
    port, calls = install(monkeypatch, candidates=[proposed], verdicts=[verdict(count=count)], source_text=source)
    result, audit, deadline = run(port, source_text=source)
    assert result is not None
    expected = hydrate_response_requirements(tuple(proposed["goals"]), tuple(proposed["response_requirements"]))
    validate_response_obligation_coverage(expected, tuple(result["selection_response_requirements"]))
    assert audit["goalframe_source_verifications"][0]["status"] == "COMPLETE"
    assert [p["model"] for p in calls] == ["jarvis:chat8b", "jarvis-live:qwen14b", "jarvis:chat8b"]
    assert deadline.understanding_model_attempt_count == 3


@pytest.mark.parametrize("status", ["INVALID", "UNPROVEN"])
def test_semantic_rejection_prevents_binding_and_legacy(monkeypatch, status):
    port, calls = install(monkeypatch, verdicts=[verdict(status)])
    result, audit, _ = run(port, parent=True)
    assert result is None and len(calls) == 2
    assert audit["candidate_discovery_error"] == "goalframe_provenance_invalid"


@pytest.mark.parametrize("limit,expected_calls,state", [(1,1,"NOT_ATTEMPTED"), (2,2,"UNAVAILABLE"), (3,3,"FAILED"), (4,4,"SUCCEEDED")])
def test_shared_budget_understand_verify_repair_reverify(monkeypatch, limit, expected_calls, state):
    port, calls = install(monkeypatch, candidates=[candidate(2), candidate(3)],
        verdicts=[verdict("INCOMPLETE",2), verdict()])
    result, audit, deadline = run(port, limit)
    assert result is None  # limit4 verifies repaired candidate but has no binding-call budget
    assert len(calls) == expected_calls == deadline.understanding_model_attempt_count
    assert audit["goalframe_repair_state"] == state
    assert len(deadline.understanding_model_attempts) == expected_calls
    assert all(a["user_memory"] is False and a["training_eligible"] is False for a in deadline.understanding_model_attempts)


def test_one_repair_succeeds_without_a_second_repair(monkeypatch):
    port, calls = install(monkeypatch, candidates=[candidate(2),candidate()], verdicts=[verdict("INCOMPLETE",2), verdict()])
    result, audit, deadline = run(port,5)
    assert result is not None and len(calls)==5
    assert audit["goalframe_repair_state"] == "SUCCEEDED"
    assert len(audit["goalframe_understanding_attempts"])==2
    assert len(audit["goalframe_source_verifications"])==2
    assert [a["model_role"] for a in deadline.understanding_model_attempts] == ["jarvis_chat_model","heavy_reasoning_model","jarvis_chat_model","heavy_reasoning_model","jarvis_chat_model"]


def test_still_incomplete_after_one_repair_fails_closed(monkeypatch):
    port,calls=install(monkeypatch,candidates=[candidate(2),candidate(2)],verdicts=[verdict("INCOMPLETE",2),verdict("INCOMPLETE",2)])
    result,audit,_=run(port,parent=True)
    assert result is None and len(calls)==4 and audit["goalframe_repair_state"]=="FAILED"


@pytest.mark.parametrize("phase",["semantic","binding","provenance"])
def test_repair_exception_never_falls_through_to_legacy(monkeypatch,phase):
    initial=candidate()
    if phase=="provenance":initial["goals"][0]["grounding"]="not present in source"
    v=verdict("INCOMPLETE") if phase=="semantic" else verdict()
    port,calls=install(monkeypatch,candidates=[initial],verdicts=[v],binding_failure=phase=="binding",repair_exception=True)
    result,audit,_=run(port,parent=True)
    assert result is None and audit["goalframe_repair_state"]=="FAILED"
    assert audit["candidate_discovery_error"]=="goalframe_provenance_invalid"
    assert len(calls)=={"semantic":3,"binding":4,"provenance":2}[phase]
    assert deadline_raw_failed(audit)


def deadline_raw_failed(audit):
    return audit["goalframe_understanding_attempts"][-1]["raw_model_content"] is None


@pytest.mark.parametrize("raw", ["not json", "{}", {**verdict(),"supported":["invented"]}, {**verdict(),"contradictions":["conflict"]}])
def test_malformed_or_inconsistent_verifier_fails_closed(monkeypatch,raw):
    port,calls=install(monkeypatch,verdicts=[raw])
    result,audit,_=run(port,parent=True)
    assert result is None and len(calls)==2
    assert audit["goalframe_source_verifications"][0]["status"]=="UNPROVEN"


def test_unavailable_verifier_is_unproven_without_call(monkeypatch):
    port,calls=install(monkeypatch)
    port.verify_source_candidate=None
    result,audit,_=run(port,parent=True)
    assert result is None and len(calls)==1
    assert audit["goalframe_source_verifications"][0]["status"]=="UNPROVEN"


@pytest.mark.parametrize("model,role",[("jarvis:chat8b","jarvis_chat_model"),("jarvis:helper3b","helper_input_correction_model"),("jarvis-live:qwen14b","heavy_reasoning_model")])
def test_trace_uses_existing_canonical_role_map(monkeypatch,model,role):
    seen=[]
    monkeypatch.setattr(adapter,"trace_model_call_started",lambda **kw:(seen.append(kw) or ("",1,0)))
    monkeypatch.setattr(adapter,"trace_model_call_completed",lambda **kw:None)
    monkeypatch.setattr(adapter,"ollama_post_json",lambda *a,**kw:{"model":model,"done":True,"message":{"content":"{}"}})
    p=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema={})
    p._single_model_call(system_prompt="fixture",user_prompt="fixture",deadline=RequestDeadline(5),schema={},num_predict=1,deadline_error="fixture",model_id=model)
    assert seen[0]["model_role"]==role


@pytest.mark.parametrize("mutation",["missing","wrong","extra","duplicate"])
def test_independent_source_oracle_can_reject_candidate_that_covers_itself(mutation):
    # Test oracle is independent of candidate; never imported by production.
    required=("A","B","C");proposed=["A","B","C"]
    if mutation=="missing":proposed.pop()
    elif mutation=="wrong":proposed[-1]="wrong-C"
    elif mutation=="extra":proposed.append("D")
    else:proposed[-1]="B"
    judgment=verdict("INCOMPLETE" if mutation=="missing" else "INVALID",len(proposed))
    assert tuple(proposed)!=required
    ids=tuple(judgment["supported"])
    assert validate_source_candidate_verdict(judgment,ids)!="COMPLETE"


@pytest.mark.parametrize("mutation",["unknown","duplicate","missing","status","bad_list","bad_reason"])
def test_public_verdict_rejects_malformed_reference_contract(mutation):
    v=verdict();ids=tuple(v["supported"])
    if mutation=="unknown":v["supported"].append("unknown")
    if mutation=="duplicate":v["supported"].append(v["supported"][0])
    if mutation=="missing":v["supported"].pop()
    if mutation=="status":v["status"]="UNKNOWN"
    if mutation=="bad_list":v["missing"]={}
    if mutation=="bad_reason":v["reason"]=""
    assert validate_source_candidate_verdict(v,ids)=="UNPROVEN"


@pytest.mark.parametrize("defer",[False, True, "stream"])
def test_sync_deferred_stream_share_fail_closed_gate_and_raws(monkeypatch,defer):
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
    from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
    class NoDownstream:
        def __getattr__(self, name):
            raise AssertionError("downstream must not be reached: " + name)
    port,calls=install(monkeypatch,verdicts=[verdict("INVALID")])
    kwargs=dict(text=SOURCE,model_port=port,project_port=NoDownstream(),conversation_port=NoDownstream(),
        final_brain_port=NoDownstream(),permission_port=SemanticPolicyEvaluator(),
        identity=IdentityContext("fixture","fixture_session","owner",True,True,"Fixture","JARVIS"),
        registry_projection=build_semantic_capability_registry_projection(), input_channel="typed",
        understanding_attempt_policy=UnderstandingAttemptPolicy(max_model_attempts=2,schema_max_attempts=1))
    if defer=="stream":
        events=list(spine.stream_canonical_semantic_turn(**kwargs))
        result=events[-1]["result"]
        assert not any(e["event"]=="chunk" for e in events)
    else:
        result=spine.run_canonical_semantic_turn(**kwargs,defer_final_brain=defer)
    assert result["operation_status"]=="UNDERSTANDING_UNAVAILABLE"
    assert len(calls)==2 and result["understanding_model_attempt_count"]==2
    assert len(result["goalframe_source_verifications"])==1
    assert result["understanding_model_attempts"][1]["semantic_verdict"]=="INVALID"
    assert not result.get("final_brain_input")


def test_verifier_transport_exception_preserves_raw_failure_and_no_legacy(monkeypatch):
    port,calls=install(monkeypatch)
    original=adapter.ollama_post_json
    def transport(url,payload,**kwargs):
        if payload["model"]=="jarvis-live:qwen14b":
            calls.append(copy.deepcopy(payload))
            raise ConnectionError("controlled verifier unavailable")
        return original(url,payload,**kwargs)
    monkeypatch.setattr(adapter,"ollama_post_json",transport)
    result,audit,deadline=run(port,parent=True)
    assert result is None and len(calls)==2
    failed=deadline.understanding_model_attempts[-1]
    assert failed["raw_response"] is None and failed["response_received"] is False
    assert failed["model_role"]=="heavy_reasoning_model" and failed["semantic_verdict"]=="UNPROVEN"
    assert audit["goalframe_source_verifications"][0]["status"]=="UNPROVEN"



def test_existing_schema_retry_keeps_each_verifier_raw_under_same_deadline(monkeypatch):
    port,calls=install(monkeypatch,verdicts=["malformed",verdict()])
    deadline=RequestDeadline(60,understanding_attempt_policy=UnderstandingAttemptPolicy(max_model_attempts=4))
    audit={}
    result=spine._model_selected_registry_details_goalframe(model_port=port,deadline=deadline,
        original_text=SOURCE,session_context={},registry_projection=build_semantic_capability_registry_projection(),audit_trace=audit)
    assert result is not None and len(calls)==4
    attempts=deadline.understanding_model_attempts
    assert [a["request_model_attempt"] for a in attempts]==[1,2,3,4]
    assert attempts[1]["raw_response"]=="malformed" and attempts[1]["semantic_verdict"]=="UNPROVEN"
    assert attempts[2]["semantic_verdict"]=="COMPLETE"
    assert attempts[1]["retry_decision"] is True and attempts[2]["retry_decision"] is False
    assert audit["goalframe_repair_state"]=="NOT_ATTEMPTED"


def test_candidate_cannot_author_own_complete_verdict(monkeypatch):
    proposed=candidate();proposed["status"]="COMPLETE"
    port,calls=install(monkeypatch,candidates=[proposed])
    result,audit,_=run(port,parent=True)
    assert result is None and len(calls)==1
    assert not audit.get("goalframe_source_verifications")
    assert audit["candidate_discovery_error"]=="goalframe_provenance_invalid"


@pytest.mark.parametrize("model_id", [adapter.PRIMARY_CONVERSATION_MODEL_ID, "jarvis-live:qwen14b", adapter.HELPER_INPUT_CORRECTION_MODEL_ID])
@pytest.mark.parametrize("end_state", ["cancelled", "expired"])
def test_late_understanding_response_is_withheld_and_retained_without_retry(monkeypatch, model_id, end_state):
    port, _ = install(monkeypatch)
    deadline = RequestDeadline(60)
    calls = []
    raw = '{"supported": true}'
    def post(url, payload, **kwargs):
        calls.append(copy.deepcopy(payload))
        if end_state == "cancelled":
            deadline.cancel()
        else:
            deadline.expires_at = deadline.started_at - 1
        return {"model": model_id, "done": True, "message": {"content": raw}}
    monkeypatch.setattr(adapter, "ollama_post_json", post)
    with pytest.raises(TimeoutError, match="controlled_deadline_exceeded"):
        port._main_model_call(system_prompt="fixture", user_prompt="fixture", deadline=deadline,
            schema={"type": "object"}, num_predict=20, deadline_error="controlled_deadline_exceeded", model_id=model_id)
    assert len(calls) == deadline.understanding_model_attempt_count == 1
    assert len(deadline.understanding_model_attempts) == 1
    failure = deadline.understanding_model_attempts[0]
    assert failure["response_received"] is True and failure["raw_response"] == raw
    assert failure["retry_decision"] is False and failure["retry_reason"] == "cancelled_after_response"
    assert failure["schema_valid"] is False and failure["diagnostic_only"] is True
    assert failure["user_memory"] is False and failure["training_eligible"] is False


@pytest.mark.parametrize("end_state", ["cancelled", "expired"])
def test_understanding_cancelled_before_call_never_contacts_provider(monkeypatch, end_state):
    port, _ = install(monkeypatch)
    deadline = RequestDeadline(60)
    if end_state == "cancelled":
        deadline.cancel()
    else:
        deadline.expires_at = deadline.started_at - 1
    def forbidden(*args, **kwargs):
        pytest.fail("cancelled request contacted provider")
    monkeypatch.setattr(adapter, "ollama_post_json", forbidden)
    with pytest.raises(TimeoutError):
        port._main_model_call(system_prompt="fixture", user_prompt="fixture", deadline=deadline,
            schema={"type": "object"}, num_predict=20, deadline_error="controlled_deadline_exceeded")
    assert deadline.understanding_model_attempt_count == 0 and not deadline.understanding_model_attempts


@pytest.mark.parametrize("cancel_stage", ["jarvis:chat8b", "jarvis-live:qwen14b"])
def test_cancelled_goalframe_call_never_reaches_downstream_binding(monkeypatch, cancel_stage):
    port, calls = install(monkeypatch)
    deadline = RequestDeadline(60)
    original = adapter.ollama_post_json
    def post(url, payload, **kwargs):
        result = original(url, payload, **kwargs)
        if payload["model"] == cancel_stage:
            deadline.cancel()
        return result
    monkeypatch.setattr(adapter, "ollama_post_json", post)
    audit = {}
    result = spine._model_selected_registry_details_goalframe(model_port=port, deadline=deadline,
        original_text=SOURCE, session_context={}, registry_projection=build_semantic_capability_registry_projection(),
        audit_trace=audit)
    assert result is None
    assert [p["model"] for p in calls] == (["jarvis:chat8b"] if cancel_stage == "jarvis:chat8b" else ["jarvis:chat8b", "jarvis-live:qwen14b"])
    assert deadline.understanding_model_attempts[-1]["response_received"] is True
    assert deadline.understanding_model_attempts[-1]["retry_decision"] is False


@pytest.mark.parametrize("review", [False, True])
@pytest.mark.parametrize("end_state", ["before", "during", "expired", "active"])
def test_helper_direct_correction_preserves_same_cancellation_boundary(monkeypatch, review, end_state):
    port, _ = install(monkeypatch)
    deadline = RequestDeadline(60)
    calls = []
    data = {"schema_version": "helper_input_correction.v2", "corrected_text": "fixture",
            "ambiguity_candidates": [], "confidence": 1.0, "reason_codes": ["no_change_needed"],
            "preserve_original": True, "no_change_needed": True}
    raw = json.dumps(data)
    if end_state == "before":
        deadline.cancel()
    def post(url, payload, **kwargs):
        calls.append(copy.deepcopy(payload))
        if end_state == "during":
            deadline.cancel()
        elif end_state == "expired":
            deadline.expires_at = deadline.started_at - 1
        return {"model": payload["model"], "done": True, "message": {"content": raw}}
    monkeypatch.setattr(adapter, "ollama_post_json", post)
    kwargs = dict(original_text="fixture", safe_normalized_text="fixture", input_channel="typed",
                  input_quality_metadata={}, deadline=deadline)
    if review:
        kwargs["prior_correction"] = data
    invoke = port.review_input_correction if review else port.correct_input
    if end_state == "active":
        result = invoke(**kwargs)
        assert result["ok"] and result["final_valid"] and result["parsed"] == data
    else:
        with pytest.raises(TimeoutError, match="helper_input_correction_deadline_exceeded") as error:
            invoke(**kwargs)
        if end_state != "before":
            retained = error.value.model_call_result
            assert retained["content"] == raw and retained["raw_model_result"]["content"] == raw
    assert len(calls) == (0 if end_state == "before" else 1)
    assert all(call["model"] == adapter.HELPER_INPUT_CORRECTION_MODEL_ID for call in calls)


def test_real_goalframe_stream_uses_one_request_token_and_retains_raw_failures(monkeypatch):
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
    from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
    port, calls = install(monkeypatch, verdicts=[verdict("INVALID")])
    token = RequestDeadline(60)
    seen = []
    single = port._single_model_call
    def observe(**kwargs):
        seen.append(kwargs["deadline"])
        return single(**kwargs)
    monkeypatch.setattr(port, "_single_model_call", observe)
    class NoDownstream:
        def __getattr__(self, name):
            raise AssertionError("invalid source verdict reached downstream: " + name)
    events = list(spine.stream_canonical_semantic_turn(text=SOURCE, model_port=port,
        project_port=NoDownstream(), conversation_port=NoDownstream(), final_brain_port=NoDownstream(),
        permission_port=SemanticPolicyEvaluator(), identity=IdentityContext("fixture", "offline", "owner", True, True),
        registry_projection=build_semantic_capability_registry_projection(), input_channel="typed",
        request_deadline=token))
    assert len(calls) == 2 and seen == [token, token]
    assert token.cancelled and token.understanding_model_attempt_count == 2
    assert len(token.understanding_model_attempts) == 2
    assert all(a["raw_response"] and not a["user_memory"] and not a["training_eligible"]
               for a in token.understanding_model_attempts)
    assert not any(event["event"] in {"chunk", "done"} for event in events)
    assert events[-1]["result"]["operation_status"] == "UNDERSTANDING_UNAVAILABLE"
