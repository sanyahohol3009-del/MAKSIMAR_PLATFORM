from fastapi.testclient import TestClient
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PermissionDecision
from MAKSIMAR_CORE_LIB.security_layer.host_principal import HostPrincipal, issue_host_token
from MAKSIMAR_CORE_LIB.security_layer.host_approval_handshake import HostApprovalStore
from MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model import model_runtime_projection
from MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model import local_host_projection

def test_local_host_uses_existing_snapshot_fields_and_reports_failure(monkeypatch,tmp_path):
    from types import SimpleNamespace
    import time
    import CONTROL_PLANE.health.monitor as monitor
    monkeypatch.setattr(monitor,'take_snapshot',lambda root:SimpleNamespace(ts=time.time(),uptime_s=42,
        cpu_count=8,loadavg=(1,2,3),mem_total=1024,mem_used=128,disk_total=4096,disk_free=2048))
    result=local_host_projection(tmp_path)
    assert result['fields']['root_filesystem_free_bytes']['value']==2048
    assert result['fields']['root_filesystem_free_bytes']['status']=='LIVE'
    assert 'not Windows desktop' in result['scope']
    def fail(root): raise OSError('unavailable')
    monkeypatch.setattr(monitor,'take_snapshot',fail)
    assert local_host_projection(tmp_path)['state']['status']=='NO_DATA'

def test_model_observation_never_promotes_unavailable_or_drifted(monkeypatch):
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport as transport
    monkeypatch.setattr(transport, 'ollama_get_json', lambda *a, **kw: {})
    assert model_runtime_projection()['state']['status']=='SERVICE_OFFLINE'
    monkeypatch.setattr(transport, 'ollama_get_json', lambda *a, **kw: {'models':[
        {'name':'jarvis-live:qwen14b','details':{'family':'qwen2'},'secret':'NEVER_COPY'}]})
    result=model_runtime_projection()
    heavy=next(role for role in result['roles'] if role['role_id']=='heavy_reasoning_model')
    assert heavy['runtime']['status']=='DEGRADED'
    assert 'NEVER_COPY' not in str(result)
    monkeypatch.setattr(transport, 'ollama_get_json', lambda *a, **kw: {'models':[
        {'name':'jarvis-live:qwen14b','details':{'family':'qwen2','parent_model':'qwen2.5-coder:3b'}},
        {'name':'qwen2.5-coder:14b','details':{'family':'qwen2'}}]})
    assert next(role for role in model_runtime_projection()['roles'] if role['role_id']=='heavy_reasoning_model')['runtime']['status']=='DEGRADED'

def test_protected_http_approval_projection_and_exact_step_decision(monkeypatch):
    import CONTROL_PLANE.api_server as api
    import MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model as projection
    monkeypatch.setenv('JARVIS_HOST_AUTH_SECRET','unit-test-only-secret')
    monkeypatch.setattr(projection,'model_runtime_projection',lambda:{'state':{'status':'SERVICE_OFFLINE'},'roles':[]})
    store=HostApprovalStore();monkeypatch.setattr(api,'CANONICAL_HOST_APPROVAL_STORE',store)
    decision=PermissionDecision(granted=False,capability_id='sample',identity_source='host',
        policy_version='semantic_policy.v1',denial_reason='approval_required',trace_id='trace',
        operation_id='op',approval_required=True,step_id='exact_step')
    resumed=[]
    pending=store.create(request_id='test',session_id='a',decision=decision,
        plan_step={'step_id':'exact_step','parameters':{'private':'DO_NOT_LEAK'}},description='bounded test',
        resume=lambda decision: resumed.append(decision.step_id) or {'trace_id':'trace','step_id':decision.step_id,'receipt':'unit-test'})
    token=issue_host_token(HostPrincipal('owner','a'))
    token_b=issue_host_token(HostPrincipal('owner','b'))
    headers={'Authorization':'Bearer '+token,'X-Jarvis-Session':'a'}
    client=TestClient(api.app)
    assert client.get('/operator-shell/read-model').status_code==401
    assert client.get('/operator-shell/events').status_code==401
    assert client.get('/operator-shell/approvals/'+pending.approval_id).status_code==401
    response=client.get('/operator-shell/read-model',headers=headers)
    assert response.status_code==200 and response.json()['approvals']['pending_count']==1
    assert 'DO_NOT_LEAK' not in response.text
    assert client.get('/operator-shell/approvals/'+pending.approval_id,
        headers={'Authorization':'Bearer '+token_b,'X-Jarvis-Session':'b'}).status_code==404
    path='/jarvis-live/approvals/'+pending.approval_id
    assert client.post(path,json={'decision':'approve','session_id':'a'}).json()['status']=='UNAUTHORIZED'
    assert client.post(path,json={'decision':'approve','session_id':'b','host_auth_token':token}).json()['status']=='DENIED'
    payload={'decision':'approve','session_id':'a','host_auth_token':token}
    approved=client.post(path,json=payload).json()
    assert approved['status']=='CONSUMED' and approved['resumed']['step_id']=='exact_step'
    assert resumed==['exact_step']
    assert client.post(path,json=payload).json()['status']=='DENIED'
    assert client.get('/operator-shell/read-model',headers=headers).json()['approvals']['pending_count']==0


def test_approved_execution_uses_canonical_durable_capture_once(monkeypatch, tmp_path):
    import json
    import CONTROL_PLANE.api_server as api
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store as memory
    monkeypatch.setenv('JARVIS_HOST_AUTH_SECRET', 'unit-test-only-secret')
    monkeypatch.setattr(memory, 'SESSION_MEMORY_ROOT', tmp_path)
    monkeypatch.setattr(api, 'CANONICAL_SESSION_CONTEXT', memory.CanonicalSessionContextStore())
    store = HostApprovalStore()
    monkeypatch.setattr(api, 'CANONICAL_HOST_APPROVAL_STORE', store)
    decision = PermissionDecision(granted=False, capability_id='sample', identity_source='host',
        policy_version='semantic_policy.v1', denial_reason='approval_required', trace_id='source_trace',
        operation_id='op', approval_required=True, step_id='exact_step')
    receipt = {'schema_version': 'execution_receipt.v1', 'receipt_id': 'receipt_one',
        'request_id': 'request_one', 'trace_id': 'source_trace', 'step_id': 'exact_step',
        'capability_id': 'sample', 'operation_id': 'op', 'provider_id': 'existing_provider',
        'status': 'COMPLETE', 'result': {'verified': True}}
    evidence = {'status': 'COMPLETE', 'items': [dict(receipt, kind='test_evidence')],
                'receipts': [receipt]}
    pending = store.create(request_id='request_one', session_id='a', decision=decision,
        plan_step={'step_id': 'exact_step'}, description='existing bounded request',
        resume=lambda _: {'status': 'COMPLETE', 'input_text': 'original model-understood request',
            'evidence_bundle': evidence, 'execution_plan': {'request_id': 'request_one',
                'steps': [{'step_id': 'exact_step'}]}})
    token = issue_host_token(HostPrincipal('owner', 'a'))
    payload = {'decision': 'approve', 'session_id': 'a', 'host_auth_token': token,
               'text': 'UNTRUSTED replacement task', 'trace_id': 'UNTRUSTED trace'}
    client = TestClient(api.app)
    path = '/jarvis-live/approvals/' + pending.approval_id
    result = client.post(path, json=payload).json()
    assert result['status'] == 'CONSUMED'
    assert result['memory_capture']['session_event']['persistence_status'] == 'PERSISTED'
    rows = [json.loads(line) for line in (tmp_path / memory.SESSION_TURN_LOG_NAME).read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]['identity_id'] == 'owner' and rows[0]['session_id'] == 'a'
    assert rows[0]['trace_id'] == 'source_trace'
    assert rows[0]['user_text'] == 'original model-understood request'
    assert rows[0]['assistant_text'] == ''
    assert rows[0]['artifact']['execution_receipts'] == [receipt]
    assert client.post(path, json=payload).json()['status'] == 'DENIED'
    assert len((tmp_path / memory.SESSION_TURN_LOG_NAME).read_text().splitlines()) == 1


def test_denied_approval_does_not_capture_unexecuted_receipt(monkeypatch, tmp_path):
    import CONTROL_PLANE.api_server as api
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store as memory
    monkeypatch.setenv('JARVIS_HOST_AUTH_SECRET', 'unit-test-only-secret')
    monkeypatch.setattr(memory, 'SESSION_MEMORY_ROOT', tmp_path)
    monkeypatch.setattr(api, 'CANONICAL_SESSION_CONTEXT', memory.CanonicalSessionContextStore())
    store = HostApprovalStore()
    monkeypatch.setattr(api, 'CANONICAL_HOST_APPROVAL_STORE', store)
    decision = PermissionDecision(granted=False, capability_id='sample', identity_source='host',
        policy_version='semantic_policy.v1', denial_reason='approval_required', trace_id='source_trace',
        operation_id='op', approval_required=True, step_id='exact_step')
    def must_not_resume(_):
        raise AssertionError('denied execution must not run')
    pending = store.create(request_id='request_one', session_id='a', decision=decision,
        plan_step={'step_id': 'exact_step'}, description='existing bounded request', resume=must_not_resume)
    token = issue_host_token(HostPrincipal('owner', 'a'))
    result = TestClient(api.app).post('/jarvis-live/approvals/' + pending.approval_id,
        json={'decision': 'deny', 'session_id': 'a', 'host_auth_token': token}).json()
    assert result['status'] == 'DENIED' and result['resumed'] is None
    assert not (tmp_path / memory.SESSION_TURN_LOG_NAME).exists()
