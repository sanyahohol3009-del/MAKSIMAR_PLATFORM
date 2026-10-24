"""Typed task/context canonical linkage; offline, no language routing or inference."""
import copy,importlib.util,json
from pathlib import Path
import pytest
from CONTROL_PLANE import canonical_semantic_spine as spine
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
R=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('requested_subject_fixture',R/'tests/jarvis_live_runtime/test_requested_subject_grounding.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
TASK='repair fixture wiring'

def context(traces=('trace_a',)):
    return {'schema_version':'bounded_session_context.v2','session_id':'session_a',
            'bounded_chronological_turns':[{'trace_id':t,'topic':'bounded topic'} for t in traces]}

def row(**kw):
    return dict(f.f.record(),task_ref=TASK,session_id='session_a',**kw)

def run(rows,ctx=None,binding=None,reference=TASK,source=None,kind='PROVENANCE',relation='ACTOR_OF_SUBJECT'):
    b=binding if binding is not None else {'scope':'SUBJECT','relation':relation,'subject_goal_id':'g1','actor':'ACTOR_A','task_ref':TASK}
    u=f.understanding(binding=b,kind=kind,query='PROVENANCE',text=source or 'Explain '+reference)
    constraints={k:v for k,v in b.items() if k not in ('relation','subject_goal_id')}
    frames=({'goal_id':'g1','grounding':reference,'subject_constraints':constraints},)
    bound,proof=spine._ground_requested_memory_subjects(understanding=u,goalframes=frames,
        evidence=f.evidence(rows),source_text=u.original_text,session_context=ctx)
    return bound,proof

def test_unique_task_and_host_context_lineage_grounds_existing_binding():
    bound,proof=run([row()],context());assert bound and proof['valid']
    assert dict(bound.response_requirements[0].subject_binding)['experience_id']=='exp_a'
    assert proof['requirements']['answer']['resolution_basis']=='SOURCE_TASK_DESCRIPTOR_AND_CANONICAL_SESSION_LINEAGE'
    assert transport._history_requirement_relations(groups=[{'matches':[row()]}],understanding=bound.to_read_model())['valid']

@pytest.mark.parametrize('case',['no_rows','no_context','no_context_trace','wrong_session','wrong_actor','wrong_task','source_absent','no_experience','missing_trace','wrong_context_schema','actor_only'])
def test_no_independent_task_context_link_cannot_ground(case):
    rows=[row()];ctx=context();binding=None;reference=TASK;source=None
    if case=='no_rows':rows=[]
    if case=='no_context':ctx=None
    if case=='no_context_trace':ctx=context(('another_trace',))
    if case=='wrong_session':ctx['session_id']='another_session'
    if case=='wrong_actor':rows[0]['actor']='OTHER_ACTOR'
    if case=='wrong_task':rows[0]['task_ref']='another task'
    if case=='source_absent':source='Explain another task'
    if case=='no_experience':rows[0].pop('experience_id')
    if case=='missing_trace':rows[0].pop('trace_id')
    if case=='wrong_context_schema':ctx['schema_version']='model_proposal'
    if case=='actor_only':binding={'scope':'SUBJECT','relation':'ACTOR_OF_SUBJECT','subject_goal_id':'g1','actor':'ACTOR_A'};reference='ACTOR_A'
    bound,proof=run(rows,ctx,binding,reference,source)
    assert bound is None and not proof['valid']

@pytest.mark.parametrize('reverse',[False,True])
def test_all_plausible_context_candidates_are_considered_not_latest_or_top_rank(reverse):
    a=row();b=row(experience_id='exp_b',trace_id='trace_b')
    a['observed_at']='2020-01-01T00:00:00Z';b['observed_at']='2030-01-01T00:00:00Z';b['score']=999
    rows=[a,b];rows.reverse() if reverse else None
    bound,proof=run(rows,context(('trace_a','trace_b')))
    assert bound is None and proof['errors'][0]['code']=='requested_subject_ambiguous'
    assert proof['ambiguous_subject_autoselect_count']==0

@pytest.mark.parametrize('proposal',['exp_b','invented'])
def test_descriptive_request_cannot_authorize_model_proposed_primary_id(proposal):
    b={'scope':'SUBJECT','relation':'ACTOR_OF_SUBJECT','subject_goal_id':'g1','actor':'ACTOR_A','task_ref':TASK,'experience_id':proposal}
    assert run([row()],context(),binding=b)[0] is None


def test_failed_explicit_id_lookup_never_falls_back_to_contextual_other_experience():
    b={'scope':'SUBJECT','relation':'ACTOR_OF_SUBJECT','subject_goal_id':'g1','actor':'ACTOR_A','task_ref':TASK,'experience_id':'exp_missing'}
    assert run([row()],context(),binding=b,reference='exp_missing')[0] is None

@pytest.mark.parametrize('mutation,kind,relation',[
 ('source','EVIDENCE','SOURCE_OF_SUBJECT'),('receipt','EXECUTION','RECEIPT_OF_EFFECT'),
 ('review','REVIEW_STATUS','REVIEW_OF_SUBJECT_OR_EXPERIENCE'),
 ('qualification','LEARNING_QUALIFICATION','LEARNING_QUALIFICATION_OF_EXPERIENCE')])
def test_same_downstream_relations_still_reject_cross_experience_substitution(mutation,kind,relation):
    record=row();b={'scope':'SUBJECT','relation':relation,'subject_goal_id':'g1','actor':'ACTOR_A','task_ref':TASK}
    if mutation=='source':b['source_ref']='source_of_another_change'
    if mutation=='receipt':record['execution_receipts'][0]['experience_id']='exp_b'
    if mutation=='review':record['review']={'experience_id':'exp_b','reviewer':'wrong'}
    if mutation=='qualification':record['learning_bundle']={'experience_id':'exp_b'}
    bound,proof=run([record],context(),binding=b,kind=kind,relation=relation)
    assert bound and proof['valid']
    assert not transport._history_requirement_relations(groups=[{'matches':[record]}],understanding=bound.to_read_model())['valid']

@pytest.mark.parametrize('state',['UNKNOWN','PARTIAL_PENDING_INDEPENDENT_REVIEW'])
def test_truthful_non_positive_review_is_not_a_grounding_failure(state):
    record=row();record['review_status']=state
    assert run([record],context())[0] is not None


def test_existing_context_and_history_owners_produce_actual_controlled_canonical_linkage(tmp_path,monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store as store
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_retrieval_adapter import ExistingMemoryRetrievalAdapter
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext,ExecutionPlan,PlanStep
    monkeypatch.setattr(store,'SESSION_MEMORY_ROOT',tmp_path/'canonical_session')
    monkeypatch.setattr(store,'SESSION_STATE_PATH',tmp_path/'state.json')
    monkeypatch.setattr(store,'_EXCLUSION_CACHE',None)
    owner=store.CanonicalSessionContextStore();identity=IdentityContext('fixture_owner','local_terminal_session','owner',True,True)
    owner.append('session_a',identity,user_text='Explain '+TASK,assistant_text='Fixture diagnostic',topic=TASK,
        unresolved_reference='',trace_id='trace_a',artifact={'kind':'developer_experience','learning_experience':
        {'experience_id':'exp_a','actor':'CODEX','task_ref':TASK,'evidence_refs':['evidence_a'],'verification_status':'PENDING'}})
    ctx=owner.read('session_a',identity)
    b={'scope':'SUBJECT','relation':'ACTOR_OF_SUBJECT','subject_goal_id':'g1','actor':'CODEX','task_ref':TASK}
    u=f.understanding(binding=b,kind='PROVENANCE',query='PROVENANCE',text='Explain '+TASK)
    plan=ExecutionPlan(request_id=u.request_id,steps=(PlanStep(step_id='s1',goal_id='g1',capability_id='runtime_history_store',
        operation='search_history',required_evidence=('history_search',),effect_type='OBSERVE',target_scope='project',reversibility='REVERSIBLE',external_side_effect=False,risk_class='READ_ONLY',
        parameters=(('query',TASK),('memory_filter',json.dumps({'query_kind':'PROVENANCE','time_basis':'ANY_TIME','time_start':'','time_end':''})))),))
    evidence=ExistingMemoryRetrievalAdapter().collect_evidence(u,plan,'trace_fixture')
    assert evidence.status=='COMPLETE',evidence.errors
    bound,proof=spine._ground_requested_memory_subjects(understanding=u,goalframes=({'goal_id':'g1','grounding':TASK,'subject_constraints':{'scope':'SUBJECT','actor':'CODEX','task_ref':TASK}},),evidence=evidence,source_text=u.original_text,session_context=ctx)
    assert bound and proof['valid']
    canonical=json.loads(evidence.items[0].observation)['history_query']['matches'][0]
    assert canonical['experience_id']=='exp_a' and canonical['trace_id']==ctx['bounded_chronological_turns'][0]['trace_id']
    assert dict(bound.response_requirements[0].subject_binding)['experience_id']==canonical['experience_id']


def test_temporal_scope_is_existing_context_not_injected_latest():
    ctx=context(('trace_a','trace_b'));before=copy.deepcopy(ctx)
    a=row();b=row(experience_id='exp_b',trace_id='trace_b')
    bound,proof=run([a,b],ctx)
    assert bound is None and ctx==before and 'time_basis' not in proof
