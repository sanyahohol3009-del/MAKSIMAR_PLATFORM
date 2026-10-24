"""Canonical source-reference grounding; controlled records, no live inference."""
import copy,json,hashlib,importlib.util
from pathlib import Path
from dataclasses import replace
import pytest
from CONTROL_PLANE import canonical_semantic_spine as spine
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import ResponseRequirement,EvidenceBundle,EvidenceItem
from MAKSIMAR_CORE_LIB.ai_orchestration.helper_model_decision_parser import parse_request_understanding_payload
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as t
R=Path(__file__).resolve().parents[2];A=R/'RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011'
spec=importlib.util.spec_from_file_location('existing_record_fixture',R/'tests/jarvis_live_runtime/test_relational_response_requirement_binding.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)


def understanding(binding=None,kind='REVIEW_STATUS',query='REVIEW_STATUS',text='Inspect exp_a'):
    raw=copy.deepcopy(json.loads((A/'owner_20261016_relational_one_natural_after_owner_docker_response.json').read_text())['result']['understanding'])
    for k in ('request_id','original_text','relevant_context_trace_ids'):raw.pop(k,None)
    for cap in raw['required_capabilities']:cap.pop('schema_version',None)
    b=dict(f.subject(),subject_goal_id='g1') if binding is None else binding
    q=ResponseRequirement(response_requirement_id='answer',applies_to_goal_ids=('g1',),description='Declared requested fact',memory_query_kind=query,requirement_kind=kind,subject_binding=tuple(b.items()))
    raw['response_requirements']=[q.to_read_model()]
    return parse_request_understanding_payload(raw,host_request_id='request_fixture',host_original_text=text)


def evidence(rows,document=False,truncated=False):
    obs=({'retrieval':{'results':rows}} if document else {'history_query':{'query_kind':'REVIEW_STATUS','matches':rows}})
    wire=json.dumps(obs)
    item=EvidenceItem(kind='mempalace_search' if document else 'history_search',source='existing_provider',observation=wire,scope='project',confidence=1.0,trace_id='trace_fixture',observed_at='2026-10-17T00:00:00Z',content_hash='sha256:'+hashlib.sha256(wire.encode()).hexdigest(),request_id='request_fixture',step_id='s1',capability_id='mempalace_search' if document else 'runtime_history_store',operation_id='search_mempalace' if document else 'search_history',provider_id='memory.retrieve',truncated=truncated)
    return EvidenceBundle(request_id='request_fixture',capability_id=item.capability_id,trace_id='trace_fixture',status='COMPLETE',items=(item,),limitations=(),receipts=(),errors=())


def ground(u,rows,reference='exp_a',document=False,truncated=False,scope='SUBJECT'):
    frames=({'goal_id':'g1','grounding':reference,'subject_constraints':{'scope':scope}},)
    return spine._ground_requested_memory_subjects(understanding=u,goalframes=frames,evidence=evidence(rows,document,truncated),source_text=u.original_text)


def test_explicit_requested_identity_precedes_existing_relation_join():
    u=understanding();row=f.record();before=copy.deepcopy(row)
    bound,proof=ground(u,[row]);assert bound and proof['valid']
    assert dict(bound.response_requirements[0].subject_binding)['experience_id']=='exp_a'
    assert t._history_requirement_relations(groups=[{'matches':[row]}],understanding=bound.to_read_model())['valid']
    assert row==before


@pytest.mark.parametrize('proposal',['exp_b','nonexistent'])
def test_real_or_nonexistent_proposed_experience_cannot_replace_requested_experience(proposal):
    b=dict(f.subject(),subject_goal_id='g1',experience_id=proposal);u=understanding(binding=b)
    other=f.record();other['experience_id']='exp_b';other['trace_id']='trace_b'
    bound,proof=ground(u,[f.record(),other]);assert bound is None and not proof['valid']
    assert proof['errors'][0]['code']=='model_subject_proposal_conflicts_with_requested_record'


@pytest.mark.parametrize('case',['no_candidate','actor_only','source_only','receipt_only','unlinked_existing','truncated','source_absent'])
def test_existing_identity_or_related_artifact_is_not_requested_subject_grounding(case):
    row=f.record();ref='exp_a';text='Inspect exp_a';truncated=False
    if case=='no_candidate':rows=[]
    else:rows=[row]
    if case=='actor_only':ref='ACTOR_A';text='Inspect ACTOR_A'
    if case=='source_only':ref='source_a';text='Inspect source_a'
    if case=='receipt_only':ref='receipt_a';text='Inspect receipt_a'
    if case=='unlinked_existing':row['experience_id']='exp_b';row['trace_id']='trace_b'
    if case=='truncated':truncated=True
    if case=='source_absent':text='Inspect an unspecified change'
    bound,proof=ground(understanding(text=text),rows,reference=ref,truncated=truncated)
    assert bound is None and not proof['valid'] and proof['ambiguous_subject_autoselect_count']==0


def test_two_experiences_sharing_requested_trace_are_ambiguous():
    a=f.record();b=copy.deepcopy(a);b['experience_id']='exp_b'
    u=understanding(text='Inspect trace_a');bound,proof=ground(u,[a,b],reference='trace_a')
    assert bound is None and proof['errors'][0]['code']=='requested_subject_ambiguous'


@pytest.mark.parametrize('relation,kind,mutate',[
 ('ACTOR_OF_SUBJECT','PROVENANCE','actor'),('SOURCE_OF_SUBJECT','EVIDENCE','source_ref'),
 ('RECEIPT_OF_EFFECT','EXECUTION','receipt'),('REVIEW_OF_SUBJECT_OR_EXPERIENCE','REVIEW_STATUS','review'),
 ('LEARNING_QUALIFICATION_OF_EXPERIENCE','LEARNING_QUALIFICATION','learning')])
def test_canonical_grounding_keeps_same_downstream_cross_subject_join_rejections(relation,kind,mutate):
    row=f.record();binding=dict(f.subject(relation),subject_goal_id='g1')
    if mutate=='actor':binding['actor']='OTHER_ACTOR'
    if mutate=='source_ref':binding['source_ref']='another_change_source'
    if mutate=='receipt':row['execution_receipts'][0]['experience_id']='exp_b'
    if mutate=='review':row['review']={'experience_id':'exp_b','reviewer':'other'}
    if mutate=='learning':row['learning_bundle']={'experience_id':'exp_b'}
    bound,proof=ground(understanding(binding=binding,kind=kind),[row])
    assert proof['valid'] and bound is not None  # requested identity grounded FIRST
    assert not t._history_requirement_relations(groups=[{'matches':[row]}],understanding=bound.to_read_model())['valid']


@pytest.mark.parametrize('state',['unknown_review','pending_review','negative_learning','missing_receipt'])
def test_grounding_does_not_require_positive_execution_review_or_training(state):
    row=f.record();kind='REVIEW_STATUS';relation='REVIEW_OF_SUBJECT_OR_EXPERIENCE'
    if state=='unknown_review':row['review_status']='UNKNOWN'
    if state=='pending_review':row['review_status']='PARTIAL_PENDING_INDEPENDENT_REVIEW'
    if state=='negative_learning':kind='LEARNING_QUALIFICATION';relation='LEARNING_QUALIFICATION_OF_EXPERIENCE'
    if state=='missing_receipt':kind='EXECUTION';relation='RECEIPT_OF_EFFECT';row['execution_receipts']=[]
    u=understanding(binding=dict(f.subject(relation),subject_goal_id='g1'),kind=kind)
    bound,proof=ground(u,[row]);assert proof['valid'] and bound is not None
    if state!='missing_receipt':assert t._history_requirement_relations(groups=[{'matches':[row]}],understanding=bound.to_read_model())['valid']
    else:assert not t._history_requirement_relations(groups=[{'matches':[row]}],understanding=bound.to_read_model())['valid']
    # Receipt absence remains accepted grounding, not a fabricated execution proof.


@pytest.mark.parametrize('rows',[[],[f.record(),dict(f.record(),experience_id='exp_b')]])
def test_existential_does_not_require_or_autoselect_a_single_subject(rows):
    u=understanding(binding=dict(scope='EXISTENTIAL',relation='REVIEW_OF_SUBJECT_OR_EXPERIENCE',subject_goal_id='g1'),text='Inspect eligible experiences')
    bound,proof=ground(u,rows,reference='eligible experiences',scope='EXISTENTIAL')
    assert bound and proof['valid'] and not proof['requirements']['answer']['subject_selected']


def test_source_document_grounding_is_a_source_not_a_change_subject():
    ref='/project/docs/source.md';row={'source_file':ref,'source_readback':[{'path':ref,'sha256':'current_hash'}]}
    u=understanding(binding=dict(scope='SUBJECT',relation='SOURCE_OF_SUBJECT',subject_goal_id='g1',source_ref=ref),kind='EVIDENCE',query='SOURCE_DOCUMENT',text='Read '+ref)
    bound,proof=ground(u,[row],reference=ref,document=True);assert bound and proof['valid']
    assert dict(bound.response_requirements[0].subject_binding)==dict(u.response_requirements[0].subject_binding)
    assert ground(understanding(),[row],document=True)[0] is None


def test_index_source_label_without_independent_file_readback_is_not_grounding():
    ref='/project/docs/source.md';row={'source_file':ref}
    u=understanding(binding=dict(scope='SUBJECT',relation='SOURCE_OF_SUBJECT',subject_goal_id='g1',source_ref=ref),kind='EVIDENCE',query='SOURCE_DOCUMENT',text='Read '+ref)
    assert ground(u,[row],reference=ref,document=True)[0] is None


def test_saved_natural_model_proposals_do_not_become_grounded_from_matching_records():
    saved=json.loads((A/'owner_20261016_relational_one_natural_after_owner_docker_response.json').read_text())['result']
    raw=copy.deepcopy(saved['understanding'])
    for k in ('request_id','original_text','relevant_context_trace_ids'):raw.pop(k,None)
    for cap in raw['required_capabilities']:cap.pop('schema_version',None)
    u=parse_request_understanding_payload(raw,host_request_id='saved',host_original_text=saved['original_text'])
    frames=tuple(saved['candidate_discovery']['goals'])
    bound,proof=spine._ground_requested_memory_subjects(understanding=u,goalframes=frames,evidence=evidence([f.record()]),source_text=u.original_text)
    assert bound is None and not proof['valid']


@pytest.mark.parametrize('document,rows', [
    (False,[None]), (False,[{'experience_id':'exp_a','actor':[]}]),
    (True,[{'source_readback':[None]}]), (True,[{'source_readback':'invalid'}]),
])
def test_malformed_canonical_readback_fails_closed(document,rows):
    u=understanding(query='SOURCE_DOCUMENT' if document else 'REVIEW_STATUS')
    bound,proof=ground(u,rows,document=document)
    assert bound is None and not proof['valid']
    assert any(e['code']=='canonical_subject_readback_malformed' for e in proof['errors'])


@pytest.mark.parametrize('scope,reference,text', [
    ('EXISTENTIAL','exp_a','Inspect exp_a'),
    ('SUBJECT','EXP_A','Inspect EXP_A'),
    ('SUBJECT','exp_a','Inspect exp_b'),
])
def test_scope_source_and_exact_identity_cannot_be_replaced(scope,reference,text):
    assert ground(understanding(text=text),[f.record()],reference=reference,scope=scope)[0] is None


def test_different_readback_versions_are_ambiguous_not_top_ranked():
    ref='/project/docs/source.md'
    rows=[{'source_readback':[{'path':ref,'sha256':sha}]} for sha in ('version_a','version_b')]
    u=understanding(binding=dict(scope='SUBJECT',relation='SOURCE_OF_SUBJECT',subject_goal_id='g1',source_ref=ref),kind='EVIDENCE',query='SOURCE_DOCUMENT',text='Read '+ref)
    bound,proof=ground(u,rows,reference=ref,document=True)
    assert bound is None and proof['errors'][0]['code']=='requested_subject_ambiguous'


@pytest.mark.parametrize('deferred',[False,True])
def test_real_canonical_sync_and_deferred_paths_withhold_ungrounded_subject(monkeypatch,deferred):
    spec=importlib.util.spec_from_file_location('canonical_turn_fixture',R/'tests/control_plane/test_canonical_semantic_turn_v2.py')
    pipeline=importlib.util.module_from_spec(spec);spec.loader.exec_module(pipeline)
    # Valid conversation plan/evidence, deliberately ungrounded memory obligation.
    # Only semantic-model output is substituted: policy, execution, subject gate,
    # sync/deferred final-author boundary are the actual canonical path.
    raw=json.loads(pipeline.model_payload('{}','conversation.respond',('respond',))['content'])
    raw['response_requirements']=[understanding().response_requirements[0].to_read_model()]
    output=pipeline.verified_model_output(json.dumps(raw))
    final=pipeline.Final()
    from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.conversation_evidence_adapter import ExistingConversationEvidenceAdapter
    result=spine.run_canonical_semantic_turn(text='Inspect exp_a',project_port=pipeline.Project(),
        conversation_port=ExistingConversationEvidenceAdapter(),model_port=pipeline.Model(lambda *_:output),
        final_brain_port=final,permission_port=SemanticPolicyEvaluator(),
        identity=IdentityContext('owner','local_terminal_session','owner',True,True),
        defer_final_brain=deferred)
    assert result['operation_status']=='SUBJECT_GROUNDING_UNAVAILABLE'
    assert not final.calls and 'final_brain_input' not in result
    assert result['understanding']['response_requirements'] and result['evidence_bundle']
    assert not result['subject_grounding']['valid']
