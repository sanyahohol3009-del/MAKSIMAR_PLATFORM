"""Pure transport/session boundary checks; no real model/provider calls."""
import pytest
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport, session_memory_store as sessions


@pytest.mark.parametrize("done,content,success",[(True,"{}",True),(False,"{}",False),(None,"{}",False),(True,"",False)])
def test_transport_terminal_evidence_cannot_claim_canonical_publication(done,content,success):
    raw={"model":transport.PRIMARY_CONVERSATION_MODEL_ID,"done":done,"message":{"content":content}}
    result=transport.ollama_model_call_result(raw,expected_model_id=transport.PRIMARY_CONVERSATION_MODEL_ID,requested_num_ctx=4096,transport_attempted=True)
    assert result["ok"] is success
    assert result["model_call_used"] is False
    assert result["requested_num_ctx"]==4096


def test_canonical_session_restart_readback_remains_identity_and_session_isolated(tmp_path,monkeypatch):
    monkeypatch.setattr(sessions,"SESSION_MEMORY_ROOT",tmp_path/"sessions")
    identity=IdentityContext("synthetic-a","local_terminal_session","owner",True,True)
    other=IdentityContext("synthetic-b","http_unverified","unknown",False,False)
    first=sessions.CanonicalSessionContextStore()
    first.append("s1",identity,user_text="synthetic user",assistant_text="synthetic answer",topic="synthetic",unresolved_reference="",trace_id="trace-test")
    restored=sessions.CanonicalSessionContextStore()
    assert restored.read("s1",identity)["bounded_chronological_turns"][0]["assistant_text"]=="synthetic answer"
    assert restored.read("s1",other)["bounded_chronological_turns"]==()
    assert restored.read("s2",identity)["bounded_chronological_turns"]==()


@pytest.mark.parametrize("escape",["../outside.json","/tmp/outside.json"])
def test_library_source_reference_cannot_escape_canonical_store(tmp_path,escape):
    import json
    from MAKSIMAR_CORE_LIB.project_read.jarvis_runtime_library_store import build_runtime_library_store_read_model
    root=tmp_path/"library";(root/"manifests").mkdir(parents=True)
    (root/"manifests/p.json").write_text(json.dumps({"manifest_id":"synthetic","report_file":escape}))
    result=build_runtime_library_store_read_model(root)
    assert result["available_count"]==0 and result["current_execution_verified"] is False
    assert any(x["status"]=="PATH_DENIED" for x in result["source_errors"])


def test_library_historical_probe_does_not_become_current_execution(tmp_path):
    import json
    from MAKSIMAR_CORE_LIB.project_read.jarvis_runtime_library_store import build_runtime_library_store_read_model
    root=tmp_path/"library";(root/"manifests").mkdir(parents=True);(root/"probe_reports").mkdir()
    (root/"manifests/p.json").write_text(json.dumps({"manifest_id":"synthetic","category":"agents"}))
    (root/"probe_reports/agents_import_probe.json").write_text(json.dumps({"observed_at":"2000-01-01T00:00:00Z","packages":[{"pip_name":"synthetic","import_ok":True}]}))
    result=build_runtime_library_store_read_model(root)
    assert result["available_count"]==1
    assert result["current_execution_verified"] is False and result["direct_execution_allowed"] is False
