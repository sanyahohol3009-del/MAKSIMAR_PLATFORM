from tests.ai_orchestration.test_model_admission_transport import acquisition
import hashlib
import json
from CONTROL_PLANE import canonical_semantic_spine as spine
from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import ExistingOllamaModelUnderstandingAdapter
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline

def test_goalframe_fingerprint_options_match_actual_submitted_understanding(monkeypatch, tmp_path, acquisition):
    submitted = []
    class Response:
        status_code = 200
        content = b'{}'
        def raise_for_status(self): pass
        def json(self):
            return {'model':acquisition['profile'].model_id,'message':{'content':'{}'},'done':True}
    def post(url, *, json, timeout):
        submitted.append(json)
        return Response()
    monkeypatch.setattr(transport.httpx, 'post', post)
    monkeypatch.setattr(obs, '_IN_FLIGHT_TRACE_FILE', tmp_path/'events.jsonl')
    previous = obs._CURRENT_TRACE_ID.set('boundary_test')
    try:
        adapter = ExistingOllamaModelUnderstandingAdapter(json_schema={'type':'object'})
        projection = {'entries':[]}
        fingerprint = spine._goalframe_input_fingerprints(source_text='private_source',
            system_prompt='private_system', user_prompt='private_user', global_projection=projection)
        adapter.understand(system_prompt='private_system',user_prompt='private_user',deadline=RequestDeadline(5))
        events = [json.loads(line) for line in (tmp_path/'events.jsonl').read_text().splitlines()]
        prepared = next(e for e in events if e['stage']=='OLLAMA_REQUEST_PREPARED')
        payload = submitted[0]
        for key in ('num_ctx','num_predict','temperature'):
            assert fingerprint[key] == prepared[key] == payload['options'][key]
        for key in ('system_prompt_sha256','user_prompt_sha256','combined_model_input_sha256'):
            assert fingerprint[key] == prepared[key]
        expected = hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert prepared['model_payload_sha256'] == expected
        assert prepared['seed_present'] is False
        assert not any(raw in (tmp_path/'events.jsonl').read_text() for raw in ('private_source','private_system','private_user'))
    finally:
        obs._CURRENT_TRACE_ID.reset(previous)
