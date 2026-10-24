"""New regressions; original historical counterexample tests remain intact."""
from pathlib import Path
import os
import subprocess
import threading
from CORE_ROOT import heartbeat_io as hb, stop_gate as gate, run_context as rc
ROOT=Path(__file__).resolve().parents[2]


def fixture_function(name,path):
    body=path.read_text().split(name+"() {\n",1)[1].split("\n}",1)[0]
    return "log() { :; }\n"+name+"() {\n"+body+"\n}\n"+name+"\n"


def test_rest_preserves_inflight_atomic_temporary_and_existing_receipt(tmp_path,monkeypatch):
    state=tmp_path/"state";state.mkdir();receipt=state/"receipt.json";receipt.write_bytes(b"old")
    monkeypatch.setattr(hb,"ensure_runtime_layout",lambda:None);monkeypatch.setattr(rc,"RUNTIME_STATE_DIR",state)
    script=tmp_path/"rest_fixture.sh";script.write_text(fixture_function("remove_stale_state_files",ROOT/"tools/rest"))
    real=hb.os.replace;protected=[]
    def replace(source,target):
        result=subprocess.run(["bash",str(script)],env={**os.environ,"HOME":str(tmp_path),"RUNTIME_STATE_DIR":str(state)},capture_output=True,text=True,timeout=5)
        assert result.returncode==0
        protected.append(Path(source).exists() and receipt.read_bytes()==b"old")
        return real(source,target)
    monkeypatch.setattr(hb.os,"replace",replace)
    hb.atomic_write_json(receipt,{"source":"synthetic","status":"alive"})
    assert protected==[True] and hb.safe_read_json(receipt)["source"]=="synthetic"


def test_work_keeps_new_receipt_and_lock_inode(tmp_path,monkeypatch):
    state=tmp_path/"state";state.mkdir();receipt=state/"receipt.json";receipt.write_bytes(b"new")
    monkeypatch.setattr(gate,"ensure_runtime_layout",lambda:None);monkeypatch.setattr(gate,"RUNTIME_STATE_DIR",state);monkeypatch.setattr(rc,"RUNTIME_STATE_DIR",state)
    script=tmp_path/"work_fixture.sh";script.write_text(fixture_function("remove_disposable_runtime_artifacts",ROOT/"tools/work"))
    with gate._transition_lock():
        inode=(state/"stop_gate_transition.lock").stat().st_ino
        result=subprocess.run(["bash",str(script)],env={**os.environ,"HOME":str(tmp_path),"RUNTIME_STATE_DIR":str(state),"LOGS_DIR":str(tmp_path/"logs")},capture_output=True,text=True,timeout=5)
        assert result.returncode==0 and receipt.read_bytes()==b"new"
        assert (state/"stop_gate_transition.lock").stat().st_ino==inode


def test_guard_pid_hint_waits_for_transition_mutation_scope(tmp_path,monkeypatch):
    state=tmp_path/"state";state.mkdir();hint=tmp_path/"guard.pid";hint.write_text("1111\n")
    monkeypatch.setattr(gate,"ensure_runtime_layout",lambda:None);monkeypatch.setattr(gate,"RUNTIME_STATE_DIR",state);monkeypatch.setattr(rc,"RUNTIME_STATE_DIR",state)
    monkeypatch.setattr(hb,"find_owned_module_process_pids",lambda module:(4242,))
    started=threading.Event();done=threading.Event()
    def writer():
        started.set();hb.write_owned_pid_hint(hint,"CORE_ROOT.stop_gate_watcher");done.set()
    with gate._transition_lock():
        thread=threading.Thread(target=writer);thread.start();assert started.wait(2)
        assert not done.wait(0.1) and hint.read_text()=="1111\n"
    thread.join(3)
    assert done.is_set() and hint.read_text()=="4242\n"


def test_nested_transition_rejected_before_second_fd_and_outer_lock_remains(tmp_path, monkeypatch):
    import pytest
    state = tmp_path / "state"
    state.mkdir()
    monkeypatch.setattr(gate, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(gate, "RUNTIME_STATE_DIR", state)
    monkeypatch.setattr(rc, "RUNTIME_STATE_DIR", state)
    with gate._transition_lock():
        first = gate._transition_local.handle.fileno()
        with pytest.raises(RuntimeError, match="not reentrant"):
            with gate._transition_lock():
                pytest.fail("second transition acquisition was allowed")
        assert gate._transition_local.handle.fileno() == first
        gate._require_transition_scope()
    with gate._transition_lock():
        gate._require_transition_scope()


def test_fork_child_cannot_borrow_parent_transition_lease(tmp_path, monkeypatch):
    import multiprocessing
    state = tmp_path / "state"
    state.mkdir()
    monkeypatch.setattr(gate, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(gate, "RUNTIME_STATE_DIR", state)
    monkeypatch.setattr(rc, "RUNTIME_STATE_DIR", state)
    context = multiprocessing.get_context("fork")
    started, acquired = context.Event(), context.Event()
    def child():
        started.set()
        with gate._transition_lock():
            gate._require_transition_scope()
            acquired.set()
    with gate._transition_lock():
        process = context.Process(target=child)
        process.start()
        assert started.wait(1)
        assert not acquired.wait(0.15)
    try:
        assert acquired.wait(2)
        process.join(2)
        assert process.exitcode == 0
    finally:
        if process.is_alive():
            process.terminate()
            process.join(2)
