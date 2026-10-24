"""Existing model-free startup/probe consumers; all effects are spies/TMP fixtures."""
import asyncio
from contextlib import nullcontext
import importlib
import json
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace
import pytest
from CORE_ROOT import run_context
from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as probe
from MAKSIMAR_CORE_LIB.action_library_adapters import external_tool_library_adapter as consumer


def forbidden(*args,**kwargs):
    pytest.fail("unexpected external import/process/model effect")


@pytest.mark.parametrize("value,expected", [(None,False),("0",False),("1",True)])
def test_process_local_context_not_cached(monkeypatch,value,expected):
    monkeypatch.delenv(run_context.MODEL_FREE_STARTUP_ENV,raising=False)
    if value is not None:monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,value)
    assert run_context.model_free_startup() is expected
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,"0")
    assert run_context.model_free_startup() is False


@pytest.mark.parametrize("value", ["true","false","", "2"])
def test_invalid_context_cannot_enable_probes(monkeypatch,value):
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,value)
    monkeypatch.setattr(probe.subprocess,"run",forbidden)
    with pytest.raises(ValueError):probe._probe_import_with_runtime_python("missing","smolagents","smolagents")


def test_model_free_actual_probe_and_consumers_keep_manifest_visibility_without_selection(monkeypatch):
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,"1")
    monkeypatch.setattr(probe.subprocess,"run",forbidden)
    manifests=probe.load_external_tool_manifests()
    assert any(m.tool_id=="external_adapter:smolagents" for m in manifests)
    report=probe.build_agent_tooling_runtime_probe_read_model()
    imports=[x for x in report["probe_results"] if x["probe_kind"]=="IMPORT"]
    assert imports
    assert all(x["import_attempted"] is False and x["import_probe_passed"] is False
               and x["runtime_capability_verified"] is False and x["installed"] is False for x in imports)
    assert all(x["errors"]==("model_free_import_not_attempted",) for x in imports)
    visibility=consumer.build_jarvis_external_adapter_visibility_read_model(report)
    assert set(visibility["visible_adapter_ids"])=={m.tool_id for m in manifests}
    assert visibility["active_adapter_ids"]==()
    smol=next(x for x in visibility["adapters"] if x["tool_id"]=="external_adapter:smolagents")
    assert smol["selection_enabled"] is False and smol["safe_direct_allowed"] is False
    assert smol["availability_status"]=="unavailable"
    assert consumer.normalize_external_adapter_tool_ids(("external_adapter:smolagents",),report)==()


def test_real_api_lifespan_model_free_never_imports_external_providers_or_loads_weights(monkeypatch):
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,"1")
    import CONTROL_PLANE.api_server as api
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import existing_capability_inventory as inventory
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(probe.subprocess,"run",forbidden)
    real_import=importlib.import_module
    attempted=[]
    def import_spy(name,*args,**kwargs):
        if name.split('.')[0] in {"smolagents","torch","transformers","playwright","llama_cpp"}:
            attempted.append(name);forbidden()
        return real_import(name,*args,**kwargs)
    monkeypatch.setattr(importlib,"import_module",import_spy)
    monkeypatch.setattr(transport,"ollama_post_json",forbidden)
    monkeypatch.setattr(transport,"grounded_final_brain_call",forbidden)
    metadata=[]
    monkeypatch.setattr(obs,"ollama_get_json",lambda url,**kw:metadata.append(url) or forbidden())
    monkeypatch.setattr(obs.ExistingWindowsEdgeAdapter,"health",forbidden)
    inventory._inventory_records.cache_clear()
    async def cycle():
        async with api._control_plane_lifespan(api.app):
            projection=api._semantic_capability_projection()
            entry=next(x for x in projection["entries"] if x["capability_id"]=="external_adapter:smolagents")
            assert entry["capability_exists"] is True
            assert entry["provider_available"] is False
            assert entry["executed"] is False and entry["execution_receipt_present"] is False
            assert entry["policy_metadata"]["turn_policy_execution_allowed"] is None
            assert api.BROWSER_PROVIDER_ADAPTER.health()["status"]=="UNAVAILABLE"
            assert obs.build_runtime_readiness_payload()["chat_model_ready"] is False
    try:asyncio.run(cycle())
    finally:inventory._inventory_records.cache_clear()
    assert attempted==[] and metadata==[]
    # HTTP claims have no authority to change the process launch policy.
    assert api._payload_text({"text":"audit","model_free":False})=="audit"
    assert run_context.model_free_startup() is True


@pytest.mark.parametrize("mode,allowed", [("0",True),("1",False)])
def test_browser_normal_probe_contract_and_model_free_skip(tmp_path,monkeypatch,mode,allowed):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import browser_provider_adapter as browser
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,mode)
    python=tmp_path/'python';python.touch();monkeypatch.setattr(browser,'BROWSER_PYTHON',python)
    calls=[]
    def fake(argv,**kw):calls.append((argv,kw));return SimpleNamespace(returncode=0)
    monkeypatch.setattr(browser.subprocess,'run',fake)
    result=browser.ExistingPlaywrightBrowserAdapter().health()
    assert (result['status']=='AVAILABLE') is allowed
    assert len(calls)==int(allowed)
    if allowed:assert calls[0][0]==[str(python),'-c',"import playwright; print('ok')"] and calls[0][1]['timeout']==5
    else:assert result['import_attempted'] is False


@pytest.mark.parametrize("defect", [None,'missing_package','wrong_runtime','same_binary_other_venv','contradictory_installed','wrong_package','missing_runtime','missing_attempt','missing_pass','missing_errors','untyped','partial','malformed'])
def test_normal_wire_requires_complete_matching_runtime(tmp_path,monkeypatch,defect):
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,'0')
    runtime=tmp_path/'python';runtime.touch();calls=[]
    payload={'installed':True,'import_probe_passed':True,'import_attempted':True,'package_name':'fixture','import_name':'fixture','runtime_python':str(runtime),'errors':[]}
    if defect=='missing_package':payload.update(installed=False,import_probe_passed=False,errors=['ModuleNotFoundError'])
    elif defect=='wrong_runtime':payload['runtime_python']='/wrong/python'
    elif defect=='same_binary_other_venv':
        other=tmp_path/'other-venv-python';other.symlink_to(runtime)
        payload['runtime_python']=str(other)
    elif defect=='contradictory_installed':payload['installed']=False
    elif defect=='wrong_package':payload['package_name']='wrong'
    elif defect and defect.startswith('missing_'):payload.pop({'missing_runtime':'runtime_python','missing_attempt':'import_attempted','missing_pass':'import_probe_passed','missing_errors':'errors'}[defect])
    elif defect=='untyped':payload['import_probe_passed']='true'
    elif defect=='partial':payload={'installed':True,'import_probe_passed':True}
    def fake(argv,**kw):
        calls.append((argv,kw));return SimpleNamespace(returncode=0,stdout='not-json' if defect=='malformed' else json.dumps(payload),stderr='')
    monkeypatch.setattr(probe.subprocess,'run',fake)
    result=probe._probe_import_with_runtime_python(str(runtime),'fixture','fixture')
    assert len(calls)==1 and calls[0][0][0]==str(runtime) and calls[0][1]['timeout']==60
    assert result.import_probe_passed is (defect is None)
    assert result.runtime_capability_verified is False


@pytest.mark.parametrize('mode',['0','1'])
def test_supervisor_passes_mode_to_existing_api_environment(monkeypatch,mode):
    from SUPERVISOR import process_supervisor as supervisor
    monkeypatch.setenv(run_context.MODEL_FREE_STARTUP_ENV,mode)
    assert supervisor.build_environment()[run_context.MODEL_FREE_STARTUP_ENV]==mode
    assert supervisor.build_command()[3]=='CONTROL_PLANE.api_server:app'


@pytest.mark.parametrize('mode',['0','1','invalid'])
def test_real_ctl_start_pins_mode_in_tmux_command_only_in_tmp(tmp_path,mode):
    root=Path(__file__).resolve().parents[2]
    text=(root/'tools/ctl').read_text();start=text[text.index('start() {'):text.index('\nstop() {')]
    reserve=text[text.index('reserve_lifecycle() {'):text.index('\nstart() {')]
    fixture_root=tmp_path/'MAKSIMAR_PLATFORM';fixture_root.mkdir()
    (fixture_root/'CORE_ROOT').symlink_to(root/'CORE_ROOT',target_is_directory=True)
    fake=tmp_path/'python';capture=tmp_path/'capture';flag=tmp_path/'started'
    fake.write_text('#!/bin/bash\nif [[ "$1" == - && $# == 1 ]]; then exec "$TEST_REAL_PYTHON" -B "$@"; fi\nif [[ "$1" == - ]]; then printf "%s\\n" "$4" > "$CAPTURE"; cat >/dev/null; touch "$STARTED"; fi\nexit 0\n');fake.chmod(0o755)
    script=tmp_path/'ctl_fixture.sh'
    setup = """#!/bin/bash
set -euo pipefail
ROOT="$FIXTURE_ROOT"
RUNTIME_DIR="$ROOT/RUNTIME"
RUNTIME_STATE_DIR="$RUNTIME_DIR/state"
LOG_FILE="$ROOT/runtime.log"
SESSION_NAME=maksimar
CANONICAL_PYTHON="$FIXTURE_PYTHON"
log() { :; }
runtime_truth() { return 1; }
process_exists() { [[ -f "$STARTED" ]]; }
session_exists() { return 1; }
write_pid_file() { :; }
remove_pid_file() { :; }
status() { :; }
sleep() { :; }
"""
    script.write_text(setup+reserve+start+'\nstart\n')
    env={**os.environ,'FIXTURE_ROOT':str(fixture_root),'HOME':str(tmp_path),'TEST_REAL_PYTHON':__import__('sys').executable,'FIXTURE_PYTHON':str(fake),'CAPTURE':str(capture),'STARTED':str(flag),'MAKSIMAR_MODEL_FREE_STARTUP':mode}
    env.pop('MAKSIMAR_STARTUP_FD',None)
    result=subprocess.run(['bash',str(script)],cwd=tmp_path,env=env,capture_output=True,text=True,timeout=8)
    if mode=='invalid':
        assert result.returncode==2 and not capture.exists()
    else:
        assert result.returncode==0,result.stdout+result.stderr
        command=capture.read_text()
        assert 'MAKSIMAR_MODEL_FREE_STARTUP='+mode+' ' in command
        assert '-m SUPERVISOR.process_supervisor' in command
