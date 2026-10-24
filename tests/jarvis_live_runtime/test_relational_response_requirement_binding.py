from tests.ai_orchestration.test_model_admission_transport import acquisition
"""Canonical request-local subject binding; no live inference or storage writes."""
import copy
import json
import time
from pathlib import Path
import pytest
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as t
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    ResponseRequirement, validate_response_requirement_goal_references,
)

ROOT=Path(__file__).resolve().parents[2]
AUDIT=ROOT/'RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011'


def subject(relation='REVIEW_OF_SUBJECT_OR_EXPERIENCE', **extra):
    return dict(scope='SUBJECT',relation=relation,subject_goal_id='change',experience_id='exp_a',actor='ACTOR_A',**extra)


def record():
    return dict(experience_id='exp_a',actor='ACTOR_A',trace_id='trace_a',request_id='req_a',task_ref='task_a',
        source_ref='source_a',operation_id='modify_a',evidence_refs=['evidence_a'],
        review_status='PARTIAL_PENDING_INDEPENDENT_REVIEW',review_ref='',training_eligible=False,
        training_export_allowed=False,training_candidate_creation_allowed=False,learning_bundle_id='bundle_a',
        execution_receipts=[dict(receipt_id='receipt_a',operation_id='modify_a',step_id='step_a',
            trace_id='trace_a',request_id='req_a',status='COMPLETE',effect_type='MUTATE',experience_id='exp_a')])


def understanding(binding):
    return {'goals':[{'goal_id':'change'}], 'response_requirements':[dict(response_requirement_id='answer',
        applies_to_goal_ids=['change'],description='Explain the canonical recorded state',
        memory_query_kind='REVIEW_STATUS',subject_binding=binding)]}


def guard(binding=None, row=None, rows=None, document=False):
    row=record() if row is None else row
    groups=[{'evidence_kind':'mempalace_search','source_document':{'results':[row]}}] if document else [
        {'query_kind':'REVIEW_STATUS','matches':rows if rows is not None else [row]}]
    return t._history_requirement_relations(groups=groups,understanding=understanding(binding or subject()))


@pytest.mark.parametrize('relation,extra',[
 ('SOURCE_OF_SUBJECT',{}),('ACTOR_OF_SUBJECT',{}),
 ('OPERATION_OF_SUBJECT',{'operation_id':'modify_a'}),
 ('EFFECT_OF_OPERATION',{'operation_id':'modify_a','effect_type':'MUTATE','step_id':'step_a'}),
 ('RECEIPT_OF_EFFECT',{'operation_id':'modify_a','receipt_id':'receipt_a','step_id':'step_a','effect_type':'MUTATE'}),
 ('REVIEW_OF_SUBJECT_OR_EXPERIENCE',{}),
 ('LEARNING_QUALIFICATION_OF_EXPERIENCE',{'learning_bundle_id':'bundle_a'}),
])
def test_same_subject_actor_and_required_canonical_edge_pass(relation,extra):
    assert guard(subject(relation,**extra))['valid'] is True


@pytest.mark.parametrize('field,value',[('experience_id','other'),('actor','OTHER_ACTOR'),('source_ref','source_b'),('trace_id','trace_b'),('task_ref','other_task')])
def test_same_evidence_type_cannot_replace_subject_actor_source_or_task(field,value):
    b=subject();b[field]=value
    assert guard(b)['valid'] is False


@pytest.mark.parametrize('field,value',[('operation_id','search_a'),('receipt_id','receipt_b'),('step_id','step_b'),('effect_type','OBSERVE')])
def test_exact_receipt_operation_step_and_effect_are_not_fungible(field,value):
    b=subject('RECEIPT_OF_EFFECT',operation_id='modify_a',receipt_id='receipt_a',step_id='step_a',effect_type='MUTATE');b[field]=value
    assert guard(b)['valid'] is False


@pytest.mark.parametrize('relation,nested',[
 ('REVIEW_OF_SUBJECT_OR_EXPERIENCE','review'),
 ('LEARNING_QUALIFICATION_OF_EXPERIENCE','learning_bundle'),
 ('LEARNING_QUALIFICATION_OF_EXPERIENCE','qualification'),
])
def test_review_or_qualification_from_another_experience_is_rejected(relation,nested):
    row=record();row[nested]={'experience_id':'exp_other','reviewer_id':'real_reviewer','training_eligible':True}
    assert guard(subject(relation),row)['valid'] is False


@pytest.mark.parametrize('field,value',[('trace_id','other_trace'),('request_id','other_request'),('experience_id','other_experience'),('status','FAILED')])
def test_disconnected_nested_receipt_never_proves_subject_effect(field,value):
    row=record();row['execution_receipts'][0][field]=value
    assert guard(subject('RECEIPT_OF_EFFECT',operation_id='modify_a'),row)['valid'] is False


def test_source_retrieval_never_implies_modification_execution_review_or_qualification():
    row={'source_file':'document_a','text':'Design description','excerpt_only':True}
    for relation in ('ACTOR_OF_SUBJECT','OPERATION_OF_SUBJECT','RECEIPT_OF_EFFECT',
                     'REVIEW_OF_SUBJECT_OR_EXPERIENCE','LEARNING_QUALIFICATION_OF_EXPERIENCE'):
        b={'scope':'SUBJECT','relation':relation,'subject_goal_id':'change','source_ref':'document_a'}
        assert guard(b,row,document=True)['valid'] is False
    b={'scope':'SUBJECT','relation':'SOURCE_OF_SUBJECT','subject_goal_id':'change','source_ref':'document_a'}
    assert guard(b,row,document=True)['valid'] is True
    b['effect_type']='MUTATE';b['operation_id']='modify_a'
    assert guard(b,row,document=True)['valid'] is False


def test_unknown_reviewer_pending_review_and_false_learning_are_valid_canonical_states():
    row=record();assert 'reviewer_id' not in row and row['training_eligible'] is False
    assert guard(subject('REVIEW_OF_SUBJECT_OR_EXPERIENCE'),row)['valid'] is True
    assert guard(subject('LEARNING_QUALIFICATION_OF_EXPERIENCE'),row)['valid'] is True


def test_existential_scope_can_select_another_subject_without_global_any_match_substitution():
    row=record();other=record();other['experience_id']='exp_b';other['actor']='ACTOR_B';other['training_eligible']=True
    # An actual existential question may range across experience identities.
    b={'scope':'EXISTENTIAL','relation':'LEARNING_QUALIFICATION_OF_EXPERIENCE','subject_goal_id':'change'}
    result=guard(b,rows=[row,other]);assert result['valid'] is True
    assert result['requirements']['answer']['record_refs']==[[1,0],[1,1]]
    # A particular-subject question has no such cross-subject permission.
    assert guard(subject(),rows=[other])['valid'] is False


def test_actor_alone_with_multiple_subjects_fails_closed_and_goal_anchor_is_not_historical_identity():
    row=record();other=record();other['experience_id']='exp_b'
    b=subject();del b['experience_id'];assert guard(b,rows=[row,other])['valid'] is False
    del b['actor'];assert guard(b)['valid'] is False


def test_shared_subject_goal_reuses_identity_constraints_without_copying_evidence():
    q=understanding(subject());other=copy.deepcopy(q['response_requirements'][0]);other['response_requirement_id']='learning'
    other['subject_binding']={'scope':'SUBJECT','relation':'LEARNING_QUALIFICATION_OF_EXPERIENCE','subject_goal_id':'change'}
    q['response_requirements'].append(other)
    result=t._history_requirement_relations(groups=[{'matches':[record()]}],understanding=q)
    assert result['valid'] is True and result['requirements']['learning']['binding']['experience_id']=='exp_a'
    other['subject_binding']['experience_id']='exp_b'
    assert t._history_requirement_relations(groups=[{'matches':[record()]}],understanding=q)['valid'] is False


def test_existing_response_contract_roundtrip_is_typed_and_goal_owned():
    b=subject();q=ResponseRequirement('answer',('change',),memory_query_kind='REVIEW_STATUS',subject_binding=b)
    assert q.to_read_model()['subject_binding']==b
    b['actor']='MUTATED_CALLER';assert dict(q.subject_binding)['actor']=='ACTOR_A'
    validate_response_requirement_goal_references((q,),{'change'})
    with pytest.raises(ValueError):validate_response_requirement_goal_references((q,),{'another_goal'})
    for invalid in ({'scope':'GLOBAL'},dict(subject(),scope='ANY'),dict(subject(),invented_registry='parallel')):
        with pytest.raises(ValueError):ResponseRequirement('answer',('change',),subject_binding=invalid)


def install_offline_verifier(monkeypatch,verdict):
    monkeypatch.setattr(t,'ollama_get_json',lambda *a,**k:{'models':[{'name':t.DEFAULT_OLLAMA_MODEL_ID}]})
    monkeypatch.setattr(t,'_measured_final_brain_prompt_budget',lambda *a,**k:{'within_budget':True})
    calls=[]
    def post(*a,**k):
        calls.append(a)
        return {'model':t.DEFAULT_OLLAMA_MODEL_ID,'done':True,'done_reason':'stop','message':{'content':json.dumps(verdict)}}
    monkeypatch.setattr(t,'ollama_post_json',post);return calls


@pytest.mark.parametrize('witness,expected',[
 ([[2,1,0]],True),([],False),([[2,1,1]],False),([[2,99,0]],False),
 ([[2,1,0],[2,1,0]],False),([[True,1,0]],False),([[3,1,0]],False),
])
def test_scoped_source_witness_and_coverage_are_both_required(monkeypatch,witness,expected):
    calls=install_offline_verifier(monkeypatch,{'supported':[1,2],'contradictions':[],'unsupported_claims':[],'relations':witness})
    result=t._validate_history_publication(content='The reviewer is not established; independent review is pending.',
        inputs={'understanding':understanding(subject()),'evidence_bundle':{'items':[{'kind':'history_search',
            'observation':{'history_query':{'query_kind':'REVIEW_STATUS','matches':[record()]}}}]}},deadline_at=time.monotonic()+30)
    assert result['valid'] is expected and len(calls)==1
    assert result['correction_attempts']==0 and result['host_answer_synthesized'] is False


def saved_material():
    result=json.loads((AUDIT/'owner_20261016_exact_admission_cross_layer_response.json').read_text())['result']
    return result,result['final_brain_result']['content']


def test_exact_saved_bad_answer_and_evidence_fail_with_all_six_original_obligations(monkeypatch):
    result,candidate=saved_material()
    monkeypatch.setattr(t,'ollama_post_json',lambda *a,**k:pytest.fail('No actual/model-verdict call needed for unbound subject'))
    verdict=t._validate_history_publication(content=candidate,inputs={'understanding':result['understanding'],
        'evidence_bundle':result['evidence_bundle']},deadline_at=time.monotonic()+30)
    assert verdict['valid'] is False
    errors=verdict['relational_validation']['errors'];assert len(errors)==6
    assert all(e['code']=='response_subject_binding_missing_or_invalid' for e in errors)
    assert {'ACTOR_OF_SUBJECT','RECEIPT_OF_EFFECT','REVIEW_OF_SUBJECT_OR_EXPERIENCE',
            'LEARNING_QUALIFICATION_OF_EXPERIENCE'} <= set(errors[0]['unproven_relations'])
    # Original candidate/evidence remain unchanged, not patched into truth by host.
    again,raw=saved_material();assert candidate==raw and result==again


@pytest.mark.parametrize('mode',['sync','stream'])
def test_real_relational_guard_withholds_saved_bad_candidate_in_both_publication_modes(monkeypatch,mode, acquisition):
    result,candidate=saved_material();author={'model':acquisition['profile'].model_id,'done':True,'done_reason':'stop','message':{'content':candidate}}
    install_offline_verifier(monkeypatch,{})
    monkeypatch.setattr(t,'ollama_post_json',lambda *a,**k:dict(author))
    class Wire:
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def raise_for_status(self):pass
        def iter_lines(self):
            yield json.dumps({'model':acquisition['profile'].model_id,'message':{'content':candidate[:20]},'done':False})
            yield json.dumps({**author,'message':{'content':candidate[20:]}})
    monkeypatch.setattr(t.httpx,'stream',lambda *a,**k:Wire())
    args={'original_text':result['original_text'],'understanding':result['understanding'],
          'execution_plan':result['execution_plan'],'evidence_bundle':result['evidence_bundle'],'capability_state':()}
    if mode=='sync':
        final=t.grounded_final_brain_call(**args)
        assert final['ok'] is False and final['response_text']=='' and final['raw_response_text']==candidate
    else:
        events=list(t.grounded_final_brain_stream(**args));assert not any(e['event']=='chunk' for e in events)
        assert events[-1]['event']=='error' and events[-1]['raw_response_text']==candidate and events[-1]['response_text']==''


def test_candidate_or_correction_cannot_switch_to_other_subject(monkeypatch):
    row=record();row['experience_id']='exp_other'
    calls=install_offline_verifier(monkeypatch,{'supported':[1,2],'contradictions':[],'unsupported_claims':[],'relations':[[2,1,0]]})
    for candidate in ('First candidate','Corrected candidate with borrowed qualification'):
        final=t._validate_history_publication(content=candidate,inputs={'understanding':understanding(subject()),
            'evidence_bundle':{'items':[{'kind':'history_search','observation':{'history_query':{'query_kind':'REVIEW_STATUS','matches':[row]}}}]}},deadline_at=time.monotonic()+30)
        assert final['valid'] is False
    assert not calls

def test_actual_learning_bundle_artifact_actor_and_bundle_identity_must_join_same_experience():
    row=record();row['learning_bundle']={'artifact_type':'developer_experience','artifact_ref':'experience://exp_a',
        'bundle_id':'bundle_a','source_actor':'ACTOR_A'}
    assert guard(subject('LEARNING_QUALIFICATION_OF_EXPERIENCE'),row)['valid'] is True
    for field,value in (('artifact_ref','experience://exp_b'),('bundle_id','bundle_b'),('source_actor','ACTOR_B')):
        bad=copy.deepcopy(row);bad['learning_bundle'][field]=value
        assert guard(subject('LEARNING_QUALIFICATION_OF_EXPERIENCE'),bad)['valid'] is False


def test_response_binding_survives_existing_parser_without_becoming_helper_authority():
    from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import parse_request_understanding_payload
    result,_=saved_material();raw=copy.deepcopy(result['understanding'])
    for key in ('request_id','original_text','relevant_context_trace_ids'):raw.pop(key,None)
    for capability in raw['required_capabilities']:capability.pop('schema_version',None)
    b=subject();b['subject_goal_id']=raw['goals'][0]['goal_id']
    raw['response_requirements'][0]['subject_binding']=b
    parsed=parse_request_understanding_payload(raw,host_request_id='offline',host_original_text=result['original_text'])
    assert parsed.to_read_model()['response_requirements'][0]['subject_binding']==b


def test_native_goalframe_schema_and_validator_reuse_exact_response_binding_contract():
    import jsonschema
    from CONTROL_PLANE import canonical_semantic_spine as spine
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import response_subject_binding_schema
    schema=spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items']
    assert 'subject_binding' not in schema['properties']
    assert spine.REQUEST_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items']['properties']['subject_binding']==response_subject_binding_schema()
    legal=spine._goalframe_item_schema('PRIMARY_OUTCOME')['properties']['goal_id']['enum'][0]
    q={'applies_to_goal_ids':[legal],'description':'canonical purpose','memory_query_kind':'REVIEW_STATUS','requirement_kind':'REVIEW_STATUS',
       'subject_binding':dict(subject(),subject_goal_id=legal)}
    jsonschema.validate({k:v for k,v in q.items() if k!='subject_binding'},schema)
    assert spine._goalframe_response_requirement_violations([{'goal_id':legal,'memory_filter':dict(query_kind='REVIEW_STATUS',time_basis='ANY_TIME',time_start='',time_end='')}],(q,))==()
    q['subject_binding']['subject_goal_id']='absent_goal'
    assert spine._goalframe_response_requirement_violations([{'goal_id':legal,'memory_filter':dict(query_kind='REVIEW_STATUS',time_basis='ANY_TIME',time_start='',time_end='')}],(q,))


def test_truthful_reference_response_passes_all_bound_obligations_offline(monkeypatch):
    relations=('SOURCE_OF_SUBJECT','ACTOR_OF_SUBJECT','OPERATION_OF_SUBJECT','RECEIPT_OF_EFFECT',
               'REVIEW_OF_SUBJECT_OR_EXPERIENCE','LEARNING_QUALIFICATION_OF_EXPERIENCE')
    u={'goals':[{'goal_id':'change'}],'response_requirements':[]}
    for i,relation in enumerate(relations):
        extra={'operation_id':'modify_a'} if relation in {'OPERATION_OF_SUBJECT','RECEIPT_OF_EFFECT'} else {}
        q=understanding(subject(relation,**extra))['response_requirements'][0];q['response_requirement_id']='answer_'+str(i)
        u['response_requirements'].append(q)
    reference='ACTOR_A: source_a, task_a, modify_a, receipt_a. Independent reviewer unknown, review pending. training_eligible=false; export=false; candidate=false.'
    calls=install_offline_verifier(monkeypatch,{'supported':list(range(1,8)),'contradictions':[],
        'unsupported_claims':[],'relations':[[i,1,0] for i in range(2,8)]})
    proof=t._validate_history_publication(content=reference,inputs={'understanding':u,'evidence_bundle':{
        'items':[{'kind':'history_search','observation':{'history_query':{'query_kind':'REVIEW_STATUS','matches':[record()]}}}]}},deadline_at=time.monotonic()+30)
    assert proof['valid'] is True and len(calls)==1 and proof['correction_attempts']==0


@pytest.mark.parametrize('mode',['sync','stream'])
def test_subject_mismatch_with_valid_binding_withheld_by_actual_gate(monkeypatch,mode, acquisition):
    candidate='A claimed effect with a borrowed receipt.'
    author={'model':acquisition['profile'].model_id,'done':True,'done_reason':'stop','message':{'content':candidate}}
    monkeypatch.setattr(t,'_measured_final_brain_prompt_budget',lambda *a,**k:{'within_budget':True})
    monkeypatch.setattr(t,'ollama_post_json',lambda *a,**k:copy.deepcopy(author))
    class Wire:
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def raise_for_status(self):pass
        def iter_lines(self):yield json.dumps(author)
    monkeypatch.setattr(t.httpx,'stream',lambda *a,**k:Wire())
    row=record();row['actor']='OTHER_ACTOR'
    args={'original_text':'Show recorded effect','understanding':understanding(subject('RECEIPT_OF_EFFECT',operation_id='modify_a')),
        'execution_plan':{'steps':[{'capability_id':'runtime_history_store','operation':'search_history'}]},'capability_state':(),
        'evidence_bundle':{'items':[{'kind':'history_search','observation':{'history_query':{'query_kind':'REVIEW_STATUS','matches':[row]}}}]}}
    if mode=='sync':
        out=t.grounded_final_brain_call(**args);assert out['ok'] is False and out['response_text']=='' and out['raw_response_text']==candidate
    else:
        out=list(t.grounded_final_brain_stream(**args));assert not any(e['event']=='chunk' for e in out)
        assert out[-1]['event']=='error' and out[-1]['response_text']=='' and out[-1]['raw_response_text']==candidate


@pytest.mark.parametrize('scoped',[False,True])
def test_json_grammar_accounting_view_does_not_change_actual_verifier_request_or_selfknowledge_default(monkeypatch,scoped):
    payload={'model':t.DEFAULT_OLLAMA_MODEL_ID,'format':'json','think':False,'stream':False,
        'messages':[{'role':'system','content':'Verify'},{'role':'user','content':'Full original evidence'}],
        'options':{'num_ctx':4096,'num_predict':256}}
    original=copy.deepcopy(payload);views=[];actual=[]
    monkeypatch.setattr(t,'_measured_final_brain_prompt_budget',lambda p,**kw:views.append(copy.deepcopy(p)) or {'within_budget':True})
    verdict={'supported':[1,2],'contradictions':[],'unsupported_claims':[]}
    if scoped:verdict['relations']=[[2,1,0]]
    def post(path,p,**kw):
        actual.append(copy.deepcopy(p));return {'model':t.DEFAULT_OLLAMA_MODEL_ID,'done':True,'done_reason':'stop','message':{'content':json.dumps(verdict)}}
    monkeypatch.setattr(t,'ollama_post_json',post)
    result=t._verify_grounded_assertion_group(payload=payload,assertion_ids=[1,2],deadline_at=time.monotonic()+30,
        **({'relation_refs':{2:[[1,0]]}} if scoped else {}))
    assert result['valid'] is True and actual==[original] and payload==original
    assert views[0]['messages']==original['messages'] and views[0]['options']==original['options']
    assert ('format' in views[0]) is (not scoped)


def test_duplicate_requirement_ids_and_absent_receipt_identity_fail_closed():
    u=understanding(subject());u['response_requirements']*=2
    assert t._history_requirement_relations(groups=[{'matches':[record()]}],understanding=u)['valid'] is False
    row=record();del row['execution_receipts'][0]['receipt_id']
    assert guard(subject('RECEIPT_OF_EFFECT',operation_id='modify_a'),row)['valid'] is False


def test_no_review_record_for_identified_subject_allows_truthful_unknown_instead_of_fake_review():
    row=record()
    for key in ('review_status','review_ref','verification_status','verification_refs'):row.pop(key,None)
    assert guard(subject('REVIEW_OF_SUBJECT_OR_EXPERIENCE'),row)['valid'] is True


def test_question_about_unknown_operation_identity_can_read_actual_subject_receipts():
    # No invented operation ID in the request binding; source receipts supply it.
    assert guard(subject('OPERATION_OF_SUBJECT'))['valid'] is True
    row=record();row['execution_receipts']=[]
    assert guard(subject('OPERATION_OF_SUBJECT'),row)['valid'] is False


def test_file_specific_receipt_effect_requires_the_same_canonical_source_identity():
    binding=subject('RECEIPT_OF_EFFECT',source_ref='source_a',operation_id='modify_a')
    row=record();assert guard(binding,row)['valid'] is False  # file link unavailable
    row['execution_receipts'][0]['source_ref']='source_b';assert guard(binding,row)['valid'] is False
    row['execution_receipts'][0]['source_ref']='source_a';assert guard(binding,row)['valid'] is True


@pytest.fixture
def isolated_publication(acquisition, monkeypatch, tmp_path):
    # Existing HOST/session fixture owns isolation; acquisition owns admission facts.
    from tests.control_plane.test_jarvis_live_hot_endpoint_smoke import isolate_existing_hot_endpoint_state
    isolate_existing_hot_endpoint_state.__wrapped__(monkeypatch, tmp_path)
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "0")
    from CONTROL_PLANE import api_server as api
    monkeypatch.setattr(api, "_semantic_capability_projection", lambda: {
        "entries": [{"capability_id": "runtime_history_store", "kind": "memory_tool"}],
        "capability_count": 1,
    })
    monkeypatch.setattr(t, "_measured_final_brain_prompt_budget", lambda *a, **k: {"within_budget": True})
    return acquisition


@pytest.mark.parametrize("mode", ["sync", "stream"])
@pytest.mark.parametrize("outcome", ["rejected", "success"])
def test_final_brain_publication_privacy_at_actual_http_boundary(isolated_publication, monkeypatch, tmp_path, mode, outcome):
    import asyncio
    import uuid
    import httpx
    from CONTROL_PLANE import api_server as api, canonical_semantic_spine as spine
    from tests.control_plane.test_jarvis_live_hot_endpoint_smoke import canonical_result
    from MAKSIMAR_CORE_LIB.execution_control import admission_contract
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store
    candidate = "synthetic-author-" + uuid.uuid4().hex
    state = isolated_publication
    author = {"model": state["profile"].model_id, "done": True, "done_reason": "stop",
              "message": {"thinking": "private-thinking-sentinel", "content": candidate}}
    wires, admissions, validations, internal, snapshots, deadlines = [], [], [], [], [], []
    wire_deadlines = []
    real_evaluate = admission_contract.evaluate_model_admission
    def evaluate(**kwargs):
        decision = real_evaluate(**kwargs)
        admissions.append(decision.admitted)
        return decision
    monkeypatch.setattr(admission_contract, "evaluate_model_admission", evaluate)
    class Response:
        status_code = 200
        content = b"{}"
        def raise_for_status(self): pass
        def json(self): return copy.deepcopy(author)
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def iter_lines(self):
            yield json.dumps({**author, "done": False, "message": {"content": candidate[:10]}})
            yield json.dumps({**author, "message": {"content": candidate[10:]}})
    def wire(*args, **kwargs):
        from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline
        wire_deadlines.append(RequestDeadline.current())
        wires.append(True)
        return Response()
    monkeypatch.setattr(t.httpx, "post", wire)
    monkeypatch.setattr(t.httpx, "stream", wire)
    row = record(); row["actor"] = "OTHER_ACTOR"
    inputs = {"original_text": "Show recorded effect", "understanding": understanding(subject("RECEIPT_OF_EFFECT", operation_id="modify_a")),
        "execution_plan": {"steps": [{"capability_id": "runtime_history_store", "operation": "search_history"}]},
        "capability_state": (), "evidence_bundle": {"items": [{"kind": "history_search", "observation": {
            "history_query": {"query_kind": "REVIEW_STATUS", "matches": [row]}}}]}}
    if outcome == "success":
        inputs.update(understanding={}, execution_plan={}, evidence_bundle={})
    real_validate = t._validate_history_publication
    def validate(**kwargs):
        result = real_validate(**kwargs)
        validations.append((kwargs["content"], result["valid"]))
        return result
    monkeypatch.setattr(t, "_validate_history_publication", validate)
    def base_result():
        value = canonical_result(status="FINAL_BRAIN_UNAVAILABLE" if outcome == "rejected" else "COMPLETE")
        value.update(understanding=inputs["understanding"], execution_plan=inputs["execution_plan"],
            evidence_bundle=inputs["evidence_bundle"], response_text="", generation_completed=outcome == "success",
            delivery_completed=outcome == "success", response_execution_status="NOT_EXECUTED" if outcome == "rejected" else "COMPLETE")
        return value
    def synchronous(**kwargs):
        deadline = kwargs["request_deadline"]; deadlines.append(deadline)
        final = kwargs["final_brain_port"].answer(deadline=deadline, **inputs)
        value = base_result(); value["response_text"] = final["response_text"]
        value["final_brain_result"] = final
        value["trace"]["final_brain_result"] = final
        value["trace"]["diagnostic_metadata"] = {"nested": [final]}
        value["diagnostic_metadata"] = {"nested": [final]}
        internal.append(value); snapshots.append(copy.deepcopy(value))
        return value
    monkeypatch.setattr(api, "run_canonical_semantic_turn", synchronous)
    def pending(**kwargs):
        assert kwargs["defer_final_brain"] is True
        deadlines.append(kwargs["request_deadline"])
        value = base_result(); value.update(operation_status="FINAL_BRAIN_PENDING", final_brain_input=inputs)
        return value
    monkeypatch.setattr(spine, "run_canonical_semantic_turn", pending)
    real_stream = spine.stream_canonical_semantic_turn
    def streaming(**kwargs):
        for event in real_stream(**kwargs):
            if event["event"] == "error":
                # Diagnostic containers are private even when they contain extra aliases.
                event["correction_proof"] = {"nested": [{"raw_model_result": {"content": candidate}}]}
                event["diagnostic_metadata"] = {"author": candidate}
                event["error_message"] = candidate
                event["result"]["trace"]["final_brain_result"] = {"raw_response_text": candidate}
                event["result"]["raw_model_result"] = {"content": candidate}
                event["result"]["diagnostic_metadata"] = {"nested": [candidate]}
                internal.append(event); snapshots.append(copy.deepcopy(event))
            yield event
    monkeypatch.setattr(api, "stream_canonical_semantic_turn", streaming)
    # Real FastAPI route + response encoders + streaming ASGI writer; no sockets/lifespan.
    async def request():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=api.app), base_url="http://offline") as client:
            return await client.post("/jarvis-live/hot", json={"text": "offline publication fixture",
                "session_id": "privacy_" + mode, "stream": mode == "stream"})
    response = asyncio.run(request())
    assert response.status_code == 200
    assert admissions and all(admissions) and len(wires) == 1
    assert wire_deadlines == deadlines  # The same bounded request reaches provider I/O.
    assert "private-thinking-sentinel" not in response.text
    if mode == "stream":
        assert response.headers["content-type"].startswith("application/x-ndjson")
        lines = response.text.splitlines(); public = [json.loads(line) for line in lines]
        terminal = public[-1]; result = terminal["result"]
        assert deadlines[0].cancelled
    else:
        assert response.headers["content-type"].startswith("application/json")
        public = response.json(); result = public["result"]
    if outcome == "rejected":
        assert validations == [(candidate, False)]
        assert internal == snapshots  # Projection/capture never scrub the original diagnostics.
        diagnostic = internal[0] if mode == "stream" else internal[0]["final_brain_result"]
        assert diagnostic["raw_response_text"] == candidate
        assert candidate not in response.text
        # Visit every serialized value, including evidence/plan/session/learning/trace.
        remaining = [public]
        while remaining:
            value = remaining.pop()
            if isinstance(value, dict):
                remaining.extend(value.keys()); remaining.extend(value.values())
                assert "raw_response_text" not in value and "raw_model_result" not in value
                assert "final_brain_result" not in value
            elif isinstance(value, list): remaining.extend(value)
            elif isinstance(value, str): assert candidate not in value
        assert result["generation_completed"] is False
        assert result["response_execution_status"] == "NOT_EXECUTED"
        assert result["evidence_bundle"] == json.loads(json.dumps(inputs["evidence_bundle"]))
        assert result["execution_plan"] == json.loads(json.dumps(inputs["execution_plan"]))
        assert result["session_event"]["assistant_text"] == ""
        assert result["learning_bundle"] is None
        if mode == "stream":
            assert terminal["error_kind"] == "final_brain_history_factual_validation_failed"
            assert not any(event["event"] in {"chunk", "done"} for event in public)
            assert all(candidate not in line for line in lines)
        else:
            assert public["ok"] is False and result["ok"] is False
            assert public["executed"] is False
        assert result["trace"]["trace_id"]
    else:
        assert candidate in response.text
        if mode == "stream":
            assert terminal["event"] == "done"
            assert "".join(event["chunk"] for event in public if event["event"] == "chunk") == candidate
        else: assert public["ok"] is True
        assert result["response_text"] == candidate
        assert result["session_event"]["assistant_text"] == candidate
    log = tmp_path / "session_memory" / session_memory_store.SESSION_TURN_LOG_NAME
    rows = [json.loads(line) for line in log.read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["assistant_text"] == ("" if outcome == "rejected" else candidate)


@pytest.mark.parametrize("mode", ["sync", "stream"])
@pytest.mark.parametrize("denial", ["missing_demand", "stale", "missing_resources", "unknown_owner", "model_free", "stopgate"])
def test_pre_generation_denial_never_fabricates_author_output(isolated_publication, monkeypatch, mode, denial):
    from dataclasses import replace
    from CORE_ROOT import runtime_paths
    state = isolated_publication
    profile = state["profile"]
    observation = t._observe_model_resources(profile)
    if denial == "missing_demand":
        state["configured"][profile.role_id] = replace(profile, load_resource_demand=None)
    elif denial == "stale":
        state["next_observation"] = replace(observation, observed_monotonic=time.monotonic() - 30)
    elif denial == "missing_resources":
        state["next_observation"] = replace(observation, memory_available_bytes=(), accelerator_available_bytes=())
    elif denial == "unknown_owner":
        state["next_observation"] = replace(observation, ownership_verified=False)
    elif denial == "model_free":
        monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "1")
    else:
        runtime_paths.DEGRADED_MODE_FILE.write_text("synthetic StopGate denial")
    monkeypatch.setattr(t.httpx, "stream", lambda *a, **k: pytest.fail("denied generation reached stream HTTP"))
    inputs = dict(original_text="offline fixture", understanding={}, execution_plan={}, evidence_bundle={}, capability_state=())
    if mode == "sync":
        result = t.grounded_final_brain_call(**inputs)
        assert result["ok"] is False
    else:
        events = list(t.grounded_final_brain_stream(**inputs))
        assert not any(event["event"] in {"chunk", "done"} for event in events)
        result = events[-1]
        assert result["event"] == "error"
    assert not state["posts"]
    assert result["model_call_attempted"] is False
    assert result["raw_output_present"] is False
    assert not result.get("raw_response_text") and not result.get("response_text")
