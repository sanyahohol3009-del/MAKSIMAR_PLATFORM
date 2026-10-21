from __future__ import annotations

from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    HELPER_INPUT_CORRECTION_MODEL_ID,
    MODEL_TIMEOUT_POLICY_SOURCE,
    OLLAMA_CHAT_URL,
    OLLAMA_LIVE_MODEL_KEEP_ALIVE,
    OLLAMA_URL,
    PRIMARY_CONVERSATION_MODEL_ID,
    build_model_call_timeout_truth,
    grounded_final_brain_stream,
    grounded_final_brain_call,
    ollama_model_call_result,
    ollama_transport_read_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    context_tokens_for_jarvis_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline
from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import (
    HELPER_INPUT_CORRECTION_SCHEMA,
    ExistingOllamaModelUnderstandingAdapter,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import (
    ExistingFinalBrainAdapter,
)


def test_ollama_transport_is_model_engine_not_edge_brain() -> None:
    model = ollama_transport_read_model()

    assert model["model_engine_only"] is True
    assert model["control_plane_required"] is True
    assert model["direct_edge_to_ollama_allowed"] is False
    assert "127.0.0.1:11434" in OLLAMA_URL
    assert OLLAMA_CHAT_URL.endswith("/api/chat")
    assert PRIMARY_CONVERSATION_MODEL_ID == "jarvis:chat8b"


def test_ollama_transport_read_model_has_required_roles() -> None:
    model = ollama_transport_read_model()

    assert model["primary_conversation_model"] == "jarvis:chat8b"
    assert model["fallback_model"] == "jarvis-live:qwen14b"
    assert model["heavy_coder_model"] == "jarvis:coder14b"
    assert model["base_heavy_coder_model"] == "qwen2.5-coder:14b"


def test_understanding_and_helper_requests_share_canonical_live_keep_alive(monkeypatch) -> None:
    payloads = []

    def fake_post(path, payload, timeout_seconds):
        payloads.append(payload)
        return {"model": payload["model"], "message": {"content": "{}"}, "done": True}

    monkeypatch.setattr("MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json", fake_post)
    adapter = ExistingOllamaModelUnderstandingAdapter(json_schema={"type": "object"})
    adapter.understand(system_prompt="system", user_prompt="user", deadline=RequestDeadline(5.0))
    adapter.correct_input(
        original_text="текст", safe_normalized_text="текст", input_channel="voice",
        input_quality_metadata={"stt_confidence": 0.5}, deadline=RequestDeadline(5.0),
    )

    assert [payload["keep_alive"] for payload in payloads] == [
        OLLAMA_LIVE_MODEL_KEEP_ALIVE, OLLAMA_LIVE_MODEL_KEEP_ALIVE,
    ]
    assert [payload["think"] for payload in payloads] == [False, False]
    assert HELPER_INPUT_CORRECTION_SCHEMA["properties"]["schema_version"]["const"] == "helper_input_correction.v2"


def test_transport_success_does_not_claim_canonical_model_use(monkeypatch) -> None:
    adapter = ExistingOllamaModelUnderstandingAdapter(json_schema={"type": "object"})
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        lambda *args, **kwargs: {"ok": False, "error": "ConnectError", "message": "connection refused"},
    )
    failed = adapter.understand(system_prompt="system", user_prompt="user", deadline=RequestDeadline(5.0))
    assert failed["model_call_attempted"] is True
    assert failed["model_call_succeeded"] is False
    assert failed["model_call_used"] is False
    assert failed["raw_output_present"] is False

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        lambda *args, **kwargs: {
            "model": PRIMARY_CONVERSATION_MODEL_ID,
            "message": {"content": "{\"ok\":true}"},
            "done": True,
        },
    )
    succeeded = adapter.understand(system_prompt="system", user_prompt="user", deadline=RequestDeadline(5.0))
    assert succeeded["model_call_succeeded"] is True
    assert succeeded["model_call_used"] is False
    assert succeeded["raw_output_present"] is True


def test_nonstream_completion_requires_explicit_terminal_done_true() -> None:
    telemetry = {
        "prompt_eval_count": 11, "eval_count": 7,
        "prompt_eval_duration": 101, "eval_duration": 102,
        "load_duration": 103, "total_duration": 306,
    }

    def envelope(**result):
        return ollama_model_call_result(
            {"model": PRIMARY_CONVERSATION_MODEL_ID, **telemetry, **result},
            expected_model_id=PRIMARY_CONVERSATION_MODEL_ID,
            requested_num_ctx=3072, transport_attempted=True,
        )

    complete = envelope(done=True, message={"content": "{}"})
    assert complete["model_call_succeeded"] is True
    assert complete["raw_output_present"] is True
    assert complete["ok"] is True
    assert complete["model_call_used"] is False

    incomplete = envelope(done=False, message={"content": "{}"})
    assert incomplete["model_call_succeeded"] is False
    assert incomplete["raw_output_present"] is True
    assert incomplete["ok"] is False
    assert incomplete["error"] == "model_completion_incomplete"

    missing = envelope(message={"content": "{}"})
    assert missing["done"] is None
    assert missing["model_call_succeeded"] is False
    assert missing["ok"] is False
    assert missing["error"] == "model_completion_unproven"

    null_done = envelope(done=None, message={"content": "{}"})
    assert null_done["done"] is None
    assert null_done["model_call_succeeded"] is False
    assert null_done["ok"] is False
    assert null_done["error"] == "model_completion_unproven"

    empty = envelope(done=True, message={"content": ""})
    assert empty["model_call_succeeded"] is True
    assert empty["raw_output_present"] is False
    assert empty["ok"] is False
    assert empty["error"] == "empty_model_output"

    for result in (complete, incomplete, missing, null_done, empty):
        assert result["prompt_eval_count"] == 11
        assert result["eval_count"] == 7
        assert result["total_duration"] == 306


def test_final_brain_request_uses_canonical_live_keep_alive(monkeypatch) -> None:
    observed = {}

    def fake_post(path, payload, timeout_seconds):
        observed.update(payload)
        return {"model": payload["model"], "message": {"content": "grounded"}, "done": True}

    monkeypatch.setattr("MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport.ollama_post_json", fake_post)
    result = grounded_final_brain_call(
        original_text="привет", understanding={}, execution_plan={},
        evidence_bundle={"items": []}, capability_state=(),
    )

    assert result["ok"] is True
    assert observed["keep_alive"] == OLLAMA_LIVE_MODEL_KEEP_ALIVE


def test_unified_envelope_preserves_telemetry_for_every_main_model_method(monkeypatch) -> None:
    payloads = []

    def fake_post(path, payload, timeout_seconds):
        del path, timeout_seconds
        payloads.append(payload)
        return {
            "model": PRIMARY_CONVERSATION_MODEL_ID,
            "message": {"content": '{"candidate_kinds":["readonly_tool"]}'},
            "done": True, "done_reason": "stop",
            "prompt_eval_count": 583, "eval_count": 192,
            "prompt_eval_duration": 11, "eval_duration": 12,
            "load_duration": 13, "total_duration": 36,
        }

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        fake_post,
    )
    adapter = ExistingOllamaModelUnderstandingAdapter(
        json_schema={"type": "object"}, candidate_json_schema={"type": "object"},
        kind_json_schema={"type": "object"},
    )
    results = (
        adapter.discover_kinds(system_prompt="s", user_prompt="u", deadline=RequestDeadline(5)),
        adapter.discover_candidates(system_prompt="s", user_prompt="u", deadline=RequestDeadline(5)),
        adapter.understand(system_prompt="s", user_prompt="u", deadline=RequestDeadline(5)),
        adapter.repair(system_prompt="s", user_prompt="u", deadline=RequestDeadline(5)),
    )
    assert all(item["prompt_eval_count"] == 583 and item["eval_count"] == 192 for item in results)
    assert all(item["total_duration"] == 36 and item["done_reason"] == "stop" for item in results)
    assert all(item["model_call_succeeded"] is True and item["model_call_used"] is False for item in results)
    assert [item["requested_num_ctx"] for item in results] == [4096, 4096, 4096, 4096]
    assert [payload["options"]["num_ctx"] for payload in payloads] == [4096, 4096, 4096, 4096]
    assert all(payload["think"] is False for payload in payloads)
    assert all(item["model_role"] == "jarvis_chat_model" for item in results)
    assert all(item["configured_component_timeout_seconds"] == 180.0 for item in results)
    assert all(item["timeout_policy_source"] == MODEL_TIMEOUT_POLICY_SOURCE for item in results)
    assert all(0 < item["effective_transport_timeout_seconds"] <= 5 for item in results)
    assert all(item["transport_started_at"] and item["transport_finished_at"] for item in results)


def test_absent_telemetry_is_null_and_helper_context_is_separate(monkeypatch) -> None:
    payloads = []

    def fake_post(path, payload, timeout_seconds):
        del path, timeout_seconds
        payloads.append(payload)
        return {"model": payload["model"], "message": {"content": "{}"}, "done": True}

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        fake_post,
    )
    adapter = ExistingOllamaModelUnderstandingAdapter(json_schema={"type": "object"})
    main = adapter.understand(system_prompt="s", user_prompt="u", deadline=RequestDeadline(5))
    helper = adapter.correct_input(
        original_text="текст", safe_normalized_text="текст", input_channel="stt",
        input_quality_metadata={"correction_requested": True}, deadline=RequestDeadline(5),
    )
    assert main["prompt_eval_count"] is None and main["total_duration"] is None
    assert main["requested_num_ctx"] == 4096
    assert helper["requested_num_ctx"] == context_tokens_for_jarvis_model(HELPER_INPUT_CORRECTION_MODEL_ID) == 2048
    assert [item["options"]["num_ctx"] for item in payloads] == [4096, 2048]


def test_streaming_done_preserves_sanitized_ollama_telemetry(monkeypatch) -> None:
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): return None
        def iter_lines(self):
            yield (
                '{"model":"jarvis:chat8b","message":{"content":"Ответ"},'
                '"done":false}'
            )
            yield (
                '{"model":"jarvis:chat8b","message":{"content":""},"done":true,'
                '"done_reason":"stop","prompt_eval_count":101,"eval_count":7,'
                '"prompt_eval_duration":10,"eval_duration":20,"load_duration":30,'
                '"total_duration":60,"thinking":"private"}'
            )

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport.httpx.stream",
        lambda *args, **kwargs: Response(),
    )
    events = list(grounded_final_brain_stream(
        original_text="ответь", understanding={}, execution_plan={},
        evidence_bundle={"items": ()}, capability_state=(),
    ))
    done = events[-1]
    assert done["event"] == "done" and done["prompt_eval_count"] == 101 and done["eval_count"] == 7
    assert done["requested_num_ctx"] == 4096 and done["total_duration"] == 60
    assert done["model_role"] == "jarvis_chat_model"
    assert done["configured_component_timeout_seconds"] == 180.0
    assert done["timeout_policy_source"] == MODEL_TIMEOUT_POLICY_SOURCE
    assert "thinking" not in str(done).casefold() and "private" not in str(done).casefold()


def test_main_model_methods_use_one_canonical_timeout_policy(monkeypatch) -> None:
    observed_timeouts = []

    def fake_post(path, payload, timeout_seconds):
        del path
        observed_timeouts.append((payload["options"]["num_predict"], timeout_seconds))
        return {
            "model": payload["model"], "message": {"content": "{}"},
            "done": True, "done_reason": "stop",
        }

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        fake_post,
    )
    adapter = ExistingOllamaModelUnderstandingAdapter(
        json_schema={"type": "object"}, candidate_json_schema={"type": "object"},
        kind_json_schema={"type": "object"},
    )
    for method in (
        adapter.discover_kinds,
        adapter.discover_candidates,
        adapter.understand,
        adapter.repair,
    ):
        result = method(system_prompt="s", user_prompt="u", deadline=RequestDeadline(300))
        assert result["configured_component_timeout_seconds"] == 180.0
        assert result["effective_transport_timeout_seconds"] == 180.0
        assert result["timeout_policy_source"] == MODEL_TIMEOUT_POLICY_SOURCE
    assert [item[1] for item in observed_timeouts] == [180.0] * 4


def test_simulated_cold_load_over_90_seconds_is_admitted_by_chat_policy(monkeypatch) -> None:
    observed = {}

    def simulated_cold_load(path, payload, timeout_seconds):
        del path
        observed["timeout_seconds"] = timeout_seconds
        assert timeout_seconds > 90.0
        return {
            "model": payload["model"], "message": {"content": '{"candidate_kinds": []}'},
            "done": True, "done_reason": "stop", "load_duration": 120_000_000_000,
        }

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        simulated_cold_load,
    )
    adapter = ExistingOllamaModelUnderstandingAdapter(
        json_schema={"type": "object"}, kind_json_schema={"type": "object"},
    )
    result = adapter.discover_kinds(
        system_prompt="s", user_prompt="u", deadline=RequestDeadline(240),
    )
    assert observed["timeout_seconds"] == 180.0
    assert result["model_call_succeeded"] is True
    assert result["load_duration"] == 120_000_000_000


def test_effective_timeout_is_minimum_of_deadline_and_policy(monkeypatch) -> None:
    observed = {}

    def fake_post(path, payload, timeout_seconds):
        del path, payload
        observed["timeout_seconds"] = timeout_seconds
        return {"ok": False, "error": "ReadTimeout", "message": "timed out"}

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        fake_post,
    )
    adapter = ExistingOllamaModelUnderstandingAdapter(json_schema={"type": "object"})
    result = adapter.understand(
        system_prompt="s", user_prompt="u", deadline=RequestDeadline(12),
    )
    assert 0 < observed["timeout_seconds"] <= 12
    assert result["configured_component_timeout_seconds"] == 180.0
    assert result["effective_transport_timeout_seconds"] == observed["timeout_seconds"]
    assert result["model_call_attempted"] is True
    assert result["model_call_succeeded"] is False
    assert result["transport_error"] == "ReadTimeout:timed out"
    assert result["transport_started_at"] and result["transport_finished_at"]


def test_timeout_truth_resolver_has_no_adapter_local_authority() -> None:
    policy_limited = build_model_call_timeout_truth(
        PRIMARY_CONVERSATION_MODEL_ID, deadline_remaining_seconds=240,
    )
    deadline_limited = build_model_call_timeout_truth(
        PRIMARY_CONVERSATION_MODEL_ID, deadline_remaining_seconds=40,
    )
    assert policy_limited["effective_transport_timeout_seconds"] == 180.0
    assert deadline_limited["effective_transport_timeout_seconds"] == 40.0
    assert policy_limited["timeout_policy_source"] == MODEL_TIMEOUT_POLICY_SOURCE
    assert not hasattr(
        ExistingOllamaModelUnderstandingAdapter(json_schema={}),
        "component_timeout_seconds",
    )


def test_final_brain_sync_and_stream_use_canonical_chat_role_policy(monkeypatch) -> None:
    observed = []

    def fake_call(*, timeout_truth, **kwargs):
        del kwargs
        observed.append(("sync", timeout_truth))
        return {"ok": True, "response_text": "готово"}

    def fake_stream(*, timeout_truth, **kwargs):
        del kwargs
        observed.append(("stream", timeout_truth))
        yield {"event": "done", "response_text": "готово"}

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter."
        "grounded_final_brain_call",
        fake_call,
    )
    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter."
        "grounded_final_brain_stream",
        fake_stream,
    )
    adapter = ExistingFinalBrainAdapter()
    assert adapter.answer(deadline=RequestDeadline(300))["ok"] is True
    assert list(adapter.stream_answer(deadline=RequestDeadline(300)))[-1]["event"] == "done"
    assert [kind for kind, _ in observed] == ["sync", "stream"]
    for _, truth in observed:
        assert truth["model_role"] == "jarvis_chat_model"
        assert truth["configured_component_timeout_seconds"] == 180.0
        assert truth["effective_transport_timeout_seconds"] == 180.0
        assert truth["timeout_policy_source"] == MODEL_TIMEOUT_POLICY_SOURCE


def test_canonical_timeout_failure_is_single_attempt_with_exact_envelope(monkeypatch) -> None:
    calls = []

    def timed_out(path, payload, timeout_seconds):
        del path, payload
        calls.append(timeout_seconds)
        return {"ok": False, "error": "ReadTimeout", "message": "timed out"}

    monkeypatch.setattr(
        "MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter.ollama_post_json",
        timed_out,
    )
    result = ExistingOllamaModelUnderstandingAdapter(
        json_schema={"type": "object"}, kind_json_schema={"type": "object"},
    ).discover_kinds(system_prompt="s", user_prompt="u", deadline=RequestDeadline(300))
    assert calls == [180.0]
    assert result["model_call_attempted"] is True
    assert result["model_call_succeeded"] is False
    assert result["model_call_used"] is False
    assert result["done"] is None
    assert result["raw_output_present"] is False
    assert result["transport_error"] == "ReadTimeout:timed out"
    assert result["effective_transport_timeout_seconds"] == 180.0


import pytest


@pytest.mark.parametrize("state_override,expected_status", [
    ({"approval_required": True}, "PENDING_APPROVAL"),
    ({"policy_execution_allowed": False}, "POLICY_DENIED"),
    ({"provider_available": False}, "PROVIDER_UNAVAILABLE"),
    ({}, "NOT_EXECUTED"),
])
def test_final_brain_preserves_every_nonexecuted_truth_and_never_rewrites_to_complete(
    state_override, expected_status,
) -> None:
    """T11 G: every non-success execution truth (DENIED / UNAVAILABLE / NOT_EXECUTED /
    PENDING_APPROVAL) is surfaced verbatim and NEVER rewritten to COMPLETE."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _bounded_final_brain_inputs
    understanding = {
        "goals": [{"description": "change volume"}],
        "unresolved_capabilities": [], "operation_requirements": [], "confidence": 0.9,
    }
    execution_plan = {
        "steps": [{"step_id": "s1", "capability_id": "windows.volume", "operation": "execute_volume_up"}],
    }
    evidence_bundle = {"receipts": [], "items": []}
    capability_state = [dict({
        "capability_id": "windows.volume", "executed": False, "execution_receipt_present": False,
        "approval_required": False, "policy_execution_allowed": True, "provider_available": True,
    }, **state_override)]
    result = _bounded_final_brain_inputs(
        understanding=understanding, execution_plan=execution_plan,
        evidence_bundle=evidence_bundle, capability_state=capability_state, session_context=None,
    )
    bounded_evidence = result[2]
    mandatory = bounded_evidence.get("mandatory_answer_facts", {})
    rows = mandatory.get("nonexecuted_operations", ())
    assert rows, "nonexecuted truth must be surfaced"
    assert rows[0][2] == expected_status  # exact truth preserved, never COMPLETE


def test_history_prompt_preserves_canonical_learning_authority_without_inferring_review():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import canonical_experience_projection
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _bounded_observation
    from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.developer_experience_contract import DeveloperExperienceRecord
    experience = DeveloperExperienceRecord(
        experience_id="devexp_partial", actor="CODEX", task_ref="repair evidence path",
        evidence_refs=("evidence://original",), failure_class=None, repair_verified=False,
        outcome="pending", provenance_ref="trace://original", verification_status="PARTIAL",
        training_export_allowed=True, training_candidate_creation_allowed=True,
    ).to_read_model()
    assert experience["training_eligible"] is False
    record = canonical_experience_projection({"trace_id":"original", "artifact": {
        "learning_experience": experience, "audit_verdict":"PARTIAL_PENDING_INDEPENDENT_REVIEW",
        "learning_bundle":{"bundle_id":"bundle_original", "schema_version":"v1"},
    }})
    bounded = _bounded_observation("history_search", {"history_query": {
        "query_kind":"REVIEW_STATUS", "matches":[record], "match_count":1,
    }})["matches"][0]
    for key in ("training_eligible", "training_export_allowed", "training_candidate_creation_allowed",
                "active_model_runtime_mutation_allowed", "active_model_auto_promotion_allowed"):
        assert bounded[key] is False
    assert bounded["review_status"] == "PARTIAL_PENDING_INDEPENDENT_REVIEW"
    assert bounded["review_ref"] == ""
    assert bounded["learning_bundle_id"] == "bundle_original"
    assert "reviewer_identity" not in bounded



def _canonical_history_publication_inputs():
    return dict(original_text="Explain this recorded work and its qualification", understanding={},
        execution_plan={"steps":[{"capability_id":"runtime_history_store", "operation":"search_history"}]},
        capability_state=(), evidence_bundle={"items":[{"kind":"history_search", "observation":{
            "history_query":{"query_kind":"REVIEW_STATUS", "match_count":1, "matches":[{
                "experience_id":"devexp_partial", "review_status":"PARTIAL_PENDING_INDEPENDENT_REVIEW",
                "review_ref":"", "training_eligible":False, "training_export_allowed":False,
                "training_candidate_creation_allowed":False, "active_model_auto_promotion_allowed":False,
                "learning_bundle_id":"bundle1"}]}}}]})


def test_history_publication_reuses_strict_same_model_verdict_without_repair(monkeypatch):
    import json, time
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs = _canonical_history_publication_inputs()
    calls=[]
    monkeypatch.setattr(transport,"ollama_get_json", lambda *a,**kw:{"models":[{"name":PRIMARY_CONVERSATION_MODEL_ID}]})
    monkeypatch.setattr(transport,"_measured_final_brain_prompt_budget",lambda *a,**kw:{"within_budget":True})
    verdicts = [
        ({"supported":[1],"contradictions":[],"unsupported_claims":[]}, True),
        ({"supported":[1],"contradictions":[],"unsupported_claims":["invented reviewer"]}, False),
        ({"supported":[1],"contradictions":["training eligibility contradicts False"],"unsupported_claims":[]}, False),
        ({"supported":[1,1],"contradictions":[],"unsupported_claims":[]}, False),
        ({"supported":[True],"contradictions":[],"unsupported_claims":[]}, False),
        ({"supported":[],"contradictions":[],"unsupported_claims":[]}, False),
        ({"supported":[1],"contradictions":[],"unsupported_claims":[],"answer":"replacement"}, False),
        (None, False),
    ]
    for verdict, expected in verdicts:
        def post(path,payload,timeout_seconds):
            calls.append(payload)
            return {"model":PRIMARY_CONVERSATION_MODEL_ID,"message":{"content":json.dumps(verdict)},
                    "done":True,"done_reason":"stop"}
        monkeypatch.setattr(transport,"ollama_post_json",post)
        before=len(calls)
        result=transport._validate_history_publication(content="Model-authored candidate",inputs=inputs,
            deadline_at=time.monotonic()+30)
        assert result["valid"] is expected
        assert len(calls)==before+1
        assert result["correction_attempts"]==0
        assert result["host_answer_synthesized"] is False
        assert calls[-1]["model"]==PRIMARY_CONVERSATION_MODEL_ID
        assert calls[-1]["options"]["num_ctx"]==transport.resident_context_tokens_for_jarvis_model(PRIMARY_CONVERSATION_MODEL_ID)
        material=json.loads(calls[-1]["messages"][-1]["content"])
        assert material["candidate"]=="Model-authored candidate"
        assert material["source_assertions"]["1"]["matches"][0]["training_eligible"] is False


def test_history_publication_missing_evidence_readiness_or_deadline_fails_without_model_call(monkeypatch):
    import time
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport,"ollama_post_json",lambda *a,**kw: (_ for _ in ()).throw(AssertionError("no model call")))
    monkeypatch.setattr(transport,"ollama_get_json",lambda *a,**kw:{"models":[]})
    for inputs, deadline, reason in (
        ({"evidence_bundle":{"items":[]}},time.monotonic()+30,"history_publication_evidence_missing"),
        (_canonical_history_publication_inputs(),time.monotonic()-1,"verification_budget_exhausted"),
        (_canonical_history_publication_inputs(),time.monotonic()+30,"semantic_verifier_not_live_loaded"),
    ):
        result=transport._validate_history_publication(content="candidate",inputs=inputs,deadline_at=deadline)
        assert result["valid"] is False
        assert result["reason"]==reason


def test_sync_and_stream_history_publication_never_expose_a_failed_candidate(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs=_canonical_history_publication_inputs()
    candidate="Reviewed by an invented reviewer; training approved"
    author={"model":PRIMARY_CONVERSATION_MODEL_ID,"message":{"content":candidate},"done":True,"done_reason":"stop"}
    monkeypatch.setattr(transport,"_final_brain_prompt_budget",lambda *a,**kw:{"within_budget":True})
    monkeypatch.setattr(transport,"ollama_post_json",lambda *a,**kw:dict(author))
    class Response:
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def raise_for_status(self):pass
        def iter_lines(self):
            yield json.dumps({"model":PRIMARY_CONVERSATION_MODEL_ID,"message":{"content":candidate[:20]},"done":False})
            yield json.dumps({**author,"message":{"content":candidate[20:]}})
    monkeypatch.setattr(transport.httpx,"stream",lambda *a,**kw:Response())
    for valid in (False,True):
        seen=[]
        def verify(**kwargs):
            seen.append(kwargs["content"])
            return {"valid":valid,"reason":"test_verdict"}
        monkeypatch.setattr(transport,"_validate_history_publication",verify)
        sync=transport.grounded_final_brain_call(**inputs)
        events=list(transport.grounded_final_brain_stream(**inputs))
        assert seen==[candidate,candidate]
        if valid:
            assert sync["response_text"]==candidate and sync["factual_valid"] is True
            assert events[-1]["event"]=="done" and events[-1]["response_text"]==candidate
            assert "".join(e.get("chunk","") for e in events)==candidate
        else:
            assert sync["ok"] is False and sync["response_text"]=="" and sync["raw_response_text"]==candidate
            assert all(e["event"]!="chunk" for e in events)
            assert events[-1]["event"]=="error" and events[-1]["response_text"]==""
            assert events[-1]["raw_response_text"]==candidate
            assert events[-1]["model_call_used"] is False

@pytest.mark.parametrize("wire_format", [None, "json", {"type": "object"}])
def test_grounded_budget_measures_same_bounded_input_for_every_answer_wire_format(monkeypatch, wire_format):
    import copy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload = {"model": PRIMARY_CONVERSATION_MODEL_ID, "stream": False, "think": False,
        "messages": [{"role": "user", "content": "evidence " * 790}],
        "options": {"num_ctx": 4096, "num_predict": 512, "temperature": 0.2}}
    if wire_format is not None:
        payload["format"] = wire_format
    original = copy.deepcopy(payload)
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is False
    calls = []
    def prefill(path, probe, **kwargs):
        calls.append(copy.deepcopy(probe))
        return {"model": PRIMARY_CONVERSATION_MODEL_ID, "done": True, "done_reason": "length",
            "message": {"content": "x"}, "prompt_eval_count": 1700, "eval_count": 1}
    monkeypatch.setattr(transport, "ollama_post_json", prefill)
    measured = transport._measured_final_brain_prompt_budget(payload, timeout_seconds=20)
    assert measured["within_budget"] is True
    assert measured["measured_input_tokens"] == 1700
    assert len(calls) == 1
    assert calls[0]["messages"] == original["messages"]
    assert calls[0].get("format") == original.get("format")
    assert calls[0]["options"] == {**original["options"], "num_predict": 1}
    assert payload == original
    assert measured["tokenizer_probe"]["output_used_as_answer"] is False


@pytest.mark.parametrize("measured_tokens", [0, True, 4000])
def test_plain_answer_prefill_does_not_admit_unproven_or_oversized_input(monkeypatch, measured_tokens):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload = {"model": PRIMARY_CONVERSATION_MODEL_ID, "messages": [{"role":"user", "content":"evidence "*790}],
        "options":{"num_ctx":4096, "num_predict":512}}
    calls=[]
    def prefill(*args, **kwargs):
        calls.append(True)
        return {"model":PRIMARY_CONVERSATION_MODEL_ID, "done":True, "done_reason":"length",
            "message":{"content":"x"}, "prompt_eval_count":measured_tokens, "eval_count":1}
    monkeypatch.setattr(transport, "ollama_post_json", prefill)
    measured=transport._measured_final_brain_prompt_budget(payload,timeout_seconds=20)
    assert calls == [True]
    assert measured["within_budget"] is False
    assert measured["measurement_error"] == "complete_input_token_count_unproven"


def test_plain_answer_prefill_never_sends_input_that_could_truncate(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    def forbidden(*args, **kwargs):
        raise AssertionError("No model call for input exceeding conservative prefill bound")
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    result=transport._measured_final_brain_prompt_budget({"messages":[{"role":"user", "content":"x"*9000}],
        "options":{"num_ctx":4096,"num_predict":512}},timeout_seconds=20)
    assert result["within_budget"] is False
    assert result["measurement_error"] == "prefill_input_not_conservatively_bounded"
@pytest.mark.parametrize("supported,expected", [([1], False), ([1,2,3], True), ([1,2], False)])
def test_history_publication_requires_each_existing_response_obligation(monkeypatch, supported, expected):
    import json,time
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs=_canonical_history_publication_inputs()
    requirements=[{"response_requirement_id":"purpose", "applies_to_goal_ids":["g1"], "description":"Explain the recorded purpose", "memory_query_kind":"PROVENANCE"},
        {"response_requirement_id":"qualification", "applies_to_goal_ids":["g1"], "description":"State recorded qualification and missing independent review", "memory_query_kind":"REVIEW_STATUS"}]
    inputs['evidence_bundle']['items'][0]['observation']['history_query']['matches'][0]['evidence_refs']=['evidence://recorded-purpose']
    for requirement, relation in zip(requirements, ('SOURCE_OF_SUBJECT','LEARNING_QUALIFICATION_OF_EXPERIENCE')):
        requirement['subject_binding']={'scope':'SUBJECT','relation':relation,'subject_goal_id':'g1','experience_id':'devexp_partial'}
    inputs['understanding']={'response_requirements':requirements}
    seen=[]
    monkeypatch.setattr(transport,'ollama_get_json',lambda *a,**kw:{'models':[{'name':PRIMARY_CONVERSATION_MODEL_ID}]})
    def post(path,payload,timeout_seconds):
        seen.append(payload)
        return {'model':PRIMARY_CONVERSATION_MODEL_ID,'done':True,'done_reason':'stop','message':{'content':json.dumps({'supported':supported,'contradictions':[],'unsupported_claims':[],'relations':[[2,1,0],[3,1,0]]})}}
    monkeypatch.setattr(transport,'ollama_post_json',post)
    result=transport._validate_history_publication(content='Unmodified model prose',inputs=inputs,deadline_at=time.monotonic()+30)
    assert result['valid'] is expected
    assert len(seen)==1
    material=json.loads(seen[0]['messages'][-1]['content'])
    assert material['candidate']=='Unmodified model prose'
    assert [material['source_assertions'][str(i+2)]['response_requirement'] for i in range(2)]==requirements
    assert all(material['source_assertions'][str(i+2)]['source_assertion_ids']==[1] for i in range(2))
    assert result['correction_attempts']==0


def test_history_grounding_preserves_record_actor_and_real_receipt_identity():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    record={'experience_id':'exp_runtime','actor':'RUNTIME_ACTOR','non_canonical':True,
        'capability_id':'document.read','operation_id':'read_source',
        'execution_receipts':[{'capability_id':'document.read','operation_id':'read_source','status':'COMPLETE','executed':True}],
        'training_eligible':False,'training_export_allowed':False,'training_candidate_creation_allowed':False}
    bounded=transport._bounded_observation('history_search',{'history_query':{'query_kind':'PROVENANCE','matches':[record],'match_count':1}})
    for field in record:
        assert bounded['matches'][0][field]==record[field]

def test_newly_retained_receipt_evidence_is_not_dropped_by_old_metadata_character_cap():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    record={'experience_id':'actual_exp','actor':'RECORDED_ACTOR','task_ref':'Read the recorded source',
        'execution_receipts':[{'receipt_id':f'receipt_{i}','capability_id':'source.read','operation_id':'read_source',
            'status':'COMPLETE','result':'recorded source observation '*20} for i in range(5)]}
    bounded=transport._bounded_final_brain_inputs(understanding={},execution_plan={},capability_state=(),session_context={},
        evidence_bundle={'items':[{'kind':'history_search','observation':{'history_query':{'query_kind':'PROVENANCE','match_count':1,'matches':[record]}}}]})
    history=next(value for kind,value in bounded[2]['items'] if kind=='history_search')
    assert history['matches'][0]['execution_receipts']==record['execution_receipts']

def test_existing_typed_response_obligations_reach_author_without_host_rewriting():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    requirements=[{'response_requirement_id':'recorded_reason','applies_to_goal_ids':['g1'],
        'description':'Explain the recorded reason; state unknown if not evidenced','memory_query_kind':'PROVENANCE'},
        {'response_requirement_id':'qualification','applies_to_goal_ids':['g1'],
        'description':'State the persisted qualification','memory_query_kind':'REVIEW_STATUS'}]
    inputs=_canonical_history_publication_inputs();inputs['understanding']={'response_requirements':requirements}
    bounded=transport._bounded_final_brain_inputs(understanding=inputs['understanding'],execution_plan=inputs['execution_plan'],
        evidence_bundle=inputs['evidence_bundle'],capability_state=(),session_context={})
    assert bounded[0]['response_requirements']==requirements
    payload=transport._grounded_final_brain_payload(**inputs,stream=False)
    assert json.dumps(requirements,ensure_ascii=False,separators=(',',':')) in payload['messages'][1]['content']
    assert payload['options']['num_ctx']==4096

def test_history_obligation_projection_does_not_change_typed_selfknowledge_prompt_contract():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs={'understanding':{'response_requirements':[{'description':'unchanged selfknowledge requirement'}]},
        'execution_plan':{'steps':[{'capability_id':'build_jarvis_live_memory_federation_status','operation':'read_memory_federation_status'}]},
        'evidence_bundle':{},'capability_state':(),'session_context':{}}
    assert 'response_requirements' not in transport._bounded_final_brain_inputs(**inputs)[0]
@pytest.mark.parametrize("capability,operation,kind", [('runtime_history_store','search_history','history_search'),('mempalace_search','search_mempalace','mempalace_search')])
def test_sync_stream_grounded_memory_gate_receives_original_obligations_and_withholds_failure(monkeypatch,capability,operation,kind):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs=_canonical_history_publication_inputs()
    requirements=[{'response_requirement_id':'proof','applies_to_goal_ids':['g1'],'description':'Explain proof and its limitations','memory_query_kind':'PROVENANCE'}]
    inputs['understanding']={'response_requirements':requirements}
    inputs['execution_plan']={'steps':[{'capability_id':capability,'operation':operation}]}
    if kind=='mempalace_search':inputs['evidence_bundle']={'items':[{'kind':kind,'observation':{'retrieval':{'results':[]}}}]}
    candidate='Unsupported model candidate'
    author={'model':PRIMARY_CONVERSATION_MODEL_ID,'message':{'content':candidate},'done':True,'done_reason':'stop'}
    monkeypatch.setattr(transport,'_final_brain_prompt_budget',lambda *a,**kw:{'within_budget':True})
    monkeypatch.setattr(transport,'ollama_post_json',lambda *a,**kw:dict(author))
    class Response:
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def raise_for_status(self):pass
        def iter_lines(self):yield json.dumps(author)
    monkeypatch.setattr(transport.httpx,'stream',lambda *a,**kw:Response())
    seen=[]
    def verify(**kwargs):
        seen.append(kwargs['inputs'])
        return {'valid':False,'reason':'required_obligation_unproven'}
    monkeypatch.setattr(transport,'_validate_history_publication',verify)
    sync=transport.grounded_final_brain_call(**inputs)
    events=list(transport.grounded_final_brain_stream(**inputs))
    assert len(seen)==2
    assert all(i['understanding']['response_requirements']==requirements for i in seen)
    assert sync['ok'] is False and sync['response_text']==''
    assert all(e['event']!='chunk' for e in events)
    assert events[-1]['event']=='error'


def test_existing_memory_verifier_checks_source_document_obligations_without_history_backend(monkeypatch):
    import json,time
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    seen=[]
    monkeypatch.setattr(transport,'ollama_get_json',lambda *a,**kw:{'models':[{'name':PRIMARY_CONVERSATION_MODEL_ID}]})
    def post(path,payload,timeout_seconds):
        seen.append(payload)
        return {'model':PRIMARY_CONVERSATION_MODEL_ID,'done':True,'done_reason':'stop','message':{'content':json.dumps({'supported':[1],'contradictions':[],'unsupported_claims':[]})}}
    monkeypatch.setattr(transport,'ollama_post_json',post)
    result=transport._validate_history_publication(content='A document alone proves training eligibility',inputs={
        'understanding':{'response_requirements':[{'response_requirement_id':'eligibility','description':'Explain actual qualification','memory_query_kind':'SOURCE_DOCUMENT','applies_to_goal_ids':['g1'],'subject_binding':{'scope':'SUBJECT','relation':'SOURCE_OF_SUBJECT','subject_goal_id':'g1','source_ref':'docs/design.md'}}]},
        'evidence_bundle':{'items':[{'kind':'mempalace_search','observation':{'retrieval':{'results':[{'text':'Source design document','source_file':'docs/design.md'}]}}}]}},deadline_at=time.monotonic()+30)
    assert len(seen)==1
    assert result['valid'] is False
    material=json.loads(seen[0]['messages'][-1]['content'])
    assert material['source_assertions']['1']['evidence_kind']=='mempalace_search'
    assert material['source_assertions']['2']['response_requirement']['response_requirement_id']=='eligibility'
@pytest.mark.parametrize("exact_count,admitted",[(2460,True),(3500,False)])
def test_finalbrain_exact_local_accounting_precedes_conservative_false_positive(monkeypatch,exact_count,admitted):
    import copy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload={'model':PRIMARY_CONVERSATION_MODEL_ID,'think':False,'messages':[{'role':'system','content':'grounded'},{'role':'user','content':'evidence '*1100}],
        'options':{'num_ctx':4096,'num_predict':512}}
    original=copy.deepcopy(payload)
    assert transport._final_brain_prompt_budget(payload)['within_budget'] is False
    monkeypatch.setattr(transport,'_local_final_brain_token_count',lambda *a,**kw:{'available':True,'input_tokens':exact_count,'proof':{'model_bound':True}},raising=False)
    monkeypatch.setattr(transport,'ollama_post_json',lambda *a,**kw:(_ for _ in ()).throw(AssertionError('No generation or prefill for exact local accounting')))
    result=transport._measured_final_brain_prompt_budget(payload,timeout_seconds=20)
    assert result['within_budget'] is admitted
    assert result['actual_input_tokens']==exact_count
    assert result['available_input_tokens']==3424
    assert result['reserved_output_tokens']==512 and result['num_ctx']==4096
    assert payload==original


@pytest.mark.parametrize('invalid',[True,-1,0])
def test_finalbrain_invalid_exact_count_cannot_admit_oversized_input(monkeypatch,invalid):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport,'_local_final_brain_token_count',lambda *a,**kw:{'available':True,'input_tokens':invalid},raising=False)
    monkeypatch.setattr(transport,'ollama_post_json',lambda *a,**kw:(_ for _ in ()).throw(AssertionError('No unsafe prefill')))
    result=transport._measured_final_brain_prompt_budget({'messages':[{'role':'user','content':'x'*11000}],
        'options':{'num_ctx':4096,'num_predict':512}},timeout_seconds=20)
    assert result['within_budget'] is False


def test_exact_admission_keeps_original_sync_stream_payload_without_compaction(monkeypatch):
    import json,copy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload={'model':PRIMARY_CONVERSATION_MODEL_ID,'think':False,'messages':[{'role':'system','content':'grounded'},{'role':'user','content':'evidence '*1100}],
        'options':{'num_ctx':4096,'num_predict':512}}
    builds=[];submitted=[]
    def builder(**kwargs):builds.append(kwargs.get('compact',False));return copy.deepcopy(payload)
    monkeypatch.setattr(transport,'_grounded_final_brain_payload',builder)
    monkeypatch.setattr(transport,'_local_final_brain_token_count',lambda *a,**kw:{'available':True,'input_tokens':2460,'proof':{'model_bound':True}},raising=False)
    author={'model':PRIMARY_CONVERSATION_MODEL_ID,'message':{'content':'model-authored'},'done':True,'done_reason':'stop'}
    def post(path,body,**kw):submitted.append(copy.deepcopy(body));return author
    monkeypatch.setattr(transport,'ollama_post_json',post)
    class Response:
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def raise_for_status(self):pass
        def iter_lines(self):yield json.dumps(author)
    monkeypatch.setattr(transport.httpx,'stream',lambda *a,**kw:Response())
    inputs=dict(original_text='original request',understanding={},execution_plan={},evidence_bundle={},capability_state=())
    sync=transport.grounded_final_brain_call(**inputs);stream=list(transport.grounded_final_brain_stream(**inputs))
    assert sync['ok'] is True and stream[-1]['event']=='done'
    assert builds==[False,False]
    assert submitted==[payload]
    assert sync['prompt_budget']['actual_input_tokens']==2460

def test_exact_renderer_preserves_actual_qwen3_collation_and_whitespace():
    import copy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload={'model':PRIMARY_CONVERSATION_MODEL_ID,'think':False,'messages':[
        {'role':'system','content':'Система\n'}, {'role':'user','content':'First\n'}, {'role':'user','content':'Second'}]}
    original=copy.deepcopy(payload)
    assert transport._render_supported_ollama_text_prompt(payload)==(
        '<|im_start|>system\n\nСистема\n<|im_end|>\n<|im_start|>user\nFirst\n\n\nSecond /no_think<|im_end|>\n'
        '<|im_start|>assistant\n<think>\n\n</think>\n\n')
    assert payload==original


@pytest.mark.parametrize('change',[{'think':True},{'format':'json'},{'tools':[]},
    {'messages':[{'role':'user','content':'missing system'}]},
    {'messages':[{'role':'system','content':'s'},{'role':'assistant','content':'a'}]},
    {'messages':[{'role':'system','content':'s'},{'role':'user','content':'u','images':['x']}]}])
def test_unknown_native_accounting_shape_is_unavailable_not_guessed(monkeypatch,change):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload={'model':PRIMARY_CONVERSATION_MODEL_ID,'think':False,'messages':[{'role':'system','content':'s'},{'role':'user','content':'u'}],**change}
    monkeypatch.setattr(transport,'_native_ollama_vocabulary_count',lambda *a,**kw:(_ for _ in ()).throw(AssertionError('No native load for unsupported framing')))
    result=transport._local_final_brain_token_count(payload,timeout_seconds=10)
    assert result['available'] is False


def test_unavailable_exact_counter_preserves_conservative_fail_closed_without_generation(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport,'_local_final_brain_token_count',lambda *a,**kw:{'available':False,'reason':'unknown native ABI'})
    monkeypatch.setattr(transport,'ollama_post_json',lambda *a,**kw:(_ for _ in ()).throw(AssertionError('No unsafe generation')))
    result=transport._measured_final_brain_prompt_budget({'messages':[{'role':'user','content':'x'*11000}],
        'options':{'num_ctx':4096,'num_predict':512}},timeout_seconds=20,allow_prefill=False)
    assert result['within_budget'] is False
    assert result['exact_accounting_unavailable']=='unknown native ABI'


def test_exact_accounting_cannot_extend_existing_deadline(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport,'_local_final_brain_token_count',lambda *a,**kw:{'available':True,'input_tokens':2})
    times=iter([10.0,12.0]);monkeypatch.setattr(transport.time,'monotonic',lambda:next(times,12.0))
    result=transport._measured_final_brain_prompt_budget({'messages':[{'role':'user','content':'x'}],
        'options':{'num_ctx':4096,'num_predict':512}},timeout_seconds=1)
    assert result['within_budget'] is False and result['measurement_error']=='request_deadline_exhausted'


# Downstream stream units mock external resource facts, never admission itself.
import pytest as _resource_pytest

@_resource_pytest.fixture(autouse=True)
def _grounded_stream_resource_facts(request, monkeypatch, tmp_path):
    if request.node.originalname == "test_final_brain_request_uses_canonical_live_keep_alive":
        from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
        monkeypatch.setattr(transport, "_local_final_brain_token_count", lambda *a, **k:
            {"available": False, "reason": "keep_alive unit fixture has no live tokenizer metadata"})
        return
    if request.node.originalname not in {'test_exact_admission_keeps_original_sync_stream_payload_without_compaction', 'test_streaming_done_preserves_sanitized_ollama_telemetry', 'test_sync_and_stream_history_publication_never_expose_a_failed_candidate', 'test_sync_stream_grounded_memory_gate_receives_original_obligations_and_withholds_failure'}:
        return
    from tests.ai_orchestration.test_model_admission_transport import acquisition
    acquisition.__wrapped__(monkeypatch, tmp_path)
