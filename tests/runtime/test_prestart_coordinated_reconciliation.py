"""Actual prestart owner, isolated files/providers; no real services/models."""
import copy
import json
import multiprocessing
import os
from pathlib import Path
import signal
import threading
import time
from types import SimpleNamespace
import pytest
from CORE_ROOT import run_context as rc, heartbeat_io as hb, stop_gate as gate, incident_history as history, runtime_paths as rp
from SUPERVISOR import runtime_preflight as pf


@pytest.fixture
def world(tmp_path, monkeypatch):
    root=tmp_path/"MAKSIMAR_PLATFORM"; state=root/"RUNTIME/state"; state.mkdir(parents=True)
    monkeypatch.delenv("MAKSIMAR_STARTUP_FD",raising=False)
    for mod in (rc,gate): monkeypatch.setattr(mod,"RUNTIME_STATE_DIR",state)
    for mod in (rc,hb,gate,history,pf): monkeypatch.setattr(mod,"ensure_runtime_layout",lambda:None)
    monkeypatch.setattr(rc,"RUN_METADATA_FILE",state/"run_metadata.json")
    monkeypatch.setattr(hb,"ROOT",root);monkeypatch.setattr(pf,"ROOT",root)
    monkeypatch.setattr(pf,"RUNTIME_STATE_DIR",state);monkeypatch.setattr(pf,"RUN_METADATA_FILE",rc.RUN_METADATA_FILE)
    monkeypatch.setattr(pf,"PREFLIGHT_RESULT_FILE",state/"preflight_result.json")
    monkeypatch.setattr(rp,"DIAGNOSTICS_DB_FILE",state/"diagnostics_db.json")
    monkeypatch.setattr(pf,"RUNTIME_PID_FILE",root/"RUNTIME/runtime.pid")
    names={"RUNTIME_HEARTBEAT_FILE":"heartbeat_state.json","GUARD_HEARTBEAT_FILE":"guard_heartbeat_state.json","CORE_GUARD_HEARTBEAT_FILE":"core_guard_heartbeat_state.json","KERNEL_HEARTBEAT_FILE":"kernel_heartbeat_state.json"}
    for attr,name in names.items():monkeypatch.setattr(pf,attr,state/name)
    for attr,name in {"DEGRADED_MODE_FILE":"degraded_mode.flag","STOP_GATE_TRIGGER_FILE":"stop_gate_trigger.txt","LAST_DEGRADED_REASON_FILE":"last_degraded_reason.txt","INCIDENT_HISTORY_FILE":"incident_history.jsonl","INCIDENT_SNAPSHOT_FILE":"last_incident_snapshot.json"}.items():
        monkeypatch.setattr(rp,attr,state/name)
        if hasattr(gate,attr):monkeypatch.setattr(gate,attr,state/name)
    monkeypatch.setattr(history,"INCIDENT_HISTORY_FILE",rp.INCIDENT_HISTORY_FILE)
    original_append=history.write_incident_record
    monkeypatch.setattr(history,"write_incident_record",lambda *a,**k:pytest.fail("false recovery incident"))
    monkeypatch.setattr(gate,"log",lambda _:None)
    tmux={"available":True,"sessions":[],"error":""}
    port={"listening":False,"owned_by_project":False,"owner_pids":[],"owner_identities":[],"error":""}
    process={"alive":False};owned={"canonical":()}
    monkeypatch.setattr(pf,"_tmux_snapshot",lambda:copy.deepcopy(tmux))
    monkeypatch.setattr(pf,"_port_snapshot",lambda:copy.deepcopy(port))
    monkeypatch.setattr(pf,"_health_snapshot",lambda:{"ok":False,"status":None})
    monkeypatch.setattr(pf,"_process_identity",lambda pid,**k:{"pid":pid,"matches":False,**process})
    monkeypatch.setattr(pf,"heartbeat_process_alive",lambda *a,**k:False)
    monkeypatch.setattr(pf,"_prestart_owned_processes",lambda:copy.deepcopy(owned))
    for index,(scope,(hint,receipt)) in enumerate(pf._prestart_receipt_paths().items()):
        pid=910001+index;hint.write_text(str(pid)+"\n")
        receipt.write_text(json.dumps({"schema_version":1,"pid":pid,"process_start_ticks":str(10000+index),"source":pf.EXPECTED_HEARTBEATS[scope][0],"status":"alive","ts":time.time()-100,"monotonic_ts":max(0,time.monotonic()-100)}))
    for name in ["degraded_mode.flag","stop_gate_trigger.txt","last_degraded_reason.txt","incident_history.jsonl"]:(state/name).write_bytes(("retain:"+name).encode())
    original={p:p.read_bytes() for pair in pf._prestart_receipt_paths().values() for p in pair}
    protected={state/n:(state/n).read_bytes() for n in ["degraded_mode.flag","stop_gate_trigger.txt","last_degraded_reason.txt","incident_history.jsonl"]}
    return SimpleNamespace(root=root,state=state,original=original,protected=protected,process=process,owned=owned,port=port,tmux=tmux,append=original_append)


def intact(w):
    assert all(p.read_bytes()==data for p,data in w.original.items())
    assert all(p.read_bytes()==data for p,data in w.protected.items())
    assert not rc.RUN_METADATA_FILE.exists()


def test_archive_reconcile_repeat_preserves_all_markers_and_never_claims_healthy(world):
    result=pf.prepare_clean_start()
    assert result["status"]=="RECONCILED" and result["healthy"] is False,result
    assert all(not p.exists() for p in world.original)
    assert all(p.read_bytes()==data for p,data in world.protected.items())
    entries={n["origin"]:n for n in json.loads((Path(result["archive_path"])/"manifest.json").read_text())["originals"]}
    for p,data in {**world.original,**world.protected}.items():assert (Path(result["archive_path"])/entries[str(p)]["archive_file"]).read_bytes()==data
    verdict=pf.inspect_runtime_state()["decision"]
    assert verdict["clean"] and not verdict["healthy"]
    inode=(world.state/"run_lifecycle.lock").stat().st_ino
    again=pf.prepare_clean_start()
    assert again["status"]=="CLEAN" and again["reconciled"] is False
    assert (world.state/"run_lifecycle.lock").stat().st_ino==inode
    assert len(list((world.state/"incident_evidence").iterdir()))==1
    assert not rc.RUN_METADATA_FILE.exists()


@pytest.mark.parametrize("bad",["live","foreign","reused","unreadable","owned","unknown_owned","port","unknown_port","session","unknown_tmux","hint","source","epoch","missing","corrupt","fresh","missing_ticks","missing_clock","metadata","symlink"])
def test_unknown_current_or_incomplete_evidence_holds_without_reconciliation(world,bad):
    receipt=pf.GUARD_HEARTBEAT_FILE
    payload=json.loads(receipt.read_text())
    if bad in {"live","foreign","reused","unreadable"}:world.process.update(alive=None if bad=="unreadable" else True,process_start_ticks="reused")
    elif bad in {"owned","unknown_owned"}:world.owned["canonical"]=None if bad=="unknown_owned" else (1234,)
    elif bad=="port":world.port.update(listening=True,owner_pids=[1234])
    elif bad=="unknown_port":world.port["error"]="unreadable"
    elif bad=="session":world.tmux["sessions"]=["foreign_session"]
    elif bad=="unknown_tmux":world.tmux["available"]=False
    elif bad=="hint":(world.root/"RUNTIME/guard.pid").write_text("5555\n")
    elif bad=="source":payload["source"]="foreign"
    elif bad=="epoch":payload["run_id"]="different"
    elif bad=="missing":receipt.unlink()
    elif bad=="corrupt":receipt.write_bytes(b"invalid JSON")
    elif bad=="fresh":payload["ts"]=time.time()
    elif bad=="missing_ticks":payload.pop("process_start_ticks")
    elif bad=="missing_clock":payload.pop("monotonic_ts")
    elif bad=="metadata":rc.RUN_METADATA_FILE.write_bytes(b"corrupt")
    elif bad=="symlink":receipt.unlink();receipt.symlink_to(world.state/"missing")
    if bad in {"source","epoch","fresh","missing_ticks","missing_clock"}:receipt.write_text(json.dumps(payload))
    before={p:p.read_bytes() for p in world.original if p.is_file()}
    result=pf.prepare_clean_start()
    assert result["status"]=="HOLD",result
    assert all(p.read_bytes()==data for p,data in before.items())
    assert not (world.state/"incident_evidence").exists()
    assert all(p.read_bytes()==data for p,data in world.protected.items())


@pytest.mark.parametrize("kind",["write","readback","before_interrupt","changed_inode"])
def test_archive_failure_interruption_or_source_change_never_authorizes_effect(world,monkeypatch,kind):
    real=history.preserve_runtime_evidence
    if kind=="write":monkeypatch.setattr(history,"preserve_runtime_evidence",lambda *a,**k:(_ for _ in ()).throw(OSError("archive failure")))
    elif kind=="readback":monkeypatch.setattr(history,"_verify_runtime_evidence_archive",lambda *a:(_ for _ in ()).throw(RuntimeError("readback mismatch")))
    elif kind=="before_interrupt":monkeypatch.setattr(history,"preserve_runtime_evidence",lambda *a,**k:(_ for _ in ()).throw(KeyboardInterrupt()))
    else:
        def change(*a,**k):
            result=real(*a,**k);p=pf.GUARD_HEARTBEAT_FILE;replacement=world.state/"replacement";replacement.write_bytes(p.read_bytes());replacement.replace(p);return result
        monkeypatch.setattr(history,"preserve_runtime_evidence",change)
    if kind=="before_interrupt":
        with pytest.raises(KeyboardInterrupt):pf.prepare_clean_start()
    else:assert pf.prepare_clean_start()["status"]=="HOLD"
    intact(world)


@pytest.mark.parametrize("interrupted",[False,True])
def test_partial_effect_restores_missing_originals_under_coordination(world,monkeypatch,interrupted):
    real=Path.unlink;count=[]
    def unlink(path,*a,**k):
        if path in world.original:
            count.append(path)
            if len(count)==2:
                if interrupted:raise KeyboardInterrupt()
                raise OSError("effect interruption")
        return real(path,*a,**k)
    monkeypatch.setattr(Path,"unlink",unlink)
    if interrupted:
        with pytest.raises(KeyboardInterrupt):pf.prepare_clean_start()
    else:assert pf.prepare_clean_start()["status"]=="HOLD"
    intact(world)


def test_other_thread_mutation_refuses_prestart_without_wait_or_effect(world):
    acquired=threading.Event();release=threading.Event()
    def writer():
        with rc.runtime_mutation():acquired.set();release.wait(3)
    t=threading.Thread(target=writer);t.start();assert acquired.wait(2)
    try:assert pf.prepare_clean_start()["status"]=="HOLD"
    finally:release.set();t.join(3)
    intact(world)


@pytest.mark.parametrize("worker",["heartbeat","stopgate","supervisor"])
def test_cross_process_start_writer_and_stopgate_exclusion(world,worker):
    ctx=multiprocessing.get_context("fork");started=ctx.Event();finished=ctx.Event();status=ctx.Queue()
    def child():
        started.set()
        try:
            if worker=="heartbeat":hb.atomic_write_json(world.state/"new_receipt.json",{"status":"alive"})
            elif worker=="stopgate":
                with gate._transition_lock():(world.state/"new_marker").write_text("synthetic")
            else:
                hb.heartbeat_process_alive=lambda *a,**k:True
                hb._process_start_ticks=lambda _:"1234"
                with rc.run_lifecycle():pass
            status.put("DONE")
        except (BlockingIOError,RuntimeError):status.put("HOLD")
        finally:finished.set()
    with rc.prestart_mutation():
        process=ctx.Process(target=child);process.start();assert started.wait(2)
        if worker=="supervisor":assert finished.wait(2) and status.get(timeout=1)=="HOLD"
        else:assert not finished.wait(0.1)
        assert not (world.state/"new_receipt.json").exists() and not (world.state/"new_marker").exists()
    assert finished.wait(3);process.join(3);assert process.exitcode==0
    if worker!="supervisor":assert status.get(timeout=1)=="DONE"
    intact(world)


def test_preflight_cli_calls_reconciliation_before_clean_evaluation(world,monkeypatch):
    import sys
    def report():
        observation=pf.inspect_runtime_state();d=observation["decision"]
        return pf.PreflightReport(preflight_id="synthetic",checked_at="synthetic",ok=d["clean"],stale_tmux_found=False,stale_pid_found=False,stale_heartbeat_found=False,port_conflict_found=False,previous_crash_found=False,already_running_healthy=False,details={"runtime_state":d})
    saved=[]
    monkeypatch.setattr(pf,"run_preflight",report);monkeypatch.setattr(pf,"write_report",saved.append);monkeypatch.setattr(pf,"log",lambda _:None)
    monkeypatch.setattr(sys,"argv",["preflight","--prepare-clean-start"])
    pf.main()
    assert saved[0].ok and saved[0].details["prestart_reconciliation"]["status"]=="RECONCILED"
    assert not pf.inspect_runtime_state()["decision"]["healthy"]


def test_empty_clean_start_does_not_need_previous_metadata(world):
    for p in world.original:p.unlink()
    result=pf.prepare_clean_start()
    assert result["status"]=="CLEAN" and not result["reconciled"]
    assert not rc.RUN_METADATA_FILE.exists()
    assert not pf.inspect_runtime_state()["decision"]["healthy"]


def test_historical_matching_metadata_is_archived_and_left_in_place(world):
    meta={"schema_version":1,"run_id":"historical","boot_id":"historical-boot","monotonic_time":10.0,"wall_time":time.time()-200,"status":"crashed"}
    rc.RUN_METADATA_FILE.write_text(json.dumps(meta));before=rc.RUN_METADATA_FILE.read_bytes()
    for _,receipt in pf._prestart_receipt_paths().values():
        value=json.loads(receipt.read_text());value.update(run_id="historical",boot_id="historical-boot",run_monotonic_time=10.0);receipt.write_text(json.dumps(value))
    result=pf.prepare_clean_start()
    assert result["status"]=="RECONCILED",result
    assert rc.RUN_METADATA_FILE.read_bytes()==before
    assert not pf.inspect_runtime_state()["decision"]["healthy"]


def test_stopgate_then_incident_append_is_reentrant_without_lock_inversion(world):
    with gate._transition_lock():
        value=world.append("synthetic observation",status="observed")
        assert value["status"]=="observed"
    assert world.protected[rp.INCIDENT_HISTORY_FILE] in rp.INCIDENT_HISTORY_FILE.read_bytes()
    assert b'"status": "recovered"' not in rp.INCIDENT_HISTORY_FILE.read_bytes()


def test_changed_content_after_archive_is_retained_not_overwritten(world,monkeypatch):
    real=history.preserve_runtime_evidence;changed=[]
    def archive(*a,**k):
        result=real(*a,**k);p=pf.GUARD_HEARTBEAT_FILE;data=json.loads(p.read_text());data["new_writer_field"]=True;p.write_text(json.dumps(data));changed.append(p.read_bytes());return result
    monkeypatch.setattr(history,"preserve_runtime_evidence",archive)
    assert pf.prepare_clean_start()["status"]=="HOLD"
    assert pf.GUARD_HEARTBEAT_FILE.read_bytes()==changed[0]
    assert all(p.exists() for p in world.original)


def test_other_startup_reservation_refuses_reconciliation(world):
    import fcntl
    with (world.state/"startup_reservation.lock").open("a") as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        assert pf.prepare_clean_start()["status"]=="HOLD"
    intact(world)


def test_borrowed_wrong_inode_startup_descriptor_refuses(world,monkeypatch):
    wrong=world.state/"wrong.lock"
    with wrong.open("a") as descriptor:
        (world.state/"startup_reservation.lock").touch()
        monkeypatch.setenv("MAKSIMAR_STARTUP_FD",str(descriptor.fileno()))
        assert pf.prepare_clean_start()["status"]=="HOLD"
    intact(world)


def test_default_preflight_cli_does_not_run_reconciliation(world,monkeypatch):
    import sys
    monkeypatch.setattr(pf,"prepare_clean_start",lambda:pytest.fail("read-only default invoked reconciliation"))
    value=pf.PreflightReport(preflight_id="synthetic",checked_at="synthetic",ok=False,stale_tmux_found=False,stale_pid_found=True,stale_heartbeat_found=True,port_conflict_found=False,previous_crash_found=True,already_running_healthy=False,details={"runtime_state":{"classification":"stale_runtime_state"}})
    monkeypatch.setattr(pf,"run_preflight",lambda:value);monkeypatch.setattr(pf,"write_report",lambda _:None);monkeypatch.setattr(pf,"log",lambda _:None);monkeypatch.setattr(sys,"argv",["preflight"])
    with pytest.raises(SystemExit) as error:pf.main()
    assert error.value.code==1
    intact(world)


@pytest.mark.parametrize("competing",["process","port"])
def test_new_owner_before_later_effect_rolls_back_all_removed_originals(world,monkeypatch,competing):
    real=Path.unlink;changed=[]
    def unlink(path,*a,**k):
        result=real(path,*a,**k)
        if path in world.original and not changed:
            changed.append(True)
            if competing=="process":world.process["alive"]=True
            else:world.port["listening"]=True
        return result
    monkeypatch.setattr(Path,"unlink",unlink)
    assert pf.prepare_clean_start()["status"]=="HOLD"
    intact(world)


def test_status_metadata_originals_are_archived_before_any_overwrite(world):
    status=pf.PREFLIGHT_RESULT_FILE;readiness=world.state/"model_readiness.json"
    status.write_bytes(b"old preflight metadata");readiness.write_bytes(b"old readiness metadata")
    result=pf.prepare_clean_start()
    assert result["status"]=="RECONCILED",result
    manifest=json.loads((Path(result["archive_path"])/"manifest.json").read_text());entries={x["origin"]:x for x in manifest["originals"]}
    for p in [status,readiness]:
        assert (Path(result["archive_path"])/entries[str(p)]["archive_file"]).read_bytes()==p.read_bytes()


@pytest.mark.parametrize("suffix",["", "\n"])
def test_same_pid_hint_preserves_mtime_even_without_newline(world,monkeypatch,suffix):
    hint=world.root/"RUNTIME/guard.pid";hint.write_text("4242"+suffix);before=hint.stat().st_mtime_ns
    monkeypatch.setattr(hb,"find_owned_module_process_pids",lambda module:(4242,))
    hb.write_owned_pid_hint(hint,"CORE_ROOT.stop_gate_watcher")
    assert hint.stat().st_mtime_ns==before and hint.read_text()=="4242"+suffix


def test_metadata_only_repeat_reuses_verified_raw_archive(world):
    for p in world.original:p.unlink()
    rc.RUN_METADATA_FILE.write_text(json.dumps({"schema_version":1,"run_id":"old","boot_id":"old-boot","status":"shutdown","wall_time":time.time()-100,"monotonic_time":1.0}))
    first=pf.prepare_clean_start();second=pf.prepare_clean_start()
    assert first["status"]==second["status"]=="CLEAN"
    assert first["archive_path"]==second["archive_path"]
    assert len(list((world.state/"incident_evidence").iterdir()))==1


@pytest.mark.parametrize("bad",["permissions","status","epoch"])
def test_untrusted_or_invalid_historical_metadata_refuses(world,bad):
    if bad=="permissions":pf.GUARD_HEARTBEAT_FILE.chmod(0o666)
    else:
        meta={"schema_version":1,"run_id":"old","boot_id":"old-boot","status":"wrong" if bad=="status" else "crashed","wall_time":time.time()-200,"monotonic_time":time.monotonic()+100 if bad=="epoch" else 1.0}
        rc.RUN_METADATA_FILE.write_text(json.dumps(meta))
        for _,receipt in pf._prestart_receipt_paths().values():
            v=json.loads(receipt.read_text());v.update(run_id=meta["run_id"],boot_id=meta["boot_id"],run_monotonic_time=meta["monotonic_time"]);receipt.write_text(json.dumps(v))
    before={p:p.read_bytes() for p in world.original}
    assert pf.prepare_clean_start()["status"]=="HOLD"
    assert all(p.read_bytes()==data for p,data in before.items())
    assert not (world.state/"incident_evidence").exists()


def test_reconciled_metadata_reuses_larger_verified_archive(world):
    test_historical_matching_metadata_is_archived_and_left_in_place(world)
    before=list((world.state/"incident_evidence").iterdir())
    assert pf.prepare_clean_start()["status"]=="CLEAN"
    assert list((world.state/"incident_evidence").iterdir())==before


def test_clean_status_metadata_is_preserved_before_preflight_report(world):
    for p in world.original:p.unlink()
    pf.PREFLIGHT_RESULT_FILE.write_bytes(b"old status bytes")
    result=pf.prepare_clean_start();assert result["status"]=="CLEAN"
    manifest=json.loads((Path(result["archive_path"])/"manifest.json").read_text())
    entry=next(x for x in manifest["originals"] if x["origin"]==str(pf.PREFLIGHT_RESULT_FILE))
    assert (Path(result["archive_path"])/entry["archive_file"]).read_bytes()==b"old status bytes"


def test_failed_preparation_does_not_overwrite_original_status(world,monkeypatch):
    import sys
    pf.PREFLIGHT_RESULT_FILE.write_bytes(b"original failed diagnostic")
    world.process["alive"]=True
    value=pf.PreflightReport(preflight_id="synthetic",checked_at="synthetic",ok=True,stale_tmux_found=False,stale_pid_found=False,stale_heartbeat_found=False,port_conflict_found=False,previous_crash_found=False,already_running_healthy=False,details={})
    monkeypatch.setattr(pf,"run_preflight",lambda:value);monkeypatch.setattr(pf,"write_report",lambda _:pytest.fail("HOLD overwrote diagnostics"));monkeypatch.setattr(pf,"log",lambda _:None);monkeypatch.setattr(sys,"argv",["preflight","--prepare-clean-start"])
    with pytest.raises(SystemExit) as error:pf.main()
    assert error.value.code==1 and pf.PREFLIGHT_RESULT_FILE.read_bytes()==b"original failed diagnostic"
    intact(world)
