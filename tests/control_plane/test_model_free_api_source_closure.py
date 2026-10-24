"""Real API lifespan with synthetic health metadata; no server or model starts."""
import asyncio
import subprocess
import pytest

from control_plane.offline_api_source_fixtures import no_external_package_import_probe
import CONTROL_PLANE.api_server as api
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
from MAKSIMAR_SERVER.AI_ORCHESTRATION import browser_provider_adapter as browser, ollama_transport as transport


@pytest.mark.parametrize("metadata_available",[False,True])
def test_actual_api_lifespan_uses_readiness_metadata_without_generation(tmp_path,monkeypatch,metadata_available):
    calls=[]
    def metadata(url,**kwargs):
        calls.append(("GET",url))
        return {"ok":metadata_available,"models":[]}
    def forbidden(*a,**k):pytest.fail("startup attempted model generation/provider effect")
    monkeypatch.setattr(obs,"ollama_get_json",metadata)
    monkeypatch.setattr(obs.ExistingWindowsEdgeAdapter,"health",lambda self:{"status":"UNAVAILABLE"})
    monkeypatch.setattr(transport,"ollama_post_json",forbidden)
    monkeypatch.setattr(transport,"grounded_final_brain_call",forbidden)
    executable=tmp_path/"browser-python";executable.touch();monkeypatch.setattr(browser,"BROWSER_PYTHON",executable)
    def import_probe(argv,**kwargs):
        assert argv==[str(executable),"-c","import playwright; print('ok')"]
        calls.append(("BROWSER_IMPORT",argv))
        return subprocess.CompletedProcess(argv,0,"ok\n","")
    monkeypatch.setattr(browser.subprocess,"run",import_probe)
    for name in ["PROJECT_UNDERSTANDING_ADAPTER","MEMORY_RETRIEVAL_ADAPTER","SIMULATION_WORKER_ADAPTER","N8N_ADAPTER","MODEL_ROLE_ADAPTER","MEDIA_PROVIDER_ADAPTER","BROWSER_PROVIDER_ADAPTER","WINDOWS_EDGE_ADAPTER","CONVERSATION_EVIDENCE_ADAPTER"]:
        adapter=getattr(api,name,None)
        if adapter is not None and hasattr(adapter,"collect_evidence"):monkeypatch.setattr(adapter,"collect_evidence",forbidden)
    async def cycle():
        async with api._control_plane_lifespan(api.app):
            projection=api._semantic_capability_projection()
            assert projection["capability_count"]>0
            ids={x["capability_id"] for x in projection["entries"]}
            assert {"project.read","conversation.respond"}<=ids
            readiness=obs.build_runtime_readiness_payload()
            assert readiness["chat_model_ready"] is False
            assert readiness["chat_model_ready_context_tokens"]==4096
    asyncio.run(cycle())
    assert any(kind=="BROWSER_IMPORT" for kind,_ in calls)
    assert all(kind in {"GET","BROWSER_IMPORT"} for kind,_ in calls)


def test_api_uses_one_existing_spine_final_brain_policy_and_session_owner():
    from CONTROL_PLANE import canonical_semantic_spine as spine
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import ExistingFinalBrainAdapter
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import CanonicalSessionContextStore
    from MAKSIMAR_CORE_LIB.security_layer.host_approval_handshake import CANONICAL_HOST_APPROVAL_STORE
    from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
    assert api.run_canonical_semantic_turn is spine.run_canonical_semantic_turn
    assert api.stream_canonical_semantic_turn is spine.stream_canonical_semantic_turn
    assert type(api.FINAL_BRAIN_ADAPTER) is ExistingFinalBrainAdapter
    assert type(api.CANONICAL_SESSION_CONTEXT) is CanonicalSessionContextStore
    assert type(api.PROJECT_READ_PERMISSION) is SemanticPolicyEvaluator
    assert api.CANONICAL_HOST_APPROVAL_STORE is spine.CANONICAL_HOST_APPROVAL_STORE is CANONICAL_HOST_APPROVAL_STORE


def test_unavailable_external_adapters_remain_visible_without_execution_authority():
    from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import build_jarvis_external_adapter_visibility_read_model
    result=build_jarvis_external_adapter_visibility_read_model({"probe_results":(),"runtime_python":"synthetic-unavailable-runtime"})
    assert result["active_adapter_ids"]==()
    assert result["visible_adapter_ids"]
    assert set(result["unavailable_adapter_ids"])<=set(result["visible_adapter_ids"])
