from copy import deepcopy
from SUPERVISOR.runtime_preflight import classify_runtime_observation


def stopped():
    return {
        "tmux": {"available": True, "sessions": []},
        "pid_file_exists": True, "runtime_pid": 999999,
        "runtime_pid_identity": {"matches": False, "alive": False},
        "heartbeats": {scope: {"exists": True, "fresh": False, "status": "stopped", "source": source}
                       for scope, source in {"runtime": "process_supervisor", "guard": "stop_gate_watcher",
                                             "core_guard": "core_guard", "kernel_guard": "kernel_watchdog"}.items()},
        "port": {"listening": False, "owned_by_project": False}, "health": {"ok": False},
    }


def test_completed_stop_is_restartable_without_deleting_evidence():
    observed = stopped(); before = deepcopy(observed)
    result = classify_runtime_observation(observed)
    assert result["clean"] and result["classification"] == "orderly_stopped"
    assert not result["healthy"] and observed == before


def test_stopped_receipts_never_mask_foreign_process_or_ambiguous_state():
    for change in ["live_pid", "foreign_port", "missing_receipt", "wrong_source", "alive_receipt", "session", "invalid_pid"]:
        observed = stopped()
        if change == "live_pid": observed["runtime_pid_identity"]["alive"] = True
        if change == "foreign_port": observed["port"]["listening"] = True
        if change == "missing_receipt": observed["heartbeats"].pop("guard")
        if change == "wrong_source": observed["heartbeats"]["runtime"]["source"] = "foreign"
        if change == "alive_receipt": observed["heartbeats"]["runtime"]["status"] = "alive"
        if change == "session": observed["tmux"]["sessions"] = ["maksimar"]
        if change == "invalid_pid": observed["runtime_pid"] = None
        assert not classify_runtime_observation(observed)["clean"], change


# Current STOP completion is a stronger query than historical restartability.
import json
import time
import os
import fcntl
from pathlib import Path
from types import SimpleNamespace
import pytest
from SUPERVISOR import runtime_preflight as pf
from CORE_ROOT import run_context as rc


@pytest.fixture
def stop_world(tmp_path, monkeypatch):
    root=tmp_path/"MAKSIMAR_PLATFORM";state=root/"RUNTIME/state";state.mkdir(parents=True)
    monkeypatch.delenv("MAKSIMAR_STARTUP_FD",raising=False)
    for module in (pf,rc):
        monkeypatch.setattr(module,"RUNTIME_STATE_DIR",state)
        monkeypatch.setattr(module,"RUN_METADATA_FILE",state/"run_metadata.json")
    monkeypatch.setattr(pf,"ROOT",root)
    monkeypatch.setattr(pf,"RUNTIME_PID_FILE",root/"RUNTIME/runtime.pid")
    monkeypatch.setattr(rc,"_writer_pid",None)
    names=("RUNTIME_HEARTBEAT_FILE","GUARD_HEARTBEAT_FILE","CORE_GUARD_HEARTBEAT_FILE","KERNEL_HEARTBEAT_FILE")
    filenames=("heartbeat_state.json","guard_heartbeat_state.json","core_guard_heartbeat_state.json","kernel_heartbeat_state.json")
    for key,name in zip(names,filenames):monkeypatch.setattr(pf,key,state/name)
    meta={"schema_version":1,"run_id":"OFFLINE_CURRENT_RUN","boot_id":"OFFLINE_BOOT","wall_time":time.time()-20,"monotonic_time":time.monotonic()-20,"status":"shutdown"}
    pf.RUN_METADATA_FILE.write_text(json.dumps(meta))
    for i,(scope,(source,module)) in enumerate(pf.EXPECTED_HEARTBEATS.items()):
        data={"schema_version":1,"source":source,"status":"stopped","pid":900000+i,"process_start_ticks":str(100+i),"ts":time.time()-1,"monotonic_ts":time.monotonic()-1,"run_id":meta["run_id"],"boot_id":meta["boot_id"],"run_monotonic_time":meta["monotonic_time"]}
        (state/filenames[i]).write_text(json.dumps(data))
    monkeypatch.setattr(pf,"_process_identity",lambda pid,**kw:{"pid":pid,"alive":False,"matches":False})
    monkeypatch.setattr(pf,"heartbeat_process_alive",lambda *a,**k:False)
    monkeypatch.setattr(pf,"_prestart_owned_processes",lambda:{m:() for _,m in pf.EXPECTED_HEARTBEATS.values()})
    monkeypatch.setattr(pf,"_tmux_snapshot",lambda:{"available":True,"sessions":[],"error":""})
    monkeypatch.setattr(pf,"_port_snapshot",lambda:{"listening":False,"owner_pids":[],"owner_identities":[],"owned_by_project":False,"error":""})
    monkeypatch.setattr(pf,"_health_snapshot",lambda:{"ok":False,"status":None})
    return SimpleNamespace(root=root,state=state,meta=meta,expected=pf.capture_stop_run_identity())


def test_current_stop_repeated_complete_readback_preserves_all_evidence(stop_world):
    w=stop_world;before={p:p.read_bytes() for p in w.state.glob("*.json")}
    for _ in range(2):
        assert pf.verify_current_stop_completion(w.expected)=={"status":"ORDERLY_STOPPED","complete":True,"run_id":w.meta["run_id"]}
    assert all(p.read_bytes()==b for p,b in before.items())
    assert not (w.state/"preflight_result.json").exists()


@pytest.mark.parametrize("change",["missing_meta","running_meta","crashed_meta","wrong_run","wrong_boot","wrong_epoch","schema_bool","invalid_epoch","receipt_missing","receipt_alive","receipt_source","receipt_run","receipt_boot","receipt_epoch","receipt_schema","receipt_time","receipt_future","receipt_duplicate_pid","hint_mismatch","symlink","live_guard","unknown_process","session","port","lifecycle_lock","reservation_lock","mutation_lock"])
def test_current_stop_never_certifies_partial_foreign_or_unknown_state(stop_world,monkeypatch,change):
    w=stop_world;path=pf.GUARD_HEARTBEAT_FILE;receipt=json.loads(path.read_text());meta=dict(w.meta)
    if change=="missing_meta":pf.RUN_METADATA_FILE.unlink()
    elif change in {"running_meta","crashed_meta","wrong_run","wrong_boot","wrong_epoch","schema_bool","invalid_epoch"}:
        key,value={"running_meta":("status","running"),"crashed_meta":("status","crashed"),"wrong_run":("run_id","OTHER"),"wrong_boot":("boot_id","OTHER"),"wrong_epoch":("monotonic_time",meta["monotonic_time"]+1),"schema_bool":("schema_version",True),"invalid_epoch":("wall_time",float("nan"))}[change]
        meta[key]=value;pf.RUN_METADATA_FILE.write_text(json.dumps(meta))
    elif change=="receipt_missing":path.unlink()
    elif change.startswith("receipt_"):
        key,value={"receipt_alive":("status","alive"),"receipt_source":("source","foreign"),"receipt_run":("run_id","foreign"),"receipt_boot":("boot_id","foreign"),"receipt_epoch":("run_monotonic_time",0),"receipt_schema":("schema_version",True),"receipt_time":("ts",float("nan")),"receipt_future":("monotonic_ts",time.monotonic()+100),"receipt_duplicate_pid":("pid",900000)}[change]
        receipt[key]=value;path.write_text(json.dumps(receipt))
    elif change=="hint_mismatch":(w.root/"RUNTIME/guard.pid").write_text("42")
    elif change=="symlink":saved=path.with_suffix(".saved");path.rename(saved);path.symlink_to(saved)
    elif change=="live_guard":monkeypatch.setattr(pf,"_process_identity",lambda pid,**kw:{"alive":True})
    elif change=="unknown_process":monkeypatch.setattr(pf,"_prestart_owned_processes",lambda:{"guard":None})
    elif change=="session":monkeypatch.setattr(pf,"_tmux_snapshot",lambda:{"available":True,"sessions":["maksimar_guard"],"error":""})
    elif change=="port":monkeypatch.setattr(pf,"_port_snapshot",lambda:{"listening":True,"owner_pids":[42],"error":""})
    before={p:p.read_bytes() for p in w.state.iterdir() if p.is_file()}
    lock=None
    try:
        if change.endswith("_lock"):
            name={"lifecycle_lock":"run_lifecycle.lock","reservation_lock":"startup_reservation.lock","mutation_lock":"runtime_mutation.lock"}[change]
            lock=(w.state/name).open("a");fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        with pytest.raises((OSError,RuntimeError,ValueError,TypeError)):
            pf.verify_current_stop_completion(w.expected)
    finally:
        if lock is not None:lock.close()
    assert all(p.read_bytes()==b for p,b in before.items())


@pytest.mark.parametrize("query",["capture","verify","malformed","conflicting"])
def test_stop_query_cli_never_writes_preflight_or_reconciles(stop_world,monkeypatch,capsys,query):
    import sys
    def forbidden(*a,**k):raise AssertionError("stop query attempted state/report/reconciliation mutation")
    for name in ("ensure_runtime_layout","prepare_clean_start","write_report","run_preflight","log"):monkeypatch.setattr(pf,name,forbidden)
    argv={"capture":["--capture-stop-run"],"verify":["--verify-current-stop",json.dumps(stop_world.expected)],"malformed":["--verify-current-stop","{"],"conflicting":["--capture-stop-run","--prepare-clean-start"]}[query]
    monkeypatch.setattr(sys,"argv",["preflight",*argv])
    if query in {"malformed","conflicting"}:
        with pytest.raises(SystemExit) as exc:pf.main()
        assert exc.value.code in (1,2)
    else:
        pf.main();d=json.loads(capsys.readouterr().out)
        assert d.get("run_id")==stop_world.meta["run_id"]


def test_current_stop_rejects_receipt_or_metadata_change_during_readback(stop_world,monkeypatch):
    original=pf.inspect_runtime_state;calls=[]
    def changing():
        result=original();calls.append(1)
        if len(calls)==1:
            p=pf.CORE_GUARD_HEARTBEAT_FILE;d=json.loads(p.read_text());d["run_id"]="OTHER";p.write_text(json.dumps(d))
        return result
    monkeypatch.setattr(pf,"inspect_runtime_state",changing)
    with pytest.raises(RuntimeError):pf.verify_current_stop_completion(stop_world.expected)
