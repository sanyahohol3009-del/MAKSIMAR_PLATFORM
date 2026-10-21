from dataclasses import replace
from contextlib import contextmanager
from urllib.parse import urlsplit
import json
import time
import pytest
from MAKSIMAR_CORE_LIB.ai_orchestration import model_profile_registry_contract as registry
from MAKSIMAR_CORE_LIB.ai_orchestration.model_resource_requirements_contract import ModelLoadResourceDemand
from MAKSIMAR_CORE_LIB.execution_control.admission_models import ModelResourceObservation
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
from SUPERVISOR import runtime_preflight as preflight
from tests.runtime.test_preflight_recovery_truth import _observation

G = 1024 ** 3

@pytest.fixture
def acquisition(monkeypatch, tmp_path):
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "0")
    profiles = registry.build_jarvis_live_runtime_model_role_profiles()
    original = registry.resolve_runtime_model_profile(role_id="jarvis_chat_model")
    demand = ModelLoadResourceDemand(original.model_id, original.backend_id, "fixture-revision", 4096,
        1, 8 * G, (("fixture-gpu", 6 * G),), 4, "fixture full-load validation", 5,
        bound_kind="VERIFIED_UPPER_BOUND")
    profile = replace(original, load_resource_demand=demand)
    configured = {p.role_id: p for p in profiles}; configured[profile.role_id] = profile
    monkeypatch.setattr(registry, "build_jarvis_live_runtime_model_role_profiles", lambda: tuple(configured.values()))
    runtime = _observation(); runtime["decision"] = preflight.classify_runtime_observation(runtime)
    assert runtime["decision"]["healthy"] is True
    monkeypatch.setattr(preflight, "inspect_runtime_state", lambda: runtime)
    from CORE_ROOT import runtime_paths
    monkeypatch.setattr(runtime_paths, "DEGRADED_MODE_FILE", tmp_path / "degraded")
    state = {"profile": profile, "configured": configured, "runtime": runtime,
             "posts": [], "gets": [], "streams": [], "observations": [], "next_observation": None, "real_observe": transport._observe_model_resources}
    def observe(selected):
        state["observations"].append(selected.model_id)
        return state["next_observation"] or ModelResourceObservation(time.monotonic(), selected.backend_id,
            "fixture-host", "fixture-provider", True, "fixture-revision", (("host", 32 * G),),
            (("fixture-gpu", 80 * G),), 16, True, True, True,
            "fixture independent atomic exclusion", 0, (), True, "fixture external observation")
    monkeypatch.setattr(transport, "_observe_model_resources", observe)
    class Response:
        def __init__(self, payload): self.payload=payload; self.status_code=200; self.content=json.dumps(payload).encode()
        def raise_for_status(self): pass
        def json(self): return self.payload
    def post(url, *, json, timeout):
        state["posts"].append((url, json, timeout))
        return Response({"model": json["model"], "done": True, "done_reason": "stop", "response": "ready",
            "message": {"content": "controlled response"}})
    def get(url, **kwargs):
        state["gets"].append(url)
        models=[{"name": p.model_id, "digest": "fixture-revision", "context_length": p.resident_context_tokens or p.default_context_tokens} for p in configured.values()]
        return Response({"models": models})
    monkeypatch.setattr(transport.httpx, "post", post)
    monkeypatch.setattr(transport.httpx, "get", get)
    monkeypatch.setattr(transport, "_local_final_brain_token_count", lambda *a, **k: {"available": False, "reason": "offline fixture"})
    state["payload"] = {"model": profile.model_id, "stream": False, "options": {"num_ctx": 4096}, "prompt": "fixture"}
    return state


def test_actual_transport_executes_canonical_admission_before_one_effect(acquisition):
    result = transport.ollama_post_json("/api/generate", acquisition["payload"])
    assert len(acquisition["posts"]) == 1 and result["resource_admission"]["admitted"] is True
    assert len(acquisition["observations"]) == 1


@pytest.mark.parametrize("case", ["unknown_demand", "policy", "stopgate", "foreign", "low_ram", "low_vram", "stale", "provider_down", "unknown_owner", "unknown_model", "wrong_revision"])
def test_actual_transport_rejected_admission_has_zero_model_post(acquisition, monkeypatch, tmp_path, case):
    s=acquisition; p=s["profile"]
    base=transport._observe_model_resources(p)
    s["observations"].clear()
    changes={"foreign":{"resident_models":(("foreign-model","other"),)},
        "low_ram":{"memory_available_bytes":(("host", G),)},
        "low_vram":{"accelerator_available_bytes":(("fixture-gpu", G),)},
        "stale":{"observed_monotonic":time.monotonic()-10},
        "provider_down":{"provider_available":False},
        "unknown_owner":{"ownership_verified":False}, "wrong_revision":{"model_revision":"other"}}
    if case in changes:s["next_observation"]=replace(base,**changes[case])
    elif case=="unknown_demand":s["configured"][p.role_id]=replace(p,load_resource_demand=None)
    elif case=="unknown_model":s["payload"]["model"]="unregistered-fixture-model"
    elif case=="policy":s["runtime"]["decision"]={**s["runtime"]["decision"],"healthy":False}
    elif case=="stopgate":
        from CORE_ROOT import runtime_paths
        runtime_paths.DEGRADED_MODE_FILE.write_text("fixture deny")
    result=transport.ollama_post_json("/api/generate",s["payload"])
    assert result["ok"] is False and result["model_call_attempted"] is False and not s["posts"]
    assert result["resource_admission"]["admitted"] is False


@pytest.mark.parametrize("method", ["get","post","stream"])
def test_model_free_prohibits_all_provider_io(acquisition, monkeypatch, method):
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP","1")
    if method=="get":result=transport.ollama_get_json("/api/ps")
    elif method=="post":result=transport.ollama_post_json("/api/generate",acquisition["payload"])
    else:
        with transport._model_effect_admission(transport.OLLAMA_CHAT_URL,acquisition["payload"]) as result:
            assert not result.admitted
    assert not acquisition["posts"] and not acquisition["gets"] and not acquisition["observations"]


def test_profile_swap_and_warmup_use_real_common_admission(acquisition):
    from tools.jarvis_live_runtime import model_warmup_probe as probe
    s=acquisition; p=s["profile"]; future="fixture-future-configured-primary"
    s["configured"][p.role_id]=replace(p,model_id=future,
        load_resource_demand=replace(p.load_resource_demand,model_id=future))
    result=probe.build_model_warmup_probe_read_model(primary_only=True,warmup_enabled=True)
    loads=[v for v in s["posts"] if urlsplit(v[0]).path=="/api/generate"]
    assert len(loads)==1 and loads[0][1]["model"]==future
    assert result["models"][0]["model_id"]==future and result["models"][0]["model_ready"]
    assert result["models"][0]["resource_admission"]["admitted"]
    assert transport.model_role_for_model_id(future)=="jarvis_chat_model"


def test_rejected_warmup_reports_no_actual_load_attempt(acquisition):
    from tools.jarvis_live_runtime import model_warmup_probe as probe
    p=acquisition["profile"]; acquisition["configured"][p.role_id]=replace(p,load_resource_demand=None)
    result=probe.build_model_warmup_probe_read_model(primary_only=True,warmup_enabled=True)
    row=result["models"][0]
    assert row["status"]=="admission_denied" and row["warmup_attempted"] is False
    assert not [v for v in acquisition["posts"] if urlsplit(v[0]).path=="/api/generate"]


def test_each_operation_and_heavy_transition_requires_fresh_admission(acquisition):
    s=acquisition
    assert transport.ollama_post_json("/api/generate",s["payload"])["resource_admission"]["admitted"]
    s["next_observation"]=replace(transport._observe_model_resources(s["profile"]),ownership_verified=False)
    assert not transport.ollama_post_json("/api/generate",s["payload"])["resource_admission"]["admitted"]
    heavy=registry.resolve_runtime_model_profile(role_id="heavy_reasoning_model")
    result=transport.ollama_post_json("/api/chat",{"model":heavy.model_id,"options":{"num_ctx":heavy.default_context_tokens}})
    assert not result["resource_admission"]["admitted"]
    assert len(s["posts"])==1


def test_direct_stream_guard_is_real_and_releases_slot_at_terminal(acquisition,monkeypatch):
    s=acquisition
    class Response:
        def raise_for_status(self):pass
        def iter_lines(self):
            yield json.dumps({"model":s["profile"].model_id,"message":{"content":"controlled response"},"done":False})
            yield json.dumps({"model":s["profile"].model_id,"message":{"content":""},"done":True,"done_reason":"stop"})
    @contextmanager
    def stream(*args,**kwargs):
        s["streams"].append(kwargs); yield Response()
    monkeypatch.setattr(transport.httpx,"stream",stream)
    events=list(transport.grounded_final_brain_stream(timeout_seconds=30, original_text="fixture", understanding={}, execution_plan={}, evidence_bundle={}, capability_state={}))
    assert len(s["streams"])==1 and events[-1]["event"]=="done"
    # A terminal stream no longer holds a local acquisition slot.
    assert transport.ollama_post_json("/api/generate",s["payload"])["resource_admission"]["admitted"]


def test_current_ollama_adapter_never_invents_exclusive_ownership(acquisition, monkeypatch):
    from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import hardware_detection_adapter as hardware
    monkeypatch.setattr(hardware,"detect_model_resource_observation",lambda:{"observed_monotonic":time.monotonic(),
        "scope_id":"fixture-host","scope_complete":True,"memory_available_bytes":(("host",32*G),),
        "accelerator_available_bytes":(("fixture-gpu",80*G),),"cpu_threads":16,
        "physical_identity_verified":True,"source":"fixture hardware"})
    # Original existing adapter; only external hardware/HTTP facts are controlled.
    observation=acquisition["real_observe"](acquisition["profile"])
    assert observation.ownership_verified is False and observation.active_concurrency is None
    assert observation.provider_instance_id=="" and not acquisition['posts']


def test_direct_stream_rejects_before_http_effect(acquisition,monkeypatch):
    p=acquisition["profile"];acquisition["configured"][p.role_id]=replace(p,load_resource_demand=None)
    monkeypatch.setattr(transport.httpx,"stream",lambda *a,**k:pytest.fail("rejected stream reached HTTP"))
    events=list(transport.grounded_final_brain_stream(timeout_seconds=30, original_text="fixture",
        understanding={},execution_plan={},evidence_bundle={},capability_state={}))
    assert events[-1]["error_kind"]=="model_resource_admission_rejected"
    assert events[-1]["model_call_attempted"] is False


def test_admission_observation_cannot_extend_transport_budget(acquisition,monkeypatch):
    clock={"now":100.0};monkeypatch.setattr(transport.time,"monotonic",lambda:clock["now"])
    original=transport._observe_model_resources
    def slow(profile):
        clock["now"]+=11
        return original(profile)
    monkeypatch.setattr(transport,"_observe_model_resources",slow)
    result=transport.ollama_post_json("/api/generate",acquisition["payload"],timeout_seconds=10)
    assert result["error"]=="model_admission_budget_exhausted" and not acquisition["posts"]


@pytest.mark.parametrize("kind", ["stopgate", "new_run"])
def test_authority_change_during_observation_cannot_admit_effect(acquisition,monkeypatch,kind):
    from CORE_ROOT import runtime_paths
    original=transport._observe_model_resources
    def observed(profile):
        value=original(profile)
        if kind=="stopgate":runtime_paths.DEGRADED_MODE_FILE.write_text("fixture stop")
        else:
            runtime=acquisition["runtime"]
            runtime["run_metadata"]["run_id"]="fixture-new-run"
            for receipt in runtime["heartbeats"].values():receipt["run_id"]="fixture-new-run"
            runtime["decision"]=preflight.classify_runtime_observation(runtime)
            assert runtime["decision"]["healthy"]
        return value
    monkeypatch.setattr(transport,"_observe_model_resources",observed)
    result=transport.ollama_post_json("/api/generate",acquisition["payload"])
    assert result["message"]=="model_admission_authority_changed" and not acquisition["posts"]


@pytest.mark.parametrize("role", ["helper_input_correction_model", "heavy_reasoning_model", "daily_coder_model"])
def test_nonprimary_acquisition_is_role_resolved_not_eager_or_author_substitution(acquisition,role):
    s=acquisition;p=s["configured"][role];context=p.resident_context_tokens or p.default_context_tokens
    demand=replace(s["profile"].load_resource_demand,model_id=p.model_id,context_tokens=context)
    s["configured"][role]=replace(p,load_resource_demand=demand)
    assert not s["posts"]
    result=transport.ollama_post_json("/api/chat",{"model":p.model_id,"options":{"num_ctx":context}})
    assert result["resource_admission"]["admitted"] and result["resource_admission"]["role_id"]==role
    assert s["posts"][0][1]["model"]==p.model_id
    assert transport.DEFAULT_OLLAMA_MODEL_ID==s["profile"].model_id


@pytest.mark.parametrize("error", ["timeout", "unavailable"])
def test_provider_error_truth_and_admission_cleanup(acquisition,monkeypatch,error):
    def failed(*args,**kwargs):
        acquisition["posts"].append("failed controlled request")
        raise (transport.httpx.ReadTimeout("fixture timeout") if error=="timeout" else transport.httpx.ConnectError("fixture unavailable"))
    monkeypatch.setattr(transport.httpx,"post",failed)
    result=transport.ollama_post_json("/api/generate",acquisition["payload"])
    assert result["ok"] is False and result["model_call_attempted"] is True
    with transport._model_effect_admission(transport.OLLAMA_CHAT_URL,acquisition["payload"]) as next_decision:
        assert next_decision.admitted


def test_stream_terminal_scope_allows_existing_followup_correction(acquisition,monkeypatch):
    s=acquisition
    class Response:
        def raise_for_status(self):pass
        def iter_lines(self):
            yield json.dumps({"model":s["profile"].model_id,"message":{"content":"controlled"},"done":False})
            yield json.dumps({"model":s["profile"].model_id,"message":{"content":""},"done":True,"done_reason":"stop"})
    @contextmanager
    def stream(*a,**kw):yield Response()
    monkeypatch.setattr(transport.httpx,"stream",stream)
    original=transport._flush_private_reasoning
    def terminal(state):
        result=transport.ollama_post_json("/api/generate",s["payload"])
        assert result["resource_admission"]["admitted"]
        return original(state)
    monkeypatch.setattr(transport,"_flush_private_reasoning",terminal)
    events=list(transport.grounded_final_brain_stream(timeout_seconds=30,original_text="fixture",
        understanding={},execution_plan={},evidence_bundle={},capability_state={}))
    assert events[-1]["event"]=="done" and len(s["posts"])==1


def test_model_free_warmup_is_not_misreported_as_missing_model(acquisition,monkeypatch):
    from tools.jarvis_live_runtime import model_warmup_probe as probe
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP","1")
    result=probe.build_model_warmup_probe_read_model(primary_only=True,warmup_enabled=True)
    row=result["models"][0]
    assert row["status"]=="disabled_model_free" and row["installed"] is None
    assert not row["warmup_attempted"] and not acquisition["gets"] and not acquisition["posts"]


def test_actual_transport_concurrent_client_cannot_bypass_local_admission(acquisition,monkeypatch):
    import threading
    entered,release=threading.Event(),threading.Event();results=[]
    original=transport.httpx.post
    def slow(*a,**kw):
        entered.set();assert release.wait(3)
        return original(*a,**kw)
    monkeypatch.setattr(transport.httpx,"post",slow)
    worker=threading.Thread(target=lambda:results.append(transport.ollama_post_json("/api/generate",acquisition["payload"])))
    worker.start();assert entered.wait(3)
    try:
        second=transport.ollama_post_json("/api/generate",acquisition["payload"])
        assert second["resource_admission"]["reason"]=="local_admission_busy"
        assert second["model_call_attempted"] is False
    finally:
        release.set();worker.join(3)
    assert not worker.is_alive() and results[0]["resource_admission"]["admitted"]
    assert len(acquisition["posts"])==1


@pytest.mark.parametrize("keep_alive", [0, "0", "0s"])
def test_owned_nonempty_inference_can_request_no_post_response_residency(acquisition, keep_alive):
    payload={**acquisition["payload"],"keep_alive":keep_alive}
    result=transport.ollama_post_json("/api/generate",payload)
    assert result["resource_admission"]["admitted"] and len(acquisition["posts"])==1
    assert acquisition["posts"][0][1]["keep_alive"]==keep_alive
    # Request policy is not independent proof of physical release.
    assert "resources_actually_released" not in result


@pytest.mark.parametrize("path,payload", [
    ("/api/generate",{"prompt":""}),
    ("/api/chat",{"messages":[]}),
    ("/api/chat",{"messages":[{"role":"user","content":""}]})])
def test_empty_release_effect_remains_denied_before_provider(acquisition,path,payload):
    body={"model":acquisition["profile"].model_id,"options":{"num_ctx":4096},"keep_alive":0,**payload}
    result=transport.ollama_post_json(path,body)
    assert not result["resource_admission"]["admitted"] and not result["model_call_attempted"]
    assert not acquisition["posts"]


@pytest.mark.parametrize("case",["foreign_owner","foreign_resident","low_headroom","stopgate"])
def test_inference_release_policy_never_bypasses_resource_authority(acquisition,case):
    from CORE_ROOT import runtime_paths
    s=acquisition;observation=transport._observe_model_resources(s["profile"])
    changes={"foreign_owner":{"ownership_verified":False},
        "foreign_resident":{"resident_models":(("foreign-fixture-model","foreign-revision"),)},
        "low_headroom":{"memory_available_bytes":(("host",G),)}}
    if case=="stopgate":runtime_paths.DEGRADED_MODE_FILE.write_text("fixture denied")
    else:s["next_observation"]=replace(observation,**changes[case])
    result=transport.ollama_post_json("/api/generate",{**s["payload"],"keep_alive":0})
    assert not result["resource_admission"]["admitted"] and not result["model_call_attempted"]
    assert not s["posts"]


@pytest.mark.parametrize("future_names",[False,True])
def test_existing_structured_adapter_primary_heavy_primary_uses_same_admission(acquisition,monkeypatch,future_names):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import model_understanding_adapter as adapter
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline
    s=acquisition;primary=s["profile"];heavy=s["configured"]["heavy_reasoning_model"]
    for profile in (primary,heavy):
        model_id=("fixture-future-"+profile.role_id) if future_names else profile.model_id
        context=profile.resident_context_tokens or profile.default_context_tokens
        demand=replace(primary.load_resource_demand,model_id=model_id,context_tokens=context)
        s["configured"][profile.role_id]=replace(profile,model_id=model_id,load_resource_demand=demand)
    primary=s["configured"][primary.role_id];heavy=s["configured"][heavy.role_id]
    effects=[]
    class Response:
        status_code=200;content=b'{"ok":true}'
        def raise_for_status(self):pass
        def json(self):return {"model":effects[-1]["model"],"message":{"content":'{"ok":true}'},"done":True,"done_reason":"stop"}
    def provider(url,*,json,timeout):effects.append(json);return Response()
    monkeypatch.setattr(transport.httpx,"post",provider)
    schema={"type":"object","additionalProperties":False,"required":["ok"],"properties":{"ok":{"type":"boolean"}}}
    model=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema=schema)
    deadline=RequestDeadline(30)
    s["observations"].clear()
    for selected,keep in [(primary,None),(heavy,0),(primary,None)]:
        result=model._main_model_call(system_prompt="offline bounded fixture",user_prompt="fixture input",deadline=deadline,
            schema=schema,num_predict=16,deadline_error="fixture_deadline",model_id=selected.model_id,
            keep_alive=keep,num_ctx=selected.resident_context_tokens or selected.default_context_tokens)
        assert result["ok"] and result["final_valid"]
    assert [p["model"] for p in effects]==[primary.model_id,heavy.model_id,primary.model_id]
    assert [p["keep_alive"] for p in effects]==["1800s",0,"1800s"]
    assert s["observations"]==[primary.model_id,heavy.model_id,primary.model_id]
    assert [a["model_role"] for a in deadline.understanding_model_attempts]==[primary.role_id,heavy.role_id,primary.role_id]
    # Controlled external observations are empty at each acquire; this case does
    # not prove eviction of a previous resident or physical VRAM release.
