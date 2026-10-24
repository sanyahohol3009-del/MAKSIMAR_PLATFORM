import time
from tools.monitor import oob_foundation_monitor as monitor

def test_oob_never_promotes_stopped_wrong_owner_or_future_receipts(monkeypatch):
    payload={'ts':time.time(),'status':'alive','source':'process_supervisor'}
    monkeypatch.setattr(monitor,'read_json',lambda path:dict(payload))
    assert monitor.heartbeat_status(monitor.RUNTIME_HEARTBEAT_FILE)=='ALIVE'
    payload['status']='stopped'
    assert monitor.heartbeat_status(monitor.RUNTIME_HEARTBEAT_FILE)=='STOPPED'
    payload.update(status='alive',source='wrong_owner')
    assert monitor.heartbeat_status(monitor.RUNTIME_HEARTBEAT_FILE)=='DEGRADED'
    payload.update(source='process_supervisor',ts=time.time()+60)
    assert monitor.heartbeat_status(monitor.RUNTIME_HEARTBEAT_FILE)=='DEGRADED'
    payload['ts']=time.time()-60
    assert monitor.heartbeat_status(monitor.RUNTIME_HEARTBEAT_FILE)=='STALE'
