"""Canonical n8n lifecycle isolation and authoritative execution identity."""
import sqlite3
from types import SimpleNamespace
import pytest
from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter as owner

@pytest.fixture
def local_owner(tmp_path, monkeypatch):
    data=tmp_path/'.n8n'; data.mkdir()
    with sqlite3.connect(data/'database.sqlite') as db:
        db.execute('CREATE TABLE execution_entity (id INTEGER, status TEXT, workflowId TEXT)')
    monkeypatch.setattr(owner,'_CANONICAL_RUNTIME_ROOT',tmp_path)
    monkeypatch.setattr(owner,'_CANONICAL_DATA_ROOT',data)
    monkeypatch.setattr(owner,'_PROJECT_ROOT',tmp_path)
    # Lifecycle tests exercise an already policy-bound graph; retain all prior
    # ownership/quiescence/restore assertions beneath the new authorization gate.
    monkeypatch.setattr(owner,'_read_stored_workflow',lambda wid:{'id':wid,'nodes':[], 'connections':{},'settings':{}})
    return data

def test_foreign_listener_is_never_stopped(local_owner,monkeypatch):
    def foreign(): raise ValueError('n8n_listener_is_not_canonical_owner')
    monkeypatch.setattr(owner,'_canonical_server_pid',foreign)
    monkeypatch.setattr(owner.os,'kill',lambda *a:pytest.fail('must not stop foreign listener'))
    assert owner._run_cli_execute('workflow', expected_graph_hash=owner._stored_workflow_hash(owner._read_stored_workflow('workflow')))['error']=='n8n_listener_is_not_canonical_owner'

@pytest.mark.parametrize('active,pending',[(True,False),(False,True)])
def test_active_or_waiting_work_is_not_interrupted(local_owner,monkeypatch,active,pending):
    if pending:
        with sqlite3.connect(local_owner/'database.sqlite') as db: db.execute("INSERT INTO execution_entity VALUES (1,'waiting','workflow')")
    monkeypatch.setattr(owner,'_canonical_server_pid',lambda:42)
    monkeypatch.setattr(owner,'_n8n_request',lambda *a:{'data':[{'id':'active'}] if active else []})
    monkeypatch.setattr(owner.os,'kill',lambda *a:pytest.fail('must not interrupt existing work'))
    assert owner._run_cli_execute('workflow', expected_graph_hash=owner._stored_workflow_hash(owner._read_stored_workflow('workflow')))['error']=='n8n_active_work_requires_server_side_execution'

def test_server_is_restored_after_cli_failure(local_owner,monkeypatch):
    pids=iter((42,None)); stopped=[]; launches=[]
    monkeypatch.setattr(owner,'_canonical_server_pid',lambda:next(pids))
    monkeypatch.setattr(owner,'_n8n_request',lambda m,p:{'status':'ok'} if p=='/healthz' else {'data':[]})
    monkeypatch.setattr(owner.os,'kill',lambda *a:stopped.append(a))
    monkeypatch.setattr(owner,'_execute_cli_in_canonical_data_root',lambda w:{'returncode':1,'output':'failed'})
    monkeypatch.setattr(owner.subprocess,'Popen',lambda *a,**k:launches.append(a))
    result=owner._run_cli_execute('workflow', expected_graph_hash=owner._stored_workflow_hash(owner._read_stored_workflow('workflow')))
    assert result['returncode']==1 and result['canonical_server_restored'] is True
    assert len(stopped)==len(launches)==1

def test_graph_node_id_cannot_become_execution_id(local_owner,monkeypatch):
    def execute(*a,**k):
        with sqlite3.connect(local_owner/'database.sqlite') as db: db.execute("INSERT INTO execution_entity VALUES (37,'success','workflow')")
        return SimpleNamespace(returncode=0,stdout='{"id":"python","status":"success"}',stderr='')
    monkeypatch.setattr(owner.subprocess,'run',execute)
    result=owner._execute_cli_in_canonical_data_root('workflow')
    assert result['execution_id']=='37' and result['execution_status']=='success'

def test_running_existing_workflow_does_not_invent_an_artifact_dag():
    from CONTROL_PLANE.canonical_semantic_spine import _extract_artifact_operation_requirements
    goal={'goal_id':'g1','semantic_domain':'automation','effect_intent':'compute_run',
          'requested_outcome':'Run the existing workflow','grounding':'run existing workflow',
          'goal_role':'PRIMARY_OUTCOME','parent_goal_id':'','subgoal_justification_kind':'NONE'}
    def unexpected(**kwargs): pytest.fail('existing workflow execution must not decompose a new artifact')
    result=_extract_artifact_operation_requirements(understand=unexpected,deadline=None,
            original_text='run existing workflow',goals=[goal],execution_restriction_source='')
    assert result[0]['artifact_operation_requirements']==() and result[0]['effect_intent']=='compute_run'

def test_final_brain_keeps_actual_execution_output_and_excludes_raw_tail():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _bounded_observation
    value={'workflow_id':'wf','execution_id':'37','status':'success',
           'execution_result':{'readback_status':'COMPLETE','last_node':'Python','items':[{'numpy_total':60}]},
           'output_tail':'raw execution state with private resume token'}
    observed=_bounded_observation('n8n_execution',value)
    assert observed['execution_result']['items']==[{'numpy_total':60}]
    assert observed['execution_id']=='37' and 'output_tail' not in observed


@pytest.mark.parametrize('wrong',['image','mount','label'])
def test_docker_ownership_rejects_foreign_container(local_owner,monkeypatch,wrong):
    import json
    deployment={'container':'canonical','image':'sha256:accepted'}
    inspected={'Image':deployment['image'],'Config':{'Labels':{'maksimar.canonical-owner':owner.PROVIDER_ID}},
               'Mounts':[{'Source':str(local_owner),'Destination':'/home/node/.n8n'}],
               'State':{'Running':True}}
    if wrong=='image':inspected['Image']='sha256:foreign'
    if wrong=='mount':inspected['Mounts'][0]['Source']='/foreign-data'
    if wrong=='label':inspected['Config']['Labels']={}
    monkeypatch.setattr(owner,'_docker_deployment',lambda:deployment)
    monkeypatch.setattr(owner.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0,stdout=json.dumps([inspected])))
    with pytest.raises(ValueError,match='n8n_container_is_not_canonical_owner'):owner._canonical_container()


def test_docker_server_restored_after_cli_failure_without_native_signal(local_owner,monkeypatch):
    actions=[]
    monkeypatch.setattr(owner,'_canonical_container',lambda:{'name':'canonical','running':True})
    monkeypatch.setattr(owner,'_canonical_server_pid',lambda:pytest.fail('Docker PID must not be used as host PID'))
    monkeypatch.setattr(owner.os,'kill',lambda *a:pytest.fail('Docker handoff must not send native signals'))
    monkeypatch.setattr(owner,'_n8n_request',lambda m,p:{'status':'ok'} if p=='/healthz' else {'data':[]})
    monkeypatch.setattr(owner,'_execute_cli_in_canonical_data_root',lambda w:{'returncode':1})
    monkeypatch.setattr(owner.subprocess,'run',lambda cmd,**k:actions.append(cmd))
    result=owner._run_cli_execute('workflow', expected_graph_hash=owner._stored_workflow_hash(owner._read_stored_workflow('workflow')))
    assert result['returncode']==1 and result['canonical_server_restored'] is True
    assert actions==[['docker','stop','--time','20','canonical'],['docker','start','canonical']]
