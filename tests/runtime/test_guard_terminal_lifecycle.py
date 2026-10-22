"""Existing guard lifecycle: real writers/signals in TMP, no live runtime/providers."""
import copy
import fcntl
import importlib
import json
import os
from pathlib import Path
import select
import shlex
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
import pytest
from CORE_ROOT import heartbeat_io as io, run_context as rc

GUARDS = [
    ("stop_gate_watcher", "write_self_heartbeat", "evaluate_runtime"),
    ("core_guard", "write_self_heartbeat", "evaluate_guard"),
    ("kernel_watchdog", "write_kernel_heartbeat", "evaluate_core_guard"),
]

@pytest.fixture
def world(tmp_path, monkeypatch):
    state=tmp_path/"state";state.mkdir()
    monkeypatch.setattr(rc,"RUNTIME_STATE_DIR",state)
    monkeypatch.setattr(rc,"RUN_METADATA_FILE",state/"run_metadata.json")
    monkeypatch.setattr(rc,"ensure_runtime_layout",lambda:None)
    monkeypatch.setattr(io,"ensure_runtime_layout",lambda:None)
    meta={"schema_version":1,"run_id":"OFFLINE_RUN","boot_id":"OFFLINE_BOOT",
          "wall_time":time.time()-10,"monotonic_time":time.monotonic()-10,"status":"running"}
    rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
    return SimpleNamespace(state=state,meta=meta,hb=state/"heartbeat.json",hint=state/"guard.pid")

@pytest.mark.parametrize("name,writer,evaluate",GUARDS)
def test_guard_owned_writer_persists_same_run_and_terminal_cannot_become_alive(world,monkeypatch,name,writer,evaluate):
    m=importlib.import_module("CORE_ROOT."+name)
    for key in ("GUARD_HEARTBEAT_FILE","CORE_GUARD_HEARTBEAT_FILE","KERNEL_HEARTBEAT_FILE"):
        if hasattr(m,key):monkeypatch.setattr(m,key,world.hb)
    monkeypatch.setattr(m,"ensure_runtime_layout",lambda:None)
    write=getattr(m,writer);identity=rc._identity(world.meta)
    write("alive",expected_run=identity)
    write("stopped",expected_run=identity)
    saved=world.hb.read_bytes();data=json.loads(saved)
    assert data["run_id"]==world.meta["run_id"] and data["pid"]==os.getpid()
    assert data["source"]==name and data["status"]=="stopped"
    assert data["process_start_ticks"]==io._process_start_ticks(Path("/proc/self").resolve())
    with pytest.raises(RuntimeError,match="cannot return to alive"):write("alive",expected_run=identity)
    assert world.hb.read_bytes()==saved

@pytest.mark.parametrize("change",["run_id","boot_id","monotonic_time","missing"])
def test_guard_writer_refuses_replaced_or_missing_run(world,change):
    identity=rc._identity(world.meta)
    if change=="missing":rc.RUN_METADATA_FILE.unlink()
    else:
        changed=copy.deepcopy(world.meta);changed[change]="foreign"
        rc.RUN_METADATA_FILE.write_text(json.dumps(changed))
    with pytest.raises(RuntimeError,match="run identity"):
        io.write_guard_heartbeat(world.hb,"core_guard",expected_run=identity)
    assert not world.hb.exists()

@pytest.mark.parametrize("failure",["write","readback","directory_fsync"])
def test_terminal_writer_failure_is_not_hidden(world,monkeypatch,failure):
    if failure=="write":monkeypatch.setattr(io,"atomic_write_json",lambda *a,**k:(_ for _ in ()).throw(OSError("WRITE_FAILED")))
    if failure=="readback":monkeypatch.setattr(io,"safe_read_json",lambda *a:None)
    if failure=="directory_fsync":
        real=os.fsync
        def fsync(fd):
            import stat
            if stat.S_ISDIR(os.fstat(fd).st_mode):raise OSError("DIRECTORY_FSYNC_FAILED")
            return real(fd)
        monkeypatch.setattr(os,"fsync",fsync)
    with pytest.raises((OSError,RuntimeError)):
        io.write_guard_heartbeat(world.hb,"core_guard","stopped",expected_run=rc._identity(world.meta))

@pytest.fixture
def stopping(world,monkeypatch):
    w=world;w.pid=7777777;w.sent=[];w.waits=[];w.closed=[]
    w.hint.write_text(str(w.pid)+"\n")
    before=io.build_heartbeat("core_guard")
    before.update(pid=w.pid,process_start_ticks="12345")
    w.hb.write_text(json.dumps(before));w.before=before
    monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:(w.pid,))
    monkeypatch.setattr(io,"_process_start_ticks",lambda p:"12345")
    monkeypatch.setattr(io,"heartbeat_process_alive",lambda *a,**k:True)
    monkeypatch.setattr(os,"pidfd_open",lambda pid:9876543)
    real_close=os.close
    monkeypatch.setattr(os,"close",lambda fd:w.closed.append(fd) if fd==9876543 else real_close(fd))
    monkeypatch.setattr(signal,"pidfd_send_signal",lambda fd,sig:w.sent.append(sig))
    def complete(*args):
        w.waits.append(args[-1])
        receipt=copy.deepcopy(before);receipt.update(status="stopped",monotonic_ts=time.monotonic(),ts=time.time())
        w.hb.write_text(json.dumps(receipt))
        return [9876543],[],[]
    monkeypatch.setattr(select,"select",complete);w.complete=complete
    w.stop=lambda **kwargs:io.stop_owned_guard_process("CORE_ROOT.core_guard","core_guard",w.hint,w.hb,**kwargs)
    return w

def test_verified_stop_pins_process_waits_reads_same_run_and_removes_only_hint(stopping,monkeypatch):
    w=stopping;w.stop()
    assert w.sent==[signal.SIGTERM] and w.waits==[1.0] and w.closed==[9876543]
    assert not w.hint.exists() and json.loads(w.hb.read_text())["status"]=="stopped"
    monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:())
    w.stop()
    assert w.sent==[signal.SIGTERM]  # repeat only after independently valid terminal receipt

@pytest.mark.parametrize("case",["foreign_pid","reused_pid","missing_owner","ambiguous","inspection_failed","wrong_run","wrong_source","wrong_ticks","missing_heartbeat","wrong_schema"])
def test_stop_refuses_unverified_identity_without_signalling_or_evidence_loss(stopping,monkeypatch,case):
    w=stopping
    if case=="foreign_pid":monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:())
    if case=="reused_pid":monkeypatch.setattr(io,"heartbeat_process_alive",lambda *a,**k:False)
    if case=="missing_owner":monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:())
    if case=="ambiguous":monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:(w.pid,w.pid+1))
    if case=="inspection_failed":monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:None)
    keys={"wrong_run":("run_id","foreign"),"wrong_source":("source","surface-id"),
          "wrong_ticks":("process_start_ticks","999"),"wrong_schema":("schema_version",True)}
    if case in keys:
        data=copy.deepcopy(w.before);k,v=keys[case];data[k]=v;w.hb.write_text(json.dumps(data))
    if case=="missing_heartbeat":w.hb.unlink()
    before=w.hb.read_bytes() if w.hb.exists() else None
    with pytest.raises(RuntimeError):w.stop()
    assert not w.sent and w.hint.exists()
    assert (w.hb.read_bytes() if w.hb.exists() else None)==before

@pytest.mark.parametrize("case",["no_receipt","wrong_run","wrong_source","wrong_pid","wrong_ticks","old_receipt","write_failed","metadata_replaced","hint_replaced"])
def test_exit_without_valid_new_terminal_receipt_remains_failed(stopping,monkeypatch,case):
    w=stopping
    def incomplete(*args):
        w.complete(*args)
        data=json.loads(w.hb.read_text())
        changes={"no_receipt":("status","alive"),"wrong_run":("run_id","foreign"),
                 "wrong_source":("source","foreign"),"wrong_pid":("pid",1),
                 "wrong_ticks":("process_start_ticks","999"),"old_receipt":("monotonic_ts",0)}
        if case in changes:
            k,v=changes[case];data[k]=v;w.hb.write_text(json.dumps(data))
        if case=="write_failed":w.hb.unlink()
        if case=="metadata_replaced":
            meta=copy.deepcopy(w.meta);meta["run_id"]="foreign"
            rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
        if case=="hint_replaced":w.hint.write_text("9999999\n")
        return [9876543],[],[]
    monkeypatch.setattr(select,"select",incomplete)
    with pytest.raises(RuntimeError):w.stop()
    assert w.sent==[signal.SIGTERM] and w.hint.exists() and w.closed==[9876543]

def test_timeout_forced_stop_never_claims_graceful_or_rewrites_receipt(stopping,monkeypatch):
    w=stopping;raw=w.hb.read_bytes()
    monkeypatch.setattr(select,"select",lambda *a:([],[],[]))
    with pytest.raises(RuntimeError,match="forced"):w.stop()
    assert w.sent==[signal.SIGTERM,signal.SIGKILL] and w.waits==[]
    assert w.hb.read_bytes()==raw and w.hint.exists() and w.closed==[9876543]

def test_concurrent_stop_request_fails_before_any_signal(stopping):
    w=stopping
    with rc.startup_reservation():
        with pytest.raises(BlockingIOError):w.stop()
    assert w.sent==[] and w.hint.exists()

def test_orphan_session_cannot_be_deleted_by_idempotent_stop(stopping,monkeypatch):
    w=stopping;w.complete(None);monkeypatch.setattr(io,"find_owned_module_process_pids",lambda *a,**k:())
    with pytest.raises(RuntimeError,match="session has no proven"):w.stop(session_id="$123")
    assert not w.sent and w.hint.exists()

@pytest.mark.parametrize("tool",["guard_ctl","core_guard_ctl","kernel_guard_ctl"])
@pytest.mark.parametrize("success",[True,False])
def test_controller_graceful_receipt_check_precedes_exact_tmux_cleanup(tmp_path,tool,success):
    source=Path("tools",tool).read_text();function=source[source.index("stop() {"):source.index("\nstatus() {")]
    trace=tmp_path/"trace";binary=tmp_path/"bin";binary.mkdir()
    python=binary/"python3";python.write_text("#!/bin/bash\ncat >/dev/null\necho verify_stop >> \"$TRACE\"\nexit "+("0" if success else "7")+"\n");python.chmod(0o700)
    script=tmp_path/"controller.sh"
    script.write_text("""set -euo pipefail
ROOT=/OFFLINE
SESSION_NAME=fixture
PID_FILE=/OFFLINE/pid
HEARTBEAT_FILE=/OFFLINE/hb
log() { :; }
reserve_lifecycle() { :; }
session_exists() { return 0; }
tmux() { if [[ "$1" == display-message ]]; then echo '$42'; else echo "tmux:$*" >> "$TRACE"; fi; }
"""+function+"\nstop\n")
    x=subprocess.run(["bash",str(script)],env={**os.environ,"PATH":str(binary)+":"+os.environ["PATH"],"TRACE":str(trace)},capture_output=True,text=True)
    assert x.returncode==(0 if success else 1)
    assert trace.read_text().splitlines()==(["verify_stop","tmux:kill-session -t $42"] if success else ["verify_stop"])

@pytest.mark.parametrize("failed",["kernel_guard_ctl","core_guard_ctl","guard_ctl"])
def test_rest_propagates_guard_failure_and_preserves_dependency_order(tmp_path,failed):
    home=tmp_path/"home";tools=home/"MAKSIMAR_PLATFORM/tools";tools.mkdir(parents=True);trace=tmp_path/"trace"
    root=tools.parent
    (root/".venv/bin").mkdir(parents=True)
    (root/".venv/bin/python").symlink_to(sys.executable)
    for package in ("CORE_ROOT","SUPERVISOR"):(root/package).symlink_to(Path.cwd()/package,target_is_directory=True)
    state=root/"RUNTIME/state";state.mkdir(parents=True)
    (state/"run_metadata.json").write_text(json.dumps({"schema_version":1,"run_id":"OFFLINE","boot_id":"BOOT","wall_time":1.0,"monotonic_time":1.0,"status":"running"}))
    names=["kernel_guard_ctl","core_guard_ctl","guard_ctl","ctl"]
    for n in names:
        p=tools/n;p.write_text("#!/bin/bash\necho "+n+" >> \"$TRACE\"\nexit "+("7" if n==failed else "0")+"\n");p.chmod(0o700)
    script=tmp_path/"rest.sh";script.write_text(Path("tools/rest").read_text())
    x=subprocess.run(["bash",str(script)],env={**os.environ,"HOME":str(home),"TRACE":str(trace)},capture_output=True,text=True)
    assert x.returncode==1 and trace.read_text().splitlines()==names[:names.index(failed)+1]

CHILD = r'''
import sys,os,time,json,importlib
from pathlib import Path
sys.path.insert(0,sys.argv[1]);target=Path(sys.argv[2]);name=sys.argv[3];mode=sys.argv[4]
from CORE_ROOT import run_context as rc,heartbeat_io as io
m=importlib.import_module("CORE_ROOT."+name)
rc.RUNTIME_STATE_DIR=target;rc.RUN_METADATA_FILE=target/"run_metadata.json"
rc.ensure_runtime_layout=lambda:None;io.ensure_runtime_layout=lambda:None;m.ensure_runtime_layout=lambda:None
m.log=lambda message:None
for attr in ["GUARD_HEARTBEAT_FILE","CORE_GUARD_HEARTBEAT_FILE","KERNEL_HEARTBEAT_FILE"]:
 if hasattr(m,attr):setattr(m,attr,target/"hb.json")
meta={"schema_version":1,"run_id":"NON_USER_DIAGNOSTIC","boot_id":"OFFLINE","wall_time":time.time(),"monotonic_time":time.monotonic(),"status":"running"}
rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
setattr(m,{"stop_gate_watcher":"evaluate_runtime","core_guard":"evaluate_guard","kernel_watchdog":"evaluate_core_guard"}[name],lambda **kwargs:(False,"offline",0))
original=io.atomic_write_json
def write(path,data):
 if data.get("status")=="stopped":
  if mode=="write_failure":raise OSError("OFFLINE_TERMINAL_WRITE_FAILURE")
  if mode=="duplicate":time.sleep(.15)
 return original(path,data)
io.atomic_write_json=write
def audit(event,args):
 if event=="open":
  p,mode,flags=args
  writing=(isinstance(mode,str) and any(x in mode for x in "wax+")) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
  if writing and not isinstance(p,int) and not Path(p).resolve().is_relative_to(target.resolve()):raise RuntimeError("fixture write escape")
 if event in ["socket.connect","subprocess.Popen","os.system"]:raise RuntimeError("fixture external effect")
sys.addaudithook(audit)
m.main()
'''

@pytest.mark.parametrize("name,writer,evaluate",GUARDS)
@pytest.mark.parametrize("mode,sig",[("normal",signal.SIGINT),("normal",signal.SIGTERM),("normal",signal.SIGHUP),("duplicate",signal.SIGTERM),("write_failure",signal.SIGTERM),("run_replaced",signal.SIGTERM)])
def test_real_guard_signal_exit_and_terminal_readback_in_isolated_process(tmp_path,name,writer,evaluate,mode,sig):
    script=tmp_path/"guard_child.py";script.write_text(CHILD)
    with (tmp_path/"output.log").open("w") as log:
        p=subprocess.Popen([sys.executable,"-B",str(script),str(Path.cwd()),str(tmp_path),name,mode],stdout=log,stderr=subprocess.STDOUT,cwd=tmp_path)
        try:
            deadline=time.monotonic()+5
            while not (tmp_path/"hb.json").exists() and time.monotonic()<deadline:
                if p.poll() is not None:break
                time.sleep(.01)
            assert (tmp_path/"hb.json").exists(),(tmp_path/"output.log").read_text()
            before=json.loads((tmp_path/"hb.json").read_text());assert before["pid"]==p.pid
            if mode=="run_replaced":
                meta=json.loads((tmp_path/"run_metadata.json").read_text());meta["run_id"]="foreign";(tmp_path/"run_metadata.json").write_text(json.dumps(meta))
            p.send_signal(sig)
            if mode=="duplicate":
                time.sleep(.02)
                if p.poll() is None:p.send_signal(sig)
            code=p.wait(timeout=5)
            after=json.loads((tmp_path/"hb.json").read_text())
            if mode in ["write_failure","run_replaced"]:
                assert code!=0 and after["status"]=="alive"
            else:
                assert code==0 and after["status"]=="stopped"
                assert all(after[k]==before[k] for k in ["pid","process_start_ticks","run_id","boot_id","run_monotonic_time","source"])
        finally:
            if p.poll() is None:p.kill();p.wait()


@pytest.mark.parametrize("field,value",[("monotonic_ts",float("nan")),("monotonic_ts",True),("ts",float("inf")),("ts",False),("run_monotonic_time",None)])
def test_malformed_receipt_is_not_process_authority(stopping,field,value):
    w=stopping;data=copy.deepcopy(w.before);data[field]=value;w.hb.write_text(json.dumps(data))
    with pytest.raises(RuntimeError):w.stop()
    assert not w.sent and w.hint.exists()

@pytest.mark.parametrize("field,value",[("schema_version",True),("monotonic_time",float("nan")),("monotonic_time",False),("status","foreign")])
def test_malformed_run_metadata_refuses_stop_before_signal(stopping,field,value):
    w=stopping;meta=copy.deepcopy(w.meta);meta[field]=value;rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
    with pytest.raises(RuntimeError):w.stop()
    assert not w.sent

@pytest.mark.parametrize("target",["hb","hint"])
def test_symlink_guard_state_is_preserved_without_signal(stopping,target):
    w=stopping;p=getattr(w,target);copy=p.with_suffix(".original");p.rename(copy);p.symlink_to(copy)
    with pytest.raises(RuntimeError,match="symlink"):w.stop()
    assert p.is_symlink() and not w.sent


@pytest.mark.parametrize("name,writer,evaluate",GUARDS)
def test_exception_kill_chain_cannot_rebind_terminal_receipt_to_new_run(world,monkeypatch,name,writer,evaluate):
    m=importlib.import_module("CORE_ROOT."+name);monkeypatch.setattr(m,"ensure_runtime_layout",lambda:None);monkeypatch.setattr(m,"log",lambda message:None)
    for key in ("GUARD_HEARTBEAT_FILE","CORE_GUARD_HEARTBEAT_FILE","KERNEL_HEARTBEAT_FILE"):
        if hasattr(m,key):monkeypatch.setattr(m,key,world.hb)
    if hasattr(m,"run_quiet"):monkeypatch.setattr(m,"run_quiet",lambda *a,**k:None)
    monkeypatch.setattr(m.subprocess,"run",lambda *a,**k:None)
    identity=rc._identity(world.meta);getattr(m,writer)("alive",expected_run=identity);raw=world.hb.read_bytes()
    meta=copy.deepcopy(world.meta);meta["run_id"]="NEW_RUN";rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
    kill={"stop_gate_watcher":"activate_guard_kill_chain","core_guard":"activate_core_kill_chain","kernel_watchdog":"activate_kernel_kill_chain"}[name]
    with pytest.raises(RuntimeError,match="run identity"):getattr(m,kill)("existing exception policy",expected_run=identity)
    assert world.hb.read_bytes()==raw


@pytest.mark.parametrize("field,value",[("schema_version",True),("run_id",""),("boot_id",None),("monotonic_time",float("nan")),("monotonic_time",False),("wall_time",float("inf"))])
def test_first_writer_cannot_pin_malformed_run_metadata(world,field,value):
    meta=copy.deepcopy(world.meta);meta[field]=value;rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
    with pytest.raises(RuntimeError,match="run identity"):
        io.write_guard_heartbeat(world.hb,"core_guard",expected_run=rc._identity(meta))
    assert not world.hb.exists()
