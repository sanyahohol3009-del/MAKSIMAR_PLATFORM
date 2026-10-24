import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

EDGE = Path('/mnt/c/MAKSIMAR_EDGE/jarvis_windows_live_runtime.py')

@pytest.fixture
def edge():
    if not EDGE.is_file(): pytest.skip('WindowsEdge external checkout unavailable')
    spec = importlib.util.spec_from_file_location('edge_host_transport_test', EDGE)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def test_existing_issuer_transport_and_stable_session(edge, monkeypatch):
    calls = []
    def run(args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=0, stdout=json.dumps({
            'session_id': edge.HOST_SESSION_ID, 'host_auth_token': 'test-only-token'}))
    monkeypatch.setattr(edge.subprocess, 'run', run)
    assert edge.host_auth_context() == edge.host_auth_context()
    assert calls[0][-1] == edge.HOST_SESSION_ID
    assert 'bootstrap_local_owner_token' in calls[0][-2]

def test_failed_bootstrap_never_sends_anonymous_request(edge, monkeypatch):
    monkeypatch.setattr(edge.subprocess, 'run', lambda *a, **kw: SimpleNamespace(returncode=1))
    monkeypatch.setattr(edge.request, 'urlopen', lambda *a, **kw: pytest.fail('anonymous HTTP fallback'))
    with pytest.raises(RuntimeError, match='bootstrap_failed'): edge.ask_hotpath('test')

def test_payload_has_signed_context_not_identity_claim(edge, monkeypatch):
    monkeypatch.setattr(edge, 'host_auth_context', lambda: {'session_id':'stable', 'host_auth_token':'test-token'})
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self): return b'{"ok":true}'
    def open_request(req, **kw):
        payload = json.loads(req.data)
        assert payload['host_auth_token'] == 'test-token'
        assert payload['session_id'] == 'stable'
        assert 'owner_identity_claim' not in payload
        assert 'owner_voice_gate_open' not in payload
        return Response()
    monkeypatch.setattr(edge.request, 'urlopen', open_request)
    assert edge.ask_hotpath('test')['ok']
