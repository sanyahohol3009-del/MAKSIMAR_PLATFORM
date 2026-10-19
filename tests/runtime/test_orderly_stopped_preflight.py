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
