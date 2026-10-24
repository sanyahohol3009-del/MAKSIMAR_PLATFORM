"""Isolated typed boundary fixtures: no real model/native acceptance calls."""
import copy
import json
import pytest
import jsonschema
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    hydrate_response_requirements,validate_response_obligation_coverage,UnderstandingAttemptPolicy,RequestDeadline,ResponseRequirement)
from MAKSIMAR_SERVER.AI_ORCHESTRATION import model_understanding_adapter as adapter
from CONTROL_PLANE import canonical_semantic_spine as spine

KINDS=('PROVENANCE','RATIONALE','EXECUTION','EVIDENCE','REVIEW_STATUS','LEARNING_QUALIFICATION')
RELATIONS=('ACTOR_OF_SUBJECT','SOURCE_OF_SUBJECT','RECEIPT_OF_EFFECT','SOURCE_OF_SUBJECT','REVIEW_OF_SUBJECT_OR_EXPERIENCE','LEARNING_QUALIFICATION_OF_EXPERIENCE')
def fixture(count=6):
    goals=({'goal_id':'g1','subject_constraints':{'scope':'SUBJECT','actor':'actor_a','experience_id':'experience_a'}},)
    obligations=tuple({'applies_to_goal_ids':['g1'],'description':f'facet_{i}',
        'memory_query_kind':'PROVENANCE','requirement_kind':KINDS[i%len(KINDS)]} for i in range(count))
    return goals,obligations

@pytest.mark.parametrize('count',[1,2,6,7])
def test_typed_declared_obligations_hydrate_once_without_six_constant(count):
    goals,q=fixture(count);before=copy.deepcopy((goals,q));rows=hydrate_response_requirements(goals,q)
    assert len(rows)==count and len({r['response_requirement_id'] for r in rows})==count
    assert [r['subject_binding']['relation'] for r in rows]==[RELATIONS[i%6] for i in range(count)]
    assert {r['subject_binding']['experience_id'] for r in rows}=={'experience_a'}
    assert all(r['subject_binding']['subject_goal_id']=='g1' for r in rows)
    assert (goals,q)==before

@pytest.mark.parametrize('mutation',['missing','duplicate','wrong_kind','extra','missing_binding','missing_relation'])
def test_coverage_rejects_every_projection_loss_or_semantic_change(mutation):
    g,q=fixture();expected=hydrate_response_requirements(g,q);actual=list(copy.deepcopy(expected))
    if mutation=='missing':actual.pop()
    if mutation=='duplicate':actual.append(copy.deepcopy(actual[0]))
    if mutation=='wrong_kind':actual[2]['requirement_kind']='EVIDENCE'
    if mutation=='extra':actual.append({**actual[0],'response_requirement_id':'unrequested'})
    if mutation=='missing_binding':actual[0].pop('subject_binding')
    if mutation=='missing_relation':actual[0]['subject_binding'].pop('relation')
    with pytest.raises(ValueError):validate_response_obligation_coverage(expected,tuple(actual))

@pytest.mark.parametrize('bad',['unknown_kind','no_subject','no_actor','ambiguous_subject'])
def test_no_semantic_or_identity_invention(bad):
    g,q=copy.deepcopy(fixture(1));q=list(q);g=list(g)
    if bad=='unknown_kind':q[0]['requirement_kind']='INVENTED'
    if bad=='no_subject':g[0].pop('subject_constraints')
    if bad=='no_actor':g[0]['subject_constraints'].pop('actor')
    if bad=='ambiguous_subject':q[0]['applies_to_goal_ids']=['g1','g2']
    with pytest.raises(ValueError):hydrate_response_requirements(tuple(g),tuple(q))

@pytest.mark.parametrize('kind,relation',[('REVIEW_STATUS','OPERATION_OF_SUBJECT'),('LEARNING_QUALIFICATION','OPERATION_OF_SUBJECT')])
def test_explicit_legacy_wrong_pairs_are_not_silently_coerced(kind,relation):
    g,q=fixture(1);q=({**q[0],'requirement_kind':kind,'subject_binding':{'scope':'SUBJECT','subject_goal_id':'g1','relation':relation}},)
    with pytest.raises(ValueError):hydrate_response_requirements(g,q)

@pytest.mark.parametrize('kind',KINDS)
def test_model_facing_kind_variants_are_disjoint_and_have_no_internal_bindings(kind):
    _,q=fixture();row=copy.deepcopy(next(x for x in q if x['requirement_kind']==kind))
    schema=spine.GOALFRAME_UNDERSTANDING_JSON_SCHEMA['properties']['response_requirements']['items']
    jsonschema.validate(row,schema)
    assert sum(jsonschema.Draft202012Validator(case).is_valid(row) for case in schema['oneOf'])==1
    assert 'subject_binding' not in schema['properties']
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate({**row,'subject_binding':{}},schema)

@pytest.mark.parametrize('limit,expected',[(1,1),(None,2)])
def test_explicit_request_budget_and_default_product_retry_preserve_all_attempts(monkeypatch,limit,expected):
    calls=[]
    def fake(url,payload,**kwargs):
        calls.append(payload)
        return {'model':'jarvis:chat8b','done':True,'done_reason':'stop','message':{'content':'{}'}}
    monkeypatch.setattr(adapter,'ollama_post_json',fake)
    port=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema={'type':'object','required':['needed']})
    deadline=RequestDeadline(10,understanding_attempt_policy=UnderstandingAttemptPolicy(max_model_attempts=limit))
    result=port.understand(system_prompt='fixture',user_prompt='fixture',deadline=deadline)
    assert len(calls)==expected and not result['final_valid']
    assert len(result['model_attempts'])==expected and len(deadline.understanding_model_attempts)==expected
    assert all(a['raw_response']=='{}' and a['validation_error'] for a in result['model_attempts'])
    assert all(a['user_memory'] is False and a['training_eligible'] is False for a in result['model_attempts'])
    assert result['model_attempts'][-1]['retry_decision'] is False
    if limit==1:
        port.understand(system_prompt='fixture',user_prompt='fixture',deadline=deadline)
        assert len(calls)==1


def test_no_positive_receipt_or_review_or_learning_is_required_to_prepare_typed_questions():
    g,q=fixture();rows=hydrate_response_requirements(g,q)
    assert [r['requirement_kind'] for r in rows]==list(KINDS)
    assert all('receipt_id' not in r['subject_binding'] for r in rows)
    assert all('training_eligible' not in r for r in rows)


def test_last_saved_malformed_candidate_is_still_rejected_without_model_call():
    from pathlib import Path
    a=Path(__file__).resolve().parents[2]/'RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011'
    r=json.loads((a/'owner_20261016_loaded_typed_kind_one_natural_response.json').read_text())['result']
    raw=json.loads(r['goalframe_understanding_attempts'][0]['raw_model_content'])
    with pytest.raises(ValueError):hydrate_response_requirements(tuple(raw['goals']),tuple(raw['response_requirements']))
    assert len(raw['response_requirements'])==5


def test_first_invalid_then_valid_preserves_both_raws_and_no_retry_on_first_valid(monkeypatch):
    calls=[];outputs=iter(['{}','{"needed": true}','{"needed": true}'])
    def fake(*args,**kwargs):
        calls.append(1)
        return {'model':'jarvis:chat8b','done':True,'done_reason':'stop','message':{'content':next(outputs)}}
    monkeypatch.setattr(adapter,'ollama_post_json',fake)
    port=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema={'type':'object','required':['needed']})
    result=port.understand(system_prompt='fixture',user_prompt='fixture',deadline=RequestDeadline(10))
    assert result['final_valid'] and len(calls)==2
    assert [a['raw_response'] for a in result['model_attempts']]==['{}','{"needed": true}']
    assert [a['schema_valid'] for a in result['model_attempts']]==[False,True]
    valid=port.understand(system_prompt='fixture',user_prompt='fixture',deadline=RequestDeadline(10))
    assert valid['final_valid'] and len(calls)==3 and len(valid['model_attempts'])==1


@pytest.mark.parametrize('value',[0,-1,True,'1',1.5])
def test_attempt_budget_is_typed_and_rejects_invalid_values(value):
    with pytest.raises(ValueError):UnderstandingAttemptPolicy(max_model_attempts=value)


def test_same_request_budget_cannot_reset_between_semantic_stages(monkeypatch):
    calls=[]
    def fake(*args,**kwargs):
        calls.append(1)
        return {'model':'jarvis:chat8b','done':True,'done_reason':'stop','message':{'content':'{}'}}
    monkeypatch.setattr(adapter,'ollama_post_json',fake)
    p=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema={'type':'object'},candidate_json_schema={'type':'object'})
    d=RequestDeadline(10,understanding_attempt_policy=UnderstandingAttemptPolicy(max_model_attempts=1))
    assert p.understand(system_prompt='s',user_prompt='u',deadline=d)['final_valid']
    assert not p.discover_candidates(system_prompt='s',user_prompt='u',deadline=d)['final_valid']
    assert len(calls)==1


def test_explicit_hot_payload_budget_parser_reuses_same_typed_contract():
    from CONTROL_PLANE.api_server import _payload_understanding_attempt_policy
    assert _payload_understanding_attempt_policy({'understanding_attempt_policy':{'max_model_attempts':1}}).max_model_attempts==1
    assert _payload_understanding_attempt_policy({}).schema_max_attempts==2
    with pytest.raises(ValueError):_payload_understanding_attempt_policy({'understanding_attempt_policy':{'unknown':1}})


def test_native_binding_hydration_to_real_finalbrain_preparation_and_relational_fixture(monkeypatch):
    import importlib.util,time
    from pathlib import Path
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as t
    root=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('same_owner_offline_fixture',root/'tests/jarvis_live_runtime/test_typed_response_relation_semantics.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    g,q=fixture();g=copy.deepcopy(g);g[0]['subject_constraints']['actor']='ACTOR_A';g[0]['subject_constraints']['experience_id']='exp_a'
    rows=hydrate_response_requirements(g,q)
    u=copy.deepcopy(m.saved_result()['understanding']);u['response_requirements']=list(rows)
    f=m.fixture_module();record=f.record()
    verdict={'supported':list(range(1,8)),'contradictions':[],'unsupported_claims':[], 'relations':[[i,1,0] for i in range(2,8)]}
    calls=f.install_offline_verifier(monkeypatch,verdict)
    evidence={'items':[{'kind':'history_search','observation':{'history_query':{'query_kind':'PROVENANCE','matches':[record]}}}]}
    plan={'steps':[{'capability_id':'runtime_history_store','operation':'search_history'}]}
    prepared=t._bounded_final_brain_inputs(understanding=u,execution_plan=plan,evidence_bundle=evidence,capability_state=(),session_context=None)[0]
    assert prepared['response_requirements']==u['response_requirements']
    assert t._history_requirement_relations(groups=[{'matches':[record]}],understanding=u)['valid']
    out=t._validate_history_publication(content='Recorded actor ACTOR_A source_a receipt_a. Rationale not established. Independent review pending; training_eligible=false.',inputs={'understanding':u,'evidence_bundle':evidence},deadline_at=time.monotonic()+30)
    assert out['valid'] and len(calls)==1
    # The semantic verdict above is a declared fixture; no author was invoked.


@pytest.mark.parametrize('limit,expected',[(None,2),(1,1)])
def test_attempt_raw_and_budget_survive_semantic_turn_to_http_audit_envelope(http_attempt_case,limit,expected):
    state = http_attempt_case('sync', 'retry_valid', limit)
    response = state['response']; result = response.json()['result']
    attempts = result['understanding_model_attempts']
    assert response.status_code == 200
    assert len(state['calls']) == expected == result['understanding_model_attempt_count']
    assert len(attempts) == expected and attempts == result['trace']['understanding_model_attempts']
    assert result['trace']['understanding_model_attempt_count'] == expected
    assert [row['attempt_index'] for row in attempts] == list(range(expected))
    assert [row['request_model_attempt'] for row in attempts] == list(range(1, expected + 1))
    internal = state['deadlines'][0].understanding_model_attempts
    # Old HTTP raw assertions conflicted with the existing safe_structure boundary.
    # Preserve raw/order internally and assert the safe metadata publicly.
    assert [row['raw_response'] for row in internal] == state['raws'][:expected]
    assert state['adapter_result']['final_valid'] is (expected == 2)
    assert attempts[0]['schema_valid'] is False
    if expected == 2:
        assert attempts[0]['retry_decision'] is True and attempts[1]['schema_valid'] is True
    assert attempts[-1]['retry_decision'] is False
    assert all(row['user_memory'] is False and row['training_eligible'] is False for row in attempts)
    assert len(state['captures']) == 1  # One parent turn, never one capture per retry.
    assert result['trace']['trace_id'] == state['payload']['trace_id']
    assert state['sentinel'] not in response.text
    assert all('raw_response' not in row for row in attempts)


def test_default_relation_is_explicit_same_owner_metadata_not_tuple_order(monkeypatch):
    from MAKSIMAR_CORE_LIB.ai_orchestration import semantic_intent_contract as contract
    original=contract._RESPONSE_REQUIREMENT_RELATIONS
    changed={k:{**v,'allowed':tuple(reversed(v['allowed']))} for k,v in original.items()}
    monkeypatch.setattr(contract,'_RESPONSE_REQUIREMENT_RELATIONS',changed)
    g,q=fixture();rows=hydrate_response_requirements(g,q)
    assert [r['subject_binding']['relation'] for r in rows]==list(RELATIONS)


def test_parameter_stage_cannot_reauthor_canonical_response_obligations(monkeypatch):
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "1")
    import importlib.util
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('projection_owner_fixture',root/'tests/control_plane/test_phase_1b_full_capability_world_correction.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    registry=m.select_semantic_projection_details(m.projection(),('runtime_history_store',))
    g,q=fixture();g=copy.deepcopy(g);g[0].update(semantic_domain='memory',effect_intent='retrieve',memory_filter=dict(query_kind='PROVENANCE',time_basis='ANY_TIME',time_start='',time_end=''));registry['selection_goalframes']=g;registry['selection_response_requirements']=q
    schema=spine.request_understanding_schema_for_projection(registry)
    assert 'response_requirements' not in schema['properties'] and 'response_requirements' not in schema['required']
    out=spine._hydrate_host_owned_understanding_fields({'operation_requirements':{}},registry)
    expected=hydrate_response_requirements(g,q)
    validate_response_obligation_coverage(expected,tuple({'schema_version':'response_requirement.v1',**r} for r in out['response_requirements']))


def test_transport_failure_does_not_erase_first_attempt_or_hide_attempt_count(monkeypatch):
    calls=[]
    def wire(*a,**k):
        calls.append(1)
        if len(calls)==2:raise TimeoutError('controlled transport failure')
        return {'model':'jarvis:chat8b','done':True,'done_reason':'stop','message':{'content':'{}'}}
    monkeypatch.setattr(adapter,'ollama_post_json',wire)
    p=adapter.ExistingOllamaModelUnderstandingAdapter(json_schema={'type':'object','required':['needed']})
    d=RequestDeadline(10)
    with pytest.raises(TimeoutError):p.understand(system_prompt='s',user_prompt='u',deadline=d)
    assert d.understanding_model_attempt_count==len(d.understanding_model_attempts)==len(calls)==2
    assert d.understanding_model_attempts[0]['raw_response']=='{}'
    assert d.understanding_model_attempts[1]['response_received'] is False
    assert d.understanding_model_attempts[1]['retry_decision'] is False


@pytest.fixture
def http_attempt_case(monkeypatch, tmp_path):
    """Actual adapter/deadline/Spine wrapper/HTTP boundary, isolated semantic execution."""
    import asyncio
    import uuid
    import httpx
    from types import SimpleNamespace
    from CONTROL_PLANE import api_server as api
    from tests.control_plane.test_jarvis_live_hot_endpoint_smoke import isolate_existing_hot_endpoint_state
    isolate_existing_hot_endpoint_state.__wrapped__(monkeypatch, tmp_path)
    monkeypatch.setattr(api, '_semantic_capability_projection', lambda: {'entries': []})
    real_turn = spine.run_canonical_semantic_turn
    real_capture = api._capture_canonical_turn_memory
    real_stage = adapter.trace_stage
    state = {'calls': [], 'captures': [], 'internal': [], 'snapshots': [], 'stages': [], 'deadlines': []}
    def run(mode, scenario='retry_valid', limit=None):
        sentinel = 'private-understanding-' + uuid.uuid4().hex
        invalid = json.dumps({'needed': sentinel, 'private_diagnostic': sentinel})
        valid = json.dumps({'needed': True, 'private_diagnostic': sentinel})
        state.update(sentinel=sentinel, raws=[valid] if scenario == 'first_valid' else [invalid, invalid if scenario == 'failed' else valid])
        outputs = iter(state['raws'])
        def fake(*args, **kwargs):
            state['calls'].append(1)
            return {'model': adapter.PRIMARY_CONVERSATION_MODEL_ID, 'done': True, 'done_reason': 'stop',
                    'message': {'content': next(outputs)}}
        monkeypatch.setattr(adapter, 'ollama_post_json', fake)
        def stage(*args, **kwargs):
            if args[0] == 'UNDERSTANDING_ATTEMPT': state['stages'].append(copy.deepcopy(kwargs['safe_structure']))
            return real_stage(*args, **kwargs)
        monkeypatch.setattr(adapter, 'trace_stage', stage)
        port = adapter.ExistingOllamaModelUnderstandingAdapter(json_schema={
            'type': 'object', 'required': ['needed'], 'properties': {'needed': {'type': 'boolean'}}})
        def after_input(**kwargs):
            deadline = kwargs['request_deadline']; state['deadlines'].append(deadline)
            answer = ({'final_valid': False, 'model_attempts': []} if scenario == 'not_attempted' else
                      port.understand(system_prompt='fixture', user_prompt='fixture', deadline=deadline))
            state['adapter_result'] = answer
            # Existing goalframe diagnostic alias; stays internal with the source attempt.
            kwargs['helper_trace']['goalframe_understanding_attempts'] = [
                {'attempt': i, 'raw_model_content': row['raw_response'], 'validation_violations': None}
                for i, row in enumerate(deadline.understanding_model_attempts)]
            success = answer['final_valid']
            return {'operation_status': ('FINAL_BRAIN_PENDING' if kwargs['defer_final_brain'] else 'COMPLETE') if success else 'UNDERSTANDING_UNAVAILABLE',
                'response_text': 'Controlled public answer.' if success and not kwargs['defer_final_brain'] else '',
                'trace_id': kwargs['trace_id'], 'trace': {'trace_id': kwargs['trace_id'], 'stages': ['understanding']},
                'understanding': {'effect_type': 'OBSERVE', 'current_topic': 'fixture'},
                'selected_capabilities': [], 'selected_provider_operation': [], 'evidence_bundle': {'items': [], 'receipts': []},
                'execution_plan': {'steps': []}, 'final_brain_input': {}, 'generation_completed': success and not kwargs['defer_final_brain'],
                'response_execution_status': 'COMPLETE' if success and not kwargs['defer_final_brain'] else 'NOT_EXECUTED',
                'adapter_result_valid': success}
        monkeypatch.setattr(spine, '_run_canonical_semantic_turn_after_input', after_input)
        def turn(**kwargs):
            kwargs['registry_projection'] = None
            value = real_turn(**kwargs)
            state['internal'].append(value); state['snapshots'].append(copy.deepcopy(value))
            return value
        monkeypatch.setattr(api, 'run_canonical_semantic_turn', turn)
        monkeypatch.setattr(spine, 'run_canonical_semantic_turn', turn)
        def capture(*args):
            state['captures'].append(copy.deepcopy(args[0]))
            return real_capture(*args)
        monkeypatch.setattr(api, '_capture_canonical_turn_memory', capture)
        def final_stream(**kwargs):
            assert kwargs['deadline'] is state['deadlines'][0]
            yield {'event': 'chunk', 'chunk': 'Controlled public answer.'}
            yield {'event': 'done', 'response_text': 'Controlled public answer.', 'model_call_attempted': True,
                'model_call_succeeded': True, 'raw_output_present': True, 'done': True, 'done_reason': 'stop', 'truncation': False}
        monkeypatch.setattr(api, 'FINAL_BRAIN_ADAPTER', SimpleNamespace(stream_answer=final_stream))
        payload = {'text': 'offline typed contract fixture', 'trace_id': 'trace_' + uuid.uuid4().hex,
                   'session_id': 'attempt_fixture', 'stream': mode == 'stream'}
        if limit is not None: payload['understanding_attempt_policy'] = {'max_model_attempts': limit}
        async def request():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=api.app), base_url='http://offline') as client:
                return await client.post('/jarvis-live/hot', json=payload)
        state['response'] = asyncio.run(request()); state['payload'] = payload
        return state
    return run


@pytest.mark.parametrize('mode', ['sync', 'stream'])
@pytest.mark.parametrize('scenario', ['failed', 'retry_valid', 'first_valid'])
@pytest.mark.parametrize('limit', [None, 1])
def test_actual_http_understanding_attempt_projection_preserves_private_diagnostics(http_attempt_case, mode, scenario, limit):
    from pathlib import Path
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store as store
    state = http_attempt_case(mode, scenario, limit)
    response = state['response']
    assert response.status_code == 200
    public = response.json() if mode == 'sync' else [json.loads(line) for line in response.text.splitlines()]
    result = public['result'] if mode == 'sync' else public[-1]['result']
    attempts = result['understanding_model_attempts']
    expected = 1 if scenario == 'first_valid' or limit == 1 else 2
    success = scenario == 'first_valid' or scenario == 'retry_valid' and limit is None
    assert len(state['calls']) == len(attempts) == expected
    assert result['understanding_model_attempt_count'] == result['trace']['understanding_model_attempt_count'] == expected
    assert attempts == result['trace']['understanding_model_attempts']
    assert [row['attempt_index'] for row in attempts] == list(range(expected))
    assert [row['request_model_attempt'] for row in attempts] == list(range(1, expected + 1))
    assert attempts[-1]['retry_decision'] is False
    internal = state['deadlines'][0].understanding_model_attempts
    assert [row['raw_response'] for row in internal] == state['raws'][:expected]
    assert state['internal'][0]['understanding_model_attempts'] == internal
    assert [row['raw_model_content'] for row in state['internal'][0]['goalframe_understanding_attempts']] == state['raws'][:expected]
    if mode == 'sync' or not success:
        assert state['internal'] == state['snapshots']
    # Exact existing stage metadata shape, with public validation ERROR CODE only.
    for audit, stage in zip(attempts, state['stages']):
        assert set(audit) == set(stage)
        assert audit['validation_error'] == stage['validation_error'].split(':', 1)[0]
        assert {k: v for k, v in audit.items() if k != 'validation_error'} == {k: v for k, v in stage.items() if k != 'validation_error'}
        assert audit['model_role'] == internal[0]['model_role']
    assert state['sentinel'] not in response.text
    pending = [public]
    while pending:
        value = pending.pop()
        if isinstance(value, dict):
            assert not {'raw_response', 'raw_response_text', 'raw_model_content', 'final_brain_result'} & set(value)
            pending.extend(value.keys()); pending.extend(value.values())
        elif isinstance(value, list): pending.extend(value)
        elif isinstance(value, str): assert state['sentinel'] not in value
    assert len(state['captures']) == 1
    assert state['captures'][0]['understanding_model_attempts'] == internal
    assert result['trace']['trace_id'] == state['payload']['trace_id']
    if mode == 'stream':
        assert public[0]['event'] == 'accepted' and public[1]['event'] == 'status'
        assert 'understanding_model_attempts' not in public[0] and 'understanding_model_attempts' not in public[1]
        assert public[-1]['event'] == ('done' if success else 'error')
        assert all(state['sentinel'] not in line for line in response.text.splitlines())
        assert state['deadlines'][0].cancelled
        if not success: assert not any(event['event'] in {'chunk', 'done'} for event in public)
    else:
        assert public['ok'] is success
        assert public['executed'] is False
    assert result['generation_completed'] is success
    assert result['learning_bundle'] is None
    assert result['session_event']['assistant_text'] == ('Controlled public answer.' if success else '')
    # Normal capture remains temporary; no raw diagnostic is copied into memory.
    memory = Path(store._session_turn_log_path()).read_text()
    assert state['sentinel'] not in memory
    assert len(memory.splitlines()) == 1
    assert RequestDeadline.current() is None


@pytest.mark.parametrize('mode', ['sync', 'stream'])
def test_http_audit_never_fabricates_an_unperformed_understanding_attempt(http_attempt_case, mode):
    state = http_attempt_case(mode, 'not_attempted', 1)
    response = state['response']
    public = response.json() if mode == 'sync' else [json.loads(line) for line in response.text.splitlines()]
    result = public['result'] if mode == 'sync' else public[-1]['result']
    assert response.status_code == 200
    assert state['calls'] == state['deadlines'][0].understanding_model_attempts == []
    assert result['understanding_model_attempts'] == result['trace']['understanding_model_attempts'] == []
    assert result['understanding_model_attempt_count'] == result['trace']['understanding_model_attempt_count'] == 0
    assert state['sentinel'] not in response.text
    if mode == 'stream': assert not any(row['event'] in {'chunk', 'done'} for row in public)
    else: assert public['ok'] is False
