import json
from datetime import UTC, datetime, timedelta
import pytest
from fastapi import HTTPException
from MAKSIMAR_CORE_LIB.security_layer.host_principal import HostPrincipal, issue_host_token
from MAKSIMAR_CORE_LIB.security_layer.host_approval_handshake import HostApprovalStore
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PermissionDecision
from MAKSIMAR_SERVER.OBSERVABILITY.operator_shell_read_model import require_operator_read, event_projection, envelope


def test_principal_session_and_expiry_fail_closed(monkeypatch):
    monkeypatch.setenv('JARVIS_HOST_AUTH_SECRET', 'operator-test-only')
    token = issue_host_token(HostPrincipal('owner', 'session_a'))
    assert require_operator_read(token, 'session_a')[1].owner_authorized
    for bad_token, session, status in [('', 'session_a', 401), (token+'.bad', 'session_a', 401),
                                        (token, 'session_b', 403),
                                        (issue_host_token(HostPrincipal('owner', 'session_a'), ttl_seconds=-1), 'session_a', 401),
                                        (issue_host_token(HostPrincipal('child', 'session_a', 'child')), 'session_a', 401)]:
        with pytest.raises(HTTPException) as exc: require_operator_read(bad_token, session)
        assert exc.value.status_code == status


def event(ident='one', when=None):
    return {'event_id':ident, 'event_type':'sample.observed', 'source':'test_owner',
            'created_at':when or datetime.now(UTC).isoformat(), 'payload':{'password':'DO_NOT_EXPOSE', 'prompt':'private'}}


def test_event_cursor_redaction_append_and_partial_line(tmp_path):
    path=tmp_path/'journal.jsonl';path.write_text(json.dumps(event())+'\n')
    before=path.read_bytes();first=event_projection(journal=path)
    assert 'DO_NOT_EXPOSE' not in json.dumps(first) and first['events'][0]['payload_redacted']
    assert path.read_bytes()==before
    assert event_projection(journal=path,cursor=first['cursor'])['events']==[]
    with path.open('a') as f:f.write(json.dumps(event('two'))+'\n'+json.dumps(event('three')))
    second=event_projection(journal=path,cursor=first['cursor'])
    assert not second['reset'] and [e['event_id'] for e in second['events']]==['two']
    with path.open('a') as f:f.write('\n')
    assert [e['event_id'] for e in event_projection(journal=path,cursor=second['cursor'])['events']]==['three']


def test_event_rotation_invalid_cursor_and_stale_sample(tmp_path):
    path=tmp_path/'journal.jsonl';path.write_text(json.dumps(event(when=(datetime.now(UTC)-timedelta(days=2)).isoformat()))+'\n')
    first=event_projection(journal=path);assert first['events'][0]['status']=='STALE'
    old=tmp_path/'old';path.rename(old);path.write_text(json.dumps(event('new'))+'\n')
    assert event_projection(journal=path,cursor=first['cursor'])['reset']
    with pytest.raises(HTTPException):event_projection(journal=path,cursor='invalid')
    path.write_text('x'*70000+'\n')
    with pytest.raises(HTTPException) as exc:event_projection(journal=path)
    assert exc.value.status_code==503


def test_missing_timestamp_is_not_live_and_future_timestamp_degrades():
    assert envelope(4,source='fixture',status='LIVE')['status']=='NO_DATA'
    assert envelope(4,source='future',produced_at=(datetime.now(UTC)+timedelta(hours=1)).isoformat(),status='LIVE')['status']=='DEGRADED'


def test_pending_projection_uses_existing_store_session_and_expiry():
    store=HostApprovalStore(ttl_seconds=1)
    decision=PermissionDecision(granted=False, capability_id='sample',identity_source='host',policy_version='semantic_policy.v1',denial_reason='approval_required',trace_id='trace',operation_id='op',approval_required=True,step_id='step')
    pending=store.create(request_id='request',session_id='a',decision=decision,plan_step={'step_id':'step'},description='review')
    assert [p.approval_id for p in store.pending_for_session('a')]==[pending.approval_id]
    assert store.pending_for_session('b')==()
    store.decide(pending.approval_id,approved=False,approver_id='owner',session_id='a')
    assert store.pending_for_session('a')==()
