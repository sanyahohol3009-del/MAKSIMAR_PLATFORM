from tests.ai_orchestration.test_model_admission_transport import acquisition
"""Typed answer-fact compatibility; isolated fixtures, never natural model calls."""
import copy
import importlib.util
import json
import time
from pathlib import Path
import pytest
import jsonschema
from CONTROL_PLANE import canonical_semantic_spine as spine
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import ResponseRequirement
from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import parse_request_understanding_payload
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as t
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011'
SAVED='owner_20261016_relational_one_natural_after_owner_docker_response.json'
# Explicit offline semantic annotation, NOT automatic reinterpretation of saved prose.
CASES=(('PROVENANCE','ACTOR_OF_SUBJECT'),('RATIONALE','SOURCE_OF_SUBJECT'),
       ('EXECUTION','RECEIPT_OF_EFFECT'),('EVIDENCE','SOURCE_OF_SUBJECT'),
       ('REVIEW_STATUS','REVIEW_OF_SUBJECT_OR_EXPERIENCE'),
       ('LEARNING_QUALIFICATION','LEARNING_QUALIFICATION_OF_EXPERIENCE'))

def fixture_module():
    spec=importlib.util.spec_from_file_location('existing_relational_fixture',ROOT/'tests/jarvis_live_runtime/test_relational_response_requirement_binding.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def binding(relation):
    return dict(scope='SUBJECT',relation=relation,subject_goal_id='g1',experience_id='exp_a',actor='ACTOR_A')

def requirement(kind,relation):
    return dict(response_requirement_id='answer',applies_to_goal_ids=['g1'],description='Recorded canonical fact',
                memory_query_kind='PROVENANCE',requirement_kind=kind,subject_binding=binding(relation))

def typed(q):
    return ResponseRequirement(**{**q, "applies_to_goal_ids": tuple(q["applies_to_goal_ids"])})

def saved_result():
    return json.loads((A/SAVED).read_text())['result']

def annotated_requirements():
    rows=copy.deepcopy(saved_result()['understanding']['response_requirements'])
    for row,(kind,relation) in zip(rows,CASES):
        row['requirement_kind']=kind
        anchor=row['subject_binding']['subject_goal_id']
        row['subject_binding']=dict(binding(relation),subject_goal_id=anchor)
    return rows

@pytest.mark.parametrize('kind,relation',CASES)
def test_fact_kind_roundtrip_and_native_schema_accepts_correct_family(kind,relation):
    q=requirement(kind,relation);model=ResponseRequirement(**{**q,'applies_to_goal_ids':tuple(q['applies_to_goal_ids'])})
    assert model.to_read_model()['requirement_kind']==kind
    assert model.to_read_model()['subject_binding']==q['subject_binding']
    item={k:v for k,v in q.items() if k not in ('response_requirement_id','subject_binding')}
    jsonschema.validate(item,spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items'])

@pytest.mark.parametrize('kind,relation',[
 ('REVIEW_STATUS','OPERATION_OF_SUBJECT'),('LEARNING_QUALIFICATION','OPERATION_OF_SUBJECT'),
 ('RATIONALE','EFFECT_OF_OPERATION'),('EXECUTION','REVIEW_OF_SUBJECT_OR_EXPERIENCE'),
 ('EVIDENCE','LEARNING_QUALIFICATION_OF_EXPERIENCE'),('PROVENANCE','OPERATION_OF_SUBJECT'),
 ('EXECUTION','UNKNOWN'),('invented_kind','SOURCE_OF_SUBJECT')])
def test_impossible_typed_pairs_reject_in_contract_and_native_schema(kind,relation):
    q=requirement(kind,relation)
    with pytest.raises(ValueError):typed(q)
    item={k:v for k,v in q.items() if k!='response_requirement_id'}
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(item,spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items'])


def test_native_schema_and_goalframe_reject_untyped_saved_collapse_before_author():
    raw=saved_result();assert len(raw['understanding']['response_requirements'])==6
    rows=raw['candidate_discovery']['response_requirements']
    assert {q['subject_binding']['relation'] for q in rows}=={'OPERATION_OF_SUBJECT'}
    schema=spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items']
    for row in rows:
        with pytest.raises(jsonschema.ValidationError):jsonschema.validate(row,schema)
    assert spine._goalframe_response_requirement_violations(raw['understanding']['goals'],tuple(rows))


def test_actor_is_required_only_by_actor_relation_not_review_learning_or_source():
    q=requirement('PROVENANCE','ACTOR_OF_SUBJECT');q['subject_binding'].pop('actor')
    with pytest.raises(ValueError,match='actor_identity_required'):typed(q)
    for kind,relation in CASES[1:]:
        q=requirement(kind,relation);q['subject_binding'].pop('actor')
        assert typed(q).to_read_model()['subject_binding']['experience_id']=='exp_a'


def test_same_subject_six_fact_roles_survive_existing_parser_and_projection():
    raw=copy.deepcopy(saved_result()['understanding'])
    for k in ('request_id','original_text','relevant_context_trace_ids'):raw.pop(k,None)
    for c in raw['required_capabilities']:c.pop('schema_version',None)
    raw['response_requirements']=annotated_requirements()
    parsed=parse_request_understanding_payload(json.loads(json.dumps(raw)),host_request_id='isolated',host_original_text='fixture').to_read_model()
    assert json.loads(json.dumps(parsed['response_requirements']))==raw['response_requirements']
    plan={'steps':[{'capability_id':'runtime_history_store','operation':'search_history'}]}
    projected=t._bounded_final_brain_inputs(understanding=parsed,execution_plan=plan,evidence_bundle={'items':[]},capability_state=(),session_context=None)[0]
    assert projected['response_requirements']==parsed['response_requirements']
    assert len({q['subject_binding']['experience_id'] for q in projected['response_requirements']})==1
    assert len({q['subject_binding']['relation'] for q in projected['response_requirements']})==5


def test_corrected_typed_pair_cannot_be_overwritten_by_hydration(monkeypatch):
    # Inventory projection is read-only here; never import-probe external runtimes.
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "1")
    spec=importlib.util.spec_from_file_location('projection_fixture',ROOT/'tests/control_plane/test_phase_1b_full_capability_world_correction.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    projection=m.select_semantic_projection_details(m.projection(),('runtime_history_store',))
    projection['selection_goalframes']=tuple(dict(goal_id=g['goal_id'],requested_outcome=g['description'],semantic_domain='memory',effect_intent='retrieve',memory_filter=dict(query_kind='PROVENANCE',time_basis='ANY_TIME',time_start='',time_end='')) for g in saved_result()['understanding']['goals'])
    projection['selection_response_requirements']=[{k:v for k,v in row.items() if k not in ('schema_version','response_requirement_id')} for row in annotated_requirements()]
    before=copy.deepcopy(projection['selection_response_requirements'])
    hydrated=spine._hydrate_host_owned_understanding_fields({'operation_requirements':{},'response_requirements':[]},projection)
    assert [q['requirement_kind'] for q in hydrated['response_requirements']]==[k for k,_ in CASES]
    assert [q['subject_binding'] for q in hydrated['response_requirements']]==[q['subject_binding'] for q in before]
    assert projection['selection_response_requirements']==before


def test_rationale_unknown_review_pending_and_false_learning_pass_controlled_verifier(monkeypatch):
    m=fixture_module();u=copy.deepcopy(saved_result()['understanding']);u['response_requirements']=annotated_requirements()
    row=m.record()  # SYNTHETIC isolated valid receipt; never inserted into saved/live evidence.
    assert 'rationale' not in row and 'reason' not in row
    verdict={'supported':list(range(1,8)),'contradictions':[],'unsupported_claims':[],'relations':[[i,1,0] for i in range(2,8)]}
    calls=m.install_offline_verifier(monkeypatch,verdict)
    text='Recorded actor ACTOR_A, source_a, modify_a, receipt_a. Rationale not established. Independent reviewer unknown; review pending. training_eligible=false; export=false; candidate=false.'
    out=t._validate_history_publication(content=text,inputs={'understanding':u,'evidence_bundle':{'items':[{'kind':'history_search','observation':{'history_query':{'query_kind':'PROVENANCE','matches':[row]}}}]}},deadline_at=time.monotonic()+30)
    assert out['valid'] and len(calls)==1
    payload=json.loads(calls[0][1]['messages'][1]['content'])
    assert payload['source_assertions']['3']['response_requirement']['requirement_kind']=='RATIONALE'


def test_typed_requirement_requires_a_known_bound_relation_and_wrong_subject_stays_rejected():
    q=requirement('REVIEW_STATUS','REVIEW_OF_SUBJECT_OR_EXPERIENCE');q['subject_binding']=None
    with pytest.raises(ValueError):typed(q)
    m=fixture_module();row=m.record();row['experience_id']='other_subject'
    q=requirement('REVIEW_STATUS','REVIEW_OF_SUBJECT_OR_EXPERIENCE')
    assert not t._history_requirement_relations(groups=[{'matches':[row]}],understanding={'goals':[{'goal_id':'g1'}],'response_requirements':[q]})['valid']

@pytest.mark.parametrize('mode',['sync','stream'])
def test_both_publication_modes_receive_identical_typed_requirements(monkeypatch,mode, acquisition):
    u=copy.deepcopy(saved_result()['understanding']);u['response_requirements']=annotated_requirements();expected=copy.deepcopy(u['response_requirements']);seen=[]
    monkeypatch.setattr(t,'_measured_final_brain_prompt_budget',lambda *a,**k:{'within_budget':True})
    def validate(*,content,inputs,deadline_at):
        seen.append(copy.deepcopy(inputs['understanding']['response_requirements']));return {'valid':False,'reason':'controlled_rejection'}
    monkeypatch.setattr(t,'_validate_history_publication',validate)
    author={'model':acquisition['profile'].model_id,'done':True,'done_reason':'stop','message':{'content':'Controlled candidate'}}
    monkeypatch.setattr(t,'ollama_post_json',lambda *a,**kw:copy.deepcopy(author))
    class Wire:
        def __enter__(self):return self
        def __exit__(self,*a):return False
        def raise_for_status(self):pass
        def iter_lines(self):yield json.dumps(author)
    monkeypatch.setattr(t.httpx,'stream',lambda *a,**kw:Wire())
    kwargs={'original_text':'fixture','understanding':u,'execution_plan':{'steps':[{'capability_id':'runtime_history_store','operation':'search_history'}]},'evidence_bundle':{'items':[]},'capability_state':()}
    if mode=='sync':assert not t.grounded_final_brain_call(**kwargs)['ok']
    else:assert list(t.grounded_final_brain_stream(**kwargs))[-1]['event']=='error'
    assert seen==[expected] and u['response_requirements']==expected

def test_existing_one_correction_preserves_same_six_typed_requirements(monkeypatch):
    spec=importlib.util.spec_from_file_location('existing_memory_fixture',ROOT/'tests/jarvis_live_runtime/test_memory_retrieval_capabilities_visible.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    inputs,paragraphs=m._factual_publication_fixture()
    inputs['understanding']=copy.deepcopy(saved_result()['understanding']);inputs['understanding']['response_requirements']=annotated_requirements()
    inputs['execution_plan']['steps']=list(inputs['execution_plan'].get('steps',()))+[{'capability_id':'runtime_history_store','operation':'search_history'}]
    correct=m._factual_coverage_content(inputs,paragraphs)
    payload=t._grounded_final_brain_payload(original_text='isolated fixture',**inputs,stream=False)
    seen=[];wire=[]
    def validation(*,content,inputs,deadline_seconds):
        seen.append(copy.deepcopy(inputs['understanding']['response_requirements']))
        return {'valid':len(seen)==2,'reason':'required_exact_facts_missing' if len(seen)==1 else 'valid','missing_exact_assertions':[]}
    monkeypatch.setattr(t,'_validate_memory_self_knowledge_publication',validation)
    monkeypatch.setattr(t,'_measured_final_brain_prompt_budget',lambda *a,**kw:{'within_budget':True})
    def post(url,p,**kw):
        wire.append(copy.deepcopy(p));return {'model':t.DEFAULT_OLLAMA_MODEL_ID,'done':True,'done_reason':'stop','message':{'content':correct}}
    monkeypatch.setattr(t,'ollama_post_json',post)
    result=t._validated_memory_answer_once(content=correct,inputs=inputs,payload=payload,deadline_at=time.monotonic()+30)
    assert result['valid'] and result['proof']['correction_attempts']==1 and len(wire)==1
    assert seen==[inputs['understanding']['response_requirements']]*2
    assert wire[0]['messages'][:-1]==payload['messages'][:-1]
    assert inputs['understanding']['response_requirements']==annotated_requirements()


def test_native_compatibility_alternatives_preserve_full_identity_grammar():
    item=spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items']
    for branch in item['oneOf']:
        assert branch['type']=='object' and branch['additionalProperties'] is False
        assert {'applies_to_goal_ids','description','memory_query_kind','requirement_kind'}<=set(branch['required'])
        assert 'subject_binding' not in branch['properties']
        assert 'const' in branch['properties']['requirement_kind']
    internal=spine.REQUEST_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items']
    subject=internal['properties']['subject_binding']
    assert {'scope','relation','subject_goal_id'}<=set(subject['required'])
    assert 'experience_id' in subject['properties'] and 'actor' in subject['properties']
