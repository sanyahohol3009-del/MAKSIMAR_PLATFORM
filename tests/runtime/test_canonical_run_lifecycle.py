"""Canonical lifecycle integration, no service/model/network/physical execution."""
from __future__ import annotations
import copy
import fcntl
import json
import os
import signal
import subprocess
from pathlib import Path
from types import SimpleNamespace
import pytest
from CORE_ROOT import run_context as rc, heartbeat_io as io
from SUPERVISOR import process_supervisor as supervisor, runtime_preflight as preflight


@pytest.fixture
def world(tmp_path, monkeypatch):
    root=tmp_path/"MAKSIMAR_PLATFORM";state=root/"RUNTIME/state";state.mkdir(parents=True)
    proc=tmp_path/"proc";proc.mkdir();calls=[];snapshots=[];handlers={};children=[]
    def make_proc(pid,module,ticks="10000",cwd=None):
        p=proc/str(pid);p.mkdir(exist_ok=True)
        if (p/"cwd").is_symlink():(p/"cwd").unlink()
        (p/"cwd").symlink_to(cwd or root,target_is_directory=True)
        args=["python","-m",module]
        if module=="uvicorn":args.append("CONTROL_PLANE.api_server:app")
        (p/"cmdline").write_bytes(b"\0".join(v.encode() for v in args)+b"\0")
        (p/"stat").write_text(str(pid)+" (worker (with spaces)) "+" ".join(["S"]+["0"]*18+[ticks]))
    make_proc(os.getpid(),"SUPERVISOR.process_supervisor")
    real_ticks=io._process_start_ticks;real_alive=io.heartbeat_process_alive;real_find=io.find_owned_module_process_pids
    monkeypatch.setattr(io,"ROOT",root)
    monkeypatch.setattr(io,"_process_start_ticks",lambda p:real_ticks(proc/p.name if p.parent==Path("/proc") else p))
    monkeypatch.setattr(io,"heartbeat_process_alive",lambda payload,module,**kwargs:real_alive(payload,module,proc_root=proc))
    monkeypatch.setattr(io,"find_owned_module_process_pids",lambda module,**kwargs:real_find(module,proc_root=proc,**{k:v for k,v in kwargs.items() if k!='proc_root'}))
    for module in (rc,io,supervisor):monkeypatch.setattr(module,"ensure_runtime_layout",lambda:None)
    monkeypatch.setattr(rc,"RUN_METADATA_FILE",state/"run_metadata.json")
    monkeypatch.setattr(rc,"RUNTIME_STATE_DIR",state)
    monkeypatch.setattr(supervisor,"ROOT",root)
    monkeypatch.setattr(supervisor,"RUNTIME_HEARTBEAT_FILE",state/"heartbeat_state.json")
    monkeypatch.setattr(supervisor,"DEGRADED_MODE_FILE",state/"degraded_mode.flag")
    monkeypatch.setattr(supervisor,"log",lambda message:calls.append(("log",message)))
    monkeypatch.setattr(supervisor,"record_child_lifecycle",lambda *a,**k:calls.append(("event",a,k)),raising=False)
    python=tmp_path/"python";python.write_text("offline canonical interpreter marker")
    monkeypatch.setattr(supervisor,"resolve_canonical_python",lambda:python)
    monkeypatch.setattr(supervisor.signal,"signal",lambda sig,handler:handlers.__setitem__(sig,handler))
    original_write=supervisor.write_heartbeat
    def heartbeat(status="alive",**kwargs):
        original_write(status,**kwargs)
        calls.append(("heartbeat",status));snapshots.append((status,copy.deepcopy(rc.read_run_metadata())))
    monkeypatch.setattr(supervisor,"write_heartbeat",heartbeat)
    port={"listening":False,"owned_by_project":False,"owner_pids":[],"error":""}
    health={"ok":False,"status":None}
    monkeypatch.setattr(preflight,"_port_snapshot",lambda:copy.deepcopy(port))
    monkeypatch.setattr(preflight,"_health_snapshot",lambda:copy.deepcopy(health))
    class Child:
        def __init__(self,pid):self.pid=pid;self.alive=True;self.returncode=None;make_proc(pid,"uvicorn",str(pid))
        def poll(self):return None if self.alive else self.returncode
        def terminate(self):calls.append(("terminate",self.pid));self.alive=False;self.returncode=0
        def wait(self,timeout):assert not self.alive;return self.returncode
        def kill(self):self.alive=False;self.returncode=-9
    def spawn(*args,**kwargs):
        assert rc.read_run_status() in ('booting','degraded')
        assert rc.run_id(rc.read_run_metadata())
        assert (root/'RUNTIME/runtime.pid').read_text().strip()==str(os.getpid())
        child=Child(901000+len(children));children.append(child);calls.append(("spawn",child.pid));return child
    monkeypatch.setattr(supervisor.subprocess,"Popen",spawn)
    callbacks=[]
    class Event:
        def set(self):pass
        def wait(self,seconds):
            assert seconds in (supervisor.POLL_INTERVAL_SEC,supervisor.RESTART_DELAY_SEC)
            if callbacks:callbacks.pop(0)()
            else:handlers[signal.SIGTERM](signal.SIGTERM,None)
    monkeypatch.setattr(supervisor.threading,"Event",Event)
    return SimpleNamespace(root=root,state=state,proc=proc,calls=calls,snapshots=snapshots,
        handlers=handlers,children=children,make_proc=make_proc,port=port,health=health,callbacks=callbacks,
        real_ticks=real_ticks,real_alive=real_alive)


def test_read_and_import_are_not_metadata_producers(world):
    before=list(world.root.rglob('*'))
    assert rc.read_run_metadata() is None
    assert rc.read_run_status() is None
    assert list(world.root.rglob('*'))==before
    with pytest.raises(RuntimeError):rc.initialize_run_metadata()
    with pytest.raises(RuntimeError):rc.set_run_status('running')
    assert not rc.RUN_METADATA_FILE.exists()


def test_one_exclusive_writer_idempotent_init_and_noninherited_lock(world):
    with rc.run_lifecycle():
        first=rc.initialize_run_metadata();before=rc.RUN_METADATA_FILE.read_bytes()
        assert rc.initialize_run_metadata()==first
        assert rc.RUN_METADATA_FILE.read_bytes()==before
        with pytest.raises(RuntimeError):
            with rc.run_lifecycle():pass
        with (rc.RUNTIME_STATE_DIR/'run_lifecycle.lock').open('a') as other:
            assert not os.get_inheritable(other.fileno())
            with pytest.raises(BlockingIOError):fcntl.flock(other.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        for status in ('running','degraded','shutdown'):
            value=rc.set_run_status(status)
            assert rc._identity(value)==rc._identity(first)
            assert value['status']==status
    with pytest.raises(RuntimeError):rc.set_run_status('running')
    with rc.run_lifecycle():
        second=rc.initialize_run_metadata()
        assert second['run_id']!=first['run_id'] and second['boot_id']!=first['boot_id']


@pytest.mark.parametrize('corrupt', ['missing','other_run','other_boot'])
def test_replaced_context_is_never_adopted_or_overwritten(world,corrupt):
    with rc.run_lifecycle():
        rc.initialize_run_metadata()
        if corrupt=='missing':rc.RUN_METADATA_FILE.unlink()
        else:
            payload=rc.read_run_metadata();payload['run_id' if corrupt=='other_run' else 'boot_id']='foreign'
            rc.RUN_METADATA_FILE.write_text(json.dumps(payload))
        expected=rc.RUN_METADATA_FILE.read_bytes() if rc.RUN_METADATA_FILE.exists() else None
        with pytest.raises(RuntimeError):rc.initialize_run_metadata()
        with pytest.raises(RuntimeError):rc.set_run_status('running')
        assert (rc.RUN_METADATA_FILE.read_bytes() if rc.RUN_METADATA_FILE.exists() else None)==expected


def test_atomic_status_write_failure_retains_original_metadata(world,monkeypatch):
    with rc.run_lifecycle():
        rc.initialize_run_metadata();original=rc.RUN_METADATA_FILE.read_bytes()
        monkeypatch.setattr(io.os,'replace',lambda *a:(_ for _ in ()).throw(OSError('interrupted write')))
        with pytest.raises(OSError):rc.set_run_status('running')
        assert rc.RUN_METADATA_FILE.read_bytes()==original


@pytest.mark.parametrize('peer', ['CORE_ROOT.stop_gate_watcher','CORE_ROOT.core_guard','CORE_ROOT.kernel_watchdog','uvicorn','SUPERVISOR.process_supervisor'])
def test_start_refuses_previous_live_peer_before_replacing_run(world,peer):
    world.make_proc(778899,peer)
    rc.RUN_METADATA_FILE.write_text('{"run_id":"retained previous context"}')
    before=rc.RUN_METADATA_FILE.read_bytes()
    with pytest.raises(RuntimeError,match='existing/unknown'):
        supervisor.main()
    assert rc.RUN_METADATA_FILE.read_bytes()==before
    assert not world.children


@pytest.mark.parametrize('port', [{'listening':True,'error':''},{'listening':False,'error':'unknown'}])
def test_occupied_or_unknown_port_cannot_create_run_metadata(world,port):
    world.port.update(port)
    with pytest.raises(RuntimeError):supervisor.main()
    assert not rc.RUN_METADATA_FILE.exists() and not world.children


def test_actual_supervisor_creates_context_before_child_and_shutdown(world):
    def ready_then_stop():
        child=world.children[0]
        world.port.update(listening=True,owned_by_project=True,owner_pids=[child.pid])
        world.health.update(ok=True,status=200)
    world.callbacks.extend([ready_then_stop])
    supervisor.main()
    assert world.calls.index(next(c for c in world.calls if c[0]=='heartbeat')) < world.calls.index(next(c for c in world.calls if c[0]=='spawn'))
    identities={rc._identity(meta) for _,meta in world.snapshots}
    assert len(identities)==1
    assert {m['status'] for _,m in world.snapshots} >= {'booting','shutdown'}
    assert rc.read_run_status()=='shutdown'
    assert world.snapshots[-1][0]=='stopped'
    assert all(not child.alive for child in world.children)


@pytest.mark.parametrize('bad', ['foreign_port_pid','bad_api','api_not_ready'])
def test_child_poll_or_http_200_alone_does_not_mark_running(world,bad):
    def observe():
        child=world.children[0]
        world.port.update(listening=True,owned_by_project=bad!='bad_api',owner_pids=[child.pid+1 if bad=='foreign_port_pid' else child.pid])
        world.health.update(ok=bad!='api_not_ready',status=200)
        supervisor._update_run_readiness(child)
        assert rc.read_run_status()=='booting'
    world.callbacks.append(observe);supervisor.main()
    assert all(m['status']!='running' for _,m in world.snapshots)


def test_partial_spawn_failure_is_crashed_and_never_healthy(world,monkeypatch):
    monkeypatch.setattr(supervisor.subprocess,'Popen',lambda *a,**k:(_ for _ in ()).throw(OSError('spawn failed')))
    with pytest.raises(OSError):supervisor.main()
    assert rc.read_run_status()=='crashed'
    assert world.snapshots[-1][0]=='broken'


def test_stop_during_startup_has_one_context_and_no_running_claim(world,monkeypatch):
    def interrupted(*a,**k):
        world.handlers[signal.SIGTERM](signal.SIGTERM,None)
        return SimpleNamespace(pid=998877,poll=lambda:0)
    monkeypatch.setattr(supervisor.subprocess,'Popen',interrupted)
    supervisor.main()
    assert rc.read_run_status()=='shutdown'
    assert all(m['status']!='running' for _,m in world.snapshots)


def test_child_retry_preserves_run_identity_and_existing_bounds(world):
    def exit_child():
        world.children[0].alive=False;world.children[0].returncode=7
    world.callbacks.extend([exit_child,lambda:None])
    supervisor.main()
    assert len(world.children)==2
    assert len({rc._identity(m) for _,m in world.snapshots})==1
    assert 'broken' in [status for status,_ in world.snapshots]
    assert rc.read_run_status()=='shutdown'


def test_current_marker_blocks_running_but_previous_marker_is_retained(world):
    marker=world.state/'degraded_mode.flag';marker.write_text('retained')
    os.utime(marker,ns=(1_000_000_000,1_000_000_000))
    def verify():
        child=world.children[0];world.port.update(listening=True,owned_by_project=True,owner_pids=[child.pid]);world.health.update(ok=True,status=200)
        supervisor._update_run_readiness(child)
        assert rc.read_run_status()=='running' and marker.read_text()=='retained'
        os.utime(marker,ns=(os.stat(world.root/'RUNTIME/runtime.pid').st_mtime_ns+1,)*2)
        supervisor._update_run_readiness(child)
        assert rc.read_run_status()=='degraded' and marker.read_text()=='retained'
    world.callbacks.append(verify);supervisor.main()
    assert marker.read_text()=='retained'


def test_exact_heartbeat_propagation_and_actual_preflight_chain(world,monkeypatch):
    monkeypatch.setattr(preflight,'ROOT',world.root)
    monkeypatch.setattr(preflight,'RUN_METADATA_FILE',rc.RUN_METADATA_FILE)
    real_heartbeat=preflight._heartbeat_status
    monkeypatch.setattr(preflight,'_heartbeat_status',lambda path,**kw:real_heartbeat(path,proc_root=world.proc,**kw))
    real_identity=preflight._process_identity
    monkeypatch.setattr(preflight,'_process_identity',lambda pid,**kw:real_identity(pid,proc_root=world.proc))
    monkeypatch.setattr(preflight,'_read_pid_file',lambda:(True,os.getpid()))
    monkeypatch.setattr(preflight,'_tmux_snapshot',lambda:{'available':True,'sessions':sorted(preflight.EXPECTED_SESSIONS),'error':''})
    paths={'runtime':'RUNTIME_HEARTBEAT_FILE','guard':'GUARD_HEARTBEAT_FILE','core_guard':'CORE_GUARD_HEARTBEAT_FILE','kernel_guard':'KERNEL_HEARTBEAT_FILE'}
    for scope,name in paths.items():monkeypatch.setattr(preflight,name,world.state/(scope+'.json'))
    monkeypatch.setattr(preflight,'RUNTIME_HEARTBEAT_FILE',supervisor.RUNTIME_HEARTBEAT_FILE)
    proved=[]
    def prove():
        child=world.children[0]
        api=real_identity(child.pid,proc_root=world.proc)
        world.port.update(listening=True,owned_by_project=True,owner_pids=[child.pid],owner_identities=[api])
        world.health.update(ok=True,status=200)
        supervisor._update_run_readiness(child)
        supervisor.write_heartbeat('alive')
        real_getpid=os.getpid
        for offset,(scope,(source,module)) in enumerate(preflight.EXPECTED_HEARTBEATS.items()):
            if scope=='runtime':continue
            pid=902000+offset;world.make_proc(pid,module)
            with monkeypatch.context() as patch:
                patch.setattr(io.os,'getpid',lambda:pid)
                payload=io.build_heartbeat(source,'alive')
            io.atomic_write_json(getattr(preflight,paths[scope]),payload)
        result=preflight.inspect_runtime_state()
        assert result['decision']['healthy'] is True,result
        from CORE_ROOT import stop_gate,incident_history
        marker=world.state/'degraded_mode.flag';marker.write_text('previous run marker')
        os.utime(marker,ns=(1_000_000_000,)*2)
        trigger=world.state/'stop_gate_trigger.txt';trigger.write_text('previous trigger')
        reason=world.state/'last_degraded_reason.txt';reason.write_text('previous reason')
        for key,value in {'ROOT':world.root,'RUNTIME_STATE_DIR':world.state,
                'DEGRADED_MODE_FILE':marker,'STOP_GATE_TRIGGER_FILE':trigger,
                'LAST_DEGRADED_REASON_FILE':reason}.items():monkeypatch.setattr(stop_gate,key,value)
        monkeypatch.setattr(stop_gate,'ensure_runtime_layout',lambda:None)
        monkeypatch.setattr(stop_gate,'log',lambda _:None)
        monkeypatch.setattr(incident_history,'INCIDENT_HISTORY_FILE',world.state/'incident_history.jsonl')
        monkeypatch.setattr(incident_history,'ensure_runtime_layout',lambda:None)
        assert stop_gate.recover_previous_run_degradation() is True
        assert not marker.exists() and trigger.read_text()=='previous trigger' and reason.read_text()=='previous reason'
        receipt=json.loads((world.state/'incident_history.jsonl').read_text())
        assert receipt['status']=='recovered' and receipt['run_id']==rc.read_run_metadata()['run_id']
        # An incident after run init but before a later PID mtime is current.
        marker.write_text('current startup incident')
        epoch=rc.read_run_metadata()['wall_time']
        os.utime(marker,ns=(int(epoch*1e9)+1000,)*2)
        os.utime(world.root/'RUNTIME/runtime.pid',ns=(int(epoch*1e9)+1000000,)*2)
        assert stop_gate.recover_previous_run_degradation() is False
        assert marker.read_text()=='current startup incident'
        assert len((world.state/'incident_history.jsonl').read_text().splitlines())==1
        # Abrupt owner loss: retained RUNNING metadata cannot substitute for process proof.
        (world.proc/str(os.getpid())/'cmdline').write_bytes(b'')
        assert rc.read_run_status()=='running'
        assert preflight.inspect_runtime_state()['decision']['healthy'] is False
        proved.append(result)
    world.callbacks.append(prove);supervisor.main()
    assert len(proved)==1
    assert preflight.inspect_runtime_state()['decision']['healthy'] is False


def test_abrupt_owner_death_leaves_stale_context_not_false_health(world):
    with rc.run_lifecycle():
        value=rc.initialize_run_metadata();rc.set_run_status('running')
    # Simulate SIGKILL: no terminal writer executes; retained metadata is evidence only.
    (world.proc/str(os.getpid())/'cmdline').write_bytes(b'')
    payload=io.build_heartbeat('process_supervisor')
    assert io.heartbeat_process_alive(payload,'SUPERVISOR.process_supervisor') is False
    assert rc.read_run_metadata()['run_id']==value['run_id']
    assert rc.read_run_status()=='running'


def test_generic_writer_cannot_acquire_run_metadata_authority(world):
    (world.proc/str(os.getpid())/'cmdline').write_bytes(b'python\0-m\0CORE_ROOT.heartbeat_writer\0')
    with pytest.raises(RuntimeError,match='not the canonical supervisor'):
        with rc.run_lifecycle():rc.initialize_run_metadata()
    assert not rc.RUN_METADATA_FILE.exists()


@pytest.mark.parametrize('owned,identity_ok,orderly', [((1234,),True,True),((1234,),True,False),((1234,),False,True),((),True,True),(None,True,True),((1234,5678),True,True)])
def test_actual_ctl_stop_pins_identity_and_preserves_failed_stop_evidence(world,monkeypatch,owned,identity_ok,orderly):
    import select,sys
    script=Path('tools/ctl').read_text().split('stop() {',1)[1]
    code=script.split("<<'PY'\n",1)[1].split('\nPY',1)[0]
    pidfile=world.root/'RUNTIME/runtime.pid';pidfile.write_text('1234')
    monkeypatch.setattr(sys,'argv',['ctl-stop',str(pidfile)])
    monkeypatch.setattr(io,'find_owned_module_process_pids',lambda *a,**k:owned)
    # The no-owned-process case keeps a foreign live hint as diagnostic evidence.
    monkeypatch.setattr(preflight,'_runtime_pid_identity',lambda pid:{'alive':True,'matches':False})
    monkeypatch.setattr(io,'heartbeat_process_alive',lambda *a,**k:identity_ok)
    monkeypatch.setattr(io,'_process_start_ticks',lambda *a:'10000')
    sent=[];closed=[]
    monkeypatch.setattr(os,'pidfd_open',lambda pid:7777)
    monkeypatch.setattr(signal,'pidfd_send_signal',lambda fd,sig:sent.append((fd,sig)))
    monkeypatch.setattr(select,'select',lambda *args:([7777] if orderly else [],[],[]))
    monkeypatch.setattr(os,'close',closed.append)
    try:
        exec(compile(code,'tools/ctl:stop','exec'),{})
        exit_code=0
    except SystemExit as exc:
        exit_code=exc.code
    if owned==():
        assert sent==[] and exit_code==0 and pidfile.exists()
    elif owned is None or len(owned)>1 or not identity_ok:
        assert sent==[] and exit_code!=0 and pidfile.exists()
    elif orderly:
        assert sent==[(7777,signal.SIGTERM)] and exit_code==0 and not pidfile.exists()
    else:
        assert sent==[(7777,signal.SIGTERM),(7777,signal.SIGKILL)]
        assert exit_code!=0 and pidfile.exists()


def test_cli_same_pid_reconciliation_preserves_current_marker_epoch(tmp_path):
    import sys,shlex
    home=tmp_path/'home';root=home/'MAKSIMAR_PLATFORM';(root/'.venv/bin').mkdir(parents=True)
    (root/'.venv/bin/python').symlink_to(sys.executable)
    pid=root/'RUNTIME/runtime.pid';pid.parent.mkdir();pid.write_text('1234\n')
    os.utime(pid,ns=(2_000_000_000,)*2)
    script=Path('tools/ctl').read_text().split('case "${1:-}" in',1)[0]
    overrides="\nfind_runtime_pid() { printf '1234\\n'; }\nwrite_pid_file\nwrite_pid_file\n"
    result=subprocess.run(['bash'],input=script+overrides,env={**os.environ,'HOME':str(home)},text=True,capture_output=True)
    assert result.returncode==0,result.stdout+result.stderr
    assert pid.stat().st_mtime_ns==2_000_000_000


def test_rest_runtime_stop_failure_preserves_receipts_before_cleanup(tmp_path):
    root=tmp_path/'MAKSIMAR_PLATFORM';(root/'tools').mkdir(parents=True)
    state=root/'RUNTIME/state';state.mkdir(parents=True)
    import sys
    (root/'.venv/bin').mkdir(parents=True)
    (root/'.venv/bin/python').symlink_to(sys.executable)
    for package in ('CORE_ROOT','SUPERVISOR'):(root/package).symlink_to(Path.cwd()/package,target_is_directory=True)
    (state/'run_metadata.json').write_text(json.dumps({'schema_version':1,'run_id':'OFFLINE','boot_id':'BOOT','wall_time':1.0,'monotonic_time':1.0,'status':'running'}))
    receipt=state/'heartbeat_state.json';receipt.write_text('original failure evidence')
    calls=tmp_path/'calls'
    for name in ('kernel_guard_ctl','core_guard_ctl','guard_ctl','ctl'):
        p=root/'tools'/name;p.write_text('#!/bin/bash\necho '+name+' >> "'+str(calls)+'"\nexit '+('7' if name=='ctl' else '0')+'\n');p.chmod(0o755)
    result=subprocess.run(['bash',str(Path('tools/rest').resolve())],env={**os.environ,'HOME':str(tmp_path)},capture_output=True,text=True)
    assert result.returncode!=0
    assert receipt.read_text()=='original failure evidence'
    assert calls.read_text().splitlines()==['kernel_guard_ctl','core_guard_ctl','guard_ctl','ctl']


def test_inherited_writer_state_cannot_mutate_current_run(world,monkeypatch):
    with rc.run_lifecycle():
        rc.initialize_run_metadata();original=rc.RUN_METADATA_FILE.read_bytes();pid=os.getpid()
        with monkeypatch.context() as patch:
            patch.setattr(rc.os,'getpid',lambda:pid+1)
            with pytest.raises(RuntimeError):rc.set_run_status('running')
        assert rc.RUN_METADATA_FILE.read_bytes()==original


@pytest.mark.parametrize('bootstrap_status',[0,2])
def test_root_entrypoint_dispatches_only_after_bootstrap(tmp_path,bootstrap_status):
    root=tmp_path/'MAKSIMAR_PLATFORM';(root/'tools').mkdir(parents=True)
    bin_dir=tmp_path/'bin';bin_dir.mkdir();calls=tmp_path/'calls'
    python=bin_dir/'python3';python.write_text('#!/bin/bash\necho BOOT >> "$TEST_CALLS"\nexit '+str(bootstrap_status)+'\n');python.chmod(0o755)
    work=root/'tools/work';work.write_text('#!/bin/bash\necho WORK >> "$TEST_CALLS"\n');work.chmod(0o755)
    result=subprocess.run(['bash',str(Path('start_maksimar.sh').resolve())],env={**os.environ,'HOME':str(tmp_path),'PATH':str(bin_dir)+':'+os.environ['PATH'],'TEST_CALLS':str(calls)},text=True,capture_output=True)
    assert result.returncode==bootstrap_status
    assert calls.read_text().splitlines()==(['BOOT','WORK'] if bootstrap_status==0 else ['BOOT'])


@pytest.mark.parametrize('healthy',[True,False])
def test_actual_work_entrypoint_preserves_idempotency_and_full_chain_gate(tmp_path,healthy):
    import sys
    home=tmp_path/'home';root=home/'MAKSIMAR_PLATFORM';(root/'.venv/bin').mkdir(parents=True)
    (root/'.venv/bin/python').symlink_to(sys.executable);(root/'tools').mkdir()
    (root/'CORE_ROOT').symlink_to(Path.cwd()/'CORE_ROOT',target_is_directory=True)
    for name in ('ctl','ui_open','rest'):
        path=root/'tools'/name;path.write_text('#!/bin/bash\necho FAKE_'+name+'\n');path.chmod(0o755)
    script=Path('tools/work').read_text().rsplit('main "$@"',1)[0]
    overrides="""
run_preflight() { echo PREFLIGHT; return 0; }
preflight_reports_healthy_runtime() { return HEALTHY_CODE; }
recover_previous_run_degradation() { echo CANONICAL_RECOVERY; }
print_truth_summary() { echo SUMMARY; }
remove_disposable_runtime_artifacts() { echo DISPOSABLE; }
start_oob_dashboard() { :; }
create_runtime_dashboard_session() { :; }
start_runtime() { :; }
wait_for_runtime_readiness() { :; }
wait_for_control_plane_health() { :; }
warm_canonical_chat_model() { echo FAKE_WARMUP; }
start_guard() { :; }
start_core_guard() { :; }
start_kernel_watchdog() { :; }
wait_for_guard_chain() { echo REFUSED_CHAIN; return 1; }
open_dashboard_windows() { echo BAD_DASHBOARD; }
main
""".replace('HEALTHY_CODE','0' if healthy else '1')
    result=subprocess.run(['bash'],input=script+overrides,env={**os.environ,'HOME':str(home)},text=True,capture_output=True)
    if healthy:
        assert result.returncode==0
        assert 'CANONICAL_RECOVERY' in result.stdout
        assert 'DISPOSABLE' not in result.stdout and 'FAKE_ctl' not in result.stdout
    else:
        assert result.returncode!=0
        assert 'REFUSED_CHAIN' in result.stdout and 'FAKE_rest' in result.stdout
        assert 'CANONICAL_RECOVERY' not in result.stdout and 'BAD_DASHBOARD' not in result.stdout


def test_work_readiness_wait_reuses_full_preflight_and_keeps_bound():
    source=Path('tools/work').read_text().split('wait_for_guard_chain() {',1)[1].split('\nopen_dashboard_windows()',1)[0]
    assert 'inspect_runtime_state()["decision"]["healthy"] is True' in source
    assert '>= 15' in source
    assert 'touch ' not in source and 'run_metadata' not in source


def test_pending_session_without_owned_pid_is_not_authorized_for_cleanup(world,monkeypatch):
    import sys
    code=Path('tools/ctl').read_text().split('stop() {',1)[1].split("<<'PY'\n",1)[1].split('\nPY',1)[0]
    path=world.root/'RUNTIME/runtime.pid';path.write_text('retained unknown pid')
    monkeypatch.setattr(sys,'argv',['ctl-stop',str(path),'$unowned-session'])
    monkeypatch.setattr(io,'find_owned_module_process_pids',lambda *a,**k:())
    with pytest.raises(SystemExit,match='no proven process owner'):exec(compile(code,'ctl-stop','exec'),{})
    assert path.read_text()=='retained unknown pid'


def test_forced_child_cleanup_does_not_publish_orderly_stop(world):
    def slow_child():
        child=world.children[0]
        child.terminate=lambda:None
        def wait(timeout):
            if child.alive:raise subprocess.TimeoutExpired('synthetic child',timeout)
            return child.returncode
        child.wait=wait
    world.callbacks.append(slow_child);supervisor.main()
    assert rc.read_run_status()=='crashed'
    assert world.snapshots[-1][0]=='broken'
    assert not any(c[0]=='log' and c[1]=='Supervisor exited cleanly.' for c in world.calls)


def test_repeated_init_does_not_reset_running_or_updated_timestamps(world):
    with rc.run_lifecycle():
        rc.initialize_run_metadata();rc.set_run_status('running')
        before=rc.RUN_METADATA_FILE.read_bytes()
        assert rc.initialize_run_metadata()['status']=='running'
        assert rc.RUN_METADATA_FILE.read_bytes()==before


def test_interrupted_initial_replace_preserves_previous_context(world,monkeypatch):
    old=rc.build_run_metadata('shutdown');rc.RUN_METADATA_FILE.write_text(json.dumps(old));before=rc.RUN_METADATA_FILE.read_bytes()
    with rc.run_lifecycle():
        monkeypatch.setattr(io.os,'replace',lambda *a:(_ for _ in ()).throw(OSError('interrupted initial replace')))
        with pytest.raises(OSError):rc.initialize_run_metadata()
        assert rc.RUN_METADATA_FILE.read_bytes()==before


def test_repeated_stop_without_runtime_is_idempotent_and_does_not_create_metadata(tmp_path):
    import sys
    home=tmp_path/'home';root=home/'MAKSIMAR_PLATFORM';(root/'.venv/bin').mkdir(parents=True)
    (root/'.venv/bin/python').symlink_to(sys.executable)
    source=Path('tools/ctl').read_text().split('case "${1:-}" in',1)[0]
    command=source+'\nsession_exists() { return 1; }\nstop\nstop\n'
    result=subprocess.run(['bash'],input=command,env={**os.environ,'HOME':str(home)},text=True,capture_output=True)
    assert result.returncode==0,result.stdout+result.stderr
    assert result.stdout.count('[ctl] done')==2
    assert not (root/'RUNTIME/state/run_metadata.json').exists()


def test_proven_dead_hint_cleanup_allows_clean_next_run_without_touching_markers(world,monkeypatch):
    import sys
    from tests.runtime.test_preflight_recovery_truth import _observation
    code=Path('tools/ctl').read_text().split('stop() {',1)[1].split("<<'PY'\n",1)[1].split('\nPY',1)[0]
    hint=world.root/'RUNTIME/runtime.pid';hint.write_text('999999')
    marker=world.state/'degraded_mode.flag';marker.write_text('historical incident retained')
    monkeypatch.setattr(sys,'argv',['ctl-stop',str(hint),''])
    monkeypatch.setattr(io,'find_owned_module_process_pids',lambda *a,**k:())
    monkeypatch.setattr(preflight,'_runtime_pid_identity',lambda pid:{'alive':False,'matches':False})
    with pytest.raises(SystemExit) as exit:
        exec(compile(code,'ctl-stop','exec'),{})
    assert exit.value.code==0 and not hint.exists()
    assert marker.read_text()=='historical incident retained'
    assert preflight.classify_runtime_observation(_observation(healthy=False))['clean'] is True


def test_incident_between_context_creation_and_pid_publication_is_current(world):
    def prove():
        child=world.children[0];world.port.update(listening=True,owned_by_project=True,owner_pids=[child.pid]);world.health.update(ok=True,status=200)
        epoch=rc.read_run_metadata()['wall_time'];marker=world.state/'degraded_mode.flag';marker.write_text('startup incident')
        os.utime(marker,ns=(int(epoch*1e9)+1000,)*2)
        os.utime(world.root/'RUNTIME/runtime.pid',ns=(int(epoch*1e9)+1000000,)*2)
        supervisor._update_run_readiness(child)
        assert rc.read_run_status()=='degraded'
        assert marker.read_text()=='startup incident'
    world.callbacks.append(prove);supervisor.main()
