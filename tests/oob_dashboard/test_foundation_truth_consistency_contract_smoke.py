from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_contract import (
    build_foundation_truth_consistency_contract,
)


def test_foundation_truth_consistency_contract_counts() -> None:
    """Truth consistency contract should expose expected counts."""
    contract = build_foundation_truth_consistency_contract()

    assert contract.total_entries == 4
    assert contract.consistent_entries == 4
    assert contract.mismatch_entries == 0
    assert contract.partial_entries == 0
    assert contract.unknown_entries == 0


def test_foundation_truth_consistency_contract_runtime_entry() -> None:
    """Truth consistency contract should expose runtime entry."""
    contract = build_foundation_truth_consistency_contract()
    entry = contract.entries[0]

    assert entry.consistency_entry_id == "foundationconsistency_runtime_001"
    assert entry.component_id == "foundation_runtime_component_001"
    assert entry.truth_scope == "runtime"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is True
    assert entry.log_truth is True
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "CONSISTENT"


def test_foundation_truth_consistency_contract_kernel_entry() -> None:
    """Truth consistency contract should expose kernel entry."""
    contract = build_foundation_truth_consistency_contract()
    entry = contract.entries[-1]

    assert entry.consistency_entry_id == "foundationconsistency_kernel_guard_001"
    assert entry.component_id == "foundation_kernel_guard_component_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is False
    assert entry.log_truth is True
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "CONSISTENT"


def test_foundation_truth_consistency_contract_scope_order() -> None:
    """Truth consistency contract should preserve canonical scope order."""
    contract = build_foundation_truth_consistency_contract()

    assert [entry.truth_scope for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]

import pytest


@pytest.fixture(autouse=True)
def observed_foundation_fixture(monkeypatch):
    return _observed_foundation_fixture(monkeypatch)


@pytest.mark.parametrize("defect", ["stale", "missing", "process_missing", "foreign_source", "api_unavailable"])
def test_observed_consistency_rejects_false_alive_and_fresh(observed_foundation_fixture, defect):
    state = observed_foundation_fixture
    heartbeat = state["heartbeats"]["runtime"]
    if defect == "stale":
        heartbeat["fresh"] = False
    elif defect == "missing":
        heartbeat.update(exists=False, fresh=False, source=None, status=None)
        state["processes"]["runtime"] = False
    elif defect == "process_missing":
        state["processes"]["runtime"] = False
    elif defect == "foreign_source":
        heartbeat["source"] = "foreign_runtime"
    else:
        state["runtime_api"] = False
    entry = build_foundation_truth_consistency_contract().entries[0]
    assert entry.derived_status != "ALIVE"
    if defect in {"stale", "missing", "foreign_source"}:
        assert entry.heartbeat_truth is False
        assert entry.last_seen_label != "fresh"
    if defect == "process_missing":
        assert entry.process_truth is False
    if defect == "api_unavailable":
        assert entry.api_truth is False


def test_missing_explicit_observation_is_unknown_through_views_and_panels():
    from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view import build_foundation_truth_consistency_view
    from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view import build_foundation_guard_chain_truth_view
    contract = build_foundation_truth_consistency_contract(observation={})
    assert all(entry.derived_status == "UNKNOWN" for entry in contract.entries)
    view = build_foundation_truth_consistency_view(observation={})
    assert all(entry.derived_status == "UNKNOWN" for entry in view.entries)
    guard = build_foundation_guard_chain_truth_view(observation={})
    assert all(entry.derived_status == "UNKNOWN" for entry in guard.entries)


def test_stale_explicit_observation_never_projects_alive(observed_foundation_fixture):
    state = observed_foundation_fixture
    for heartbeat in state["heartbeats"].values():
        heartbeat.update(fresh=False, age_seconds=100)
    contract = build_foundation_truth_consistency_contract(observation=state)
    assert all(entry.derived_status == "UNKNOWN" for entry in contract.entries)
    assert all(entry.last_seen_label == "stale" for entry in contract.entries)


def test_server_collects_foundation_facts_from_existing_owners(monkeypatch, tmp_path):
    from CORE_ROOT import heartbeat_io, runtime_paths
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as models
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
    calls = []
    monkeypatch.setattr(obs, "observe_runtime_preflight", lambda: {
        "tmux": {"sessions": []}, "heartbeats": {},
        "health": {"ok": True}, "port": {"owned_by_project": False},
    })
    monkeypatch.setattr(heartbeat_io, "safe_read_json", lambda path: calls.append(path) or {"fixture": True})
    monkeypatch.setattr(heartbeat_io, "heartbeat_process_alive", lambda payload, module: False)
    for name in ("RUNTIME_LOG_FILE", "GUARD_LOG_FILE", "CORE_GUARD_LOG_FILE", "KERNEL_GUARD_LOG_FILE"):
        monkeypatch.setattr(runtime_paths, name, tmp_path / name)
    observation = models.observe_foundation_consistency()
    assert calls == []  # Never reread heartbeats after canonical preflight.
    assert observation["runtime_api"] is False  # Unowned API success is not truth.
    assert not any(observation["processes"].values())
    assert all(entry.derived_status == "UNKNOWN" for entry in
               build_foundation_truth_consistency_contract(observation).entries)


def _observed_foundation_fixture(monkeypatch):
    from tests.runtime.test_preflight_recovery_truth import _observation
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as models
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
    from MAKSIMAR_CORE_LIB.oob_dashboard import foundation_truth_consistency_contract as contract
    snapshot = _observation()
    monkeypatch.setattr(obs, "observe_runtime_preflight", lambda: snapshot)
    observation = models.observe_foundation_consistency()
    # Retained log presence is a known synthetic fixture fact, never fabricated by production.
    observation["logs"] = {scope: True for scope in observation["heartbeats"]}
    monkeypatch.setattr(contract, "_observe_foundation_consistency", lambda: observation)
    return observation


@pytest.mark.parametrize("field", ["fresh", "exists", "processes", "sessions", "runtime_api", "logs"])
@pytest.mark.parametrize("bad", ["false", "0", 1, 0, [], None, {}])
def test_truth_never_coerces_untyped_values(observed_foundation_fixture, field, bad):
    import copy
    state = copy.deepcopy(observed_foundation_fixture)
    if field in {"fresh", "exists"}:
        state["heartbeats"]["runtime"][field] = bad
    elif field == "runtime_api":
        state[field] = bad
    else:
        state[field]["runtime"] = bad
    entry = build_foundation_truth_consistency_contract(state).entries[0]
    attr = {"fresh": "heartbeat_truth", "exists": "heartbeat_truth", "processes": "process_truth",
            "sessions": "session_truth", "runtime_api": "api_truth", "logs": "log_truth"}[field]
    assert getattr(entry, attr) is None
    if field != "logs":  # Retained log presence is explicitly not current health.
        assert entry.derived_status != "ALIVE"
        assert entry.consistency_status != "CONSISTENT"


@pytest.mark.parametrize("bad", [None, [], "false", 1, {}, {"heartbeats": []}, {"heartbeats": {"guard": 1}}])
def test_malformed_observation_has_no_healthy_default(monkeypatch, bad):
    from MAKSIMAR_CORE_LIB.oob_dashboard import foundation_truth_consistency_contract as module
    monkeypatch.setattr(module, "_observe_foundation_consistency", lambda: {})
    out = module.build_foundation_truth_consistency_contract(bad)
    assert out.total_entries == 4
    assert all(row.derived_status != "ALIVE" and row.consistency_status != "CONSISTENT" for row in out.entries)
    assert any(row.process_truth is None for row in out.entries)


@pytest.mark.parametrize("defect", ["run_id", "boot_id", "epoch", "start_ticks", "foreign_cwd", "stale", "missing_guard", "api_foreign", "history", "forged_decision"])
def test_canonical_producer_uses_one_snapshot_and_real_epoch_classifier(monkeypatch, defect):
    import copy
    from tests.runtime.test_preflight_recovery_truth import _observation
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as models
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
    from CORE_ROOT import heartbeat_io
    snapshot = _observation()
    heartbeat = snapshot["heartbeats"]["guard"]
    if defect in {"run_id", "boot_id"}:
        heartbeat[defect] = "other-run"
    elif defect == "epoch":
        heartbeat["run_monotonic_time"] -= 1
    elif defect == "start_ticks":
        heartbeat["identity"]["process_start_ticks"] = "999999"
    elif defect == "foreign_cwd":
        heartbeat["identity"]["cwd"] = "/foreign/project"
    elif defect == "stale":
        heartbeat["fresh"] = False
    elif defect == "missing_guard":
        snapshot["heartbeats"].pop("guard")
    elif defect == "api_foreign":
        snapshot["port"]["owned_by_project"] = False
    elif defect == "history":
        snapshot["run_metadata"]["status"] = "shutdown"
    else:
        heartbeat["run_id"] = "other-run"
        snapshot["decision"] = {"healthy": True, "heartbeat_chain_valid": True}
    before = copy.deepcopy(snapshot)
    calls = []
    monkeypatch.setattr(obs, "observe_runtime_preflight", lambda: calls.append("snapshot") or snapshot)
    def forbidden(*args, **kwargs):
        raise AssertionError("Dashboard must not reread physical heartbeats")
    monkeypatch.setattr(heartbeat_io, "safe_read_json", forbidden)
    monkeypatch.setattr(heartbeat_io, "heartbeat_process_alive", forbidden)
    out = models.observe_foundation_consistency()
    assert calls == ["snapshot"]
    assert snapshot == before
    assert out["canonical_decision"]["healthy"] is False
    contract = build_foundation_truth_consistency_contract(out)
    assert not all(row.derived_status == "ALIVE" and row.consistency_status == "CONSISTENT" for row in contract.entries)
    if defect != "api_foreign":
        assert out["epoch_verified"] is False
        assert all(row.derived_status != "ALIVE" for row in contract.entries)


def test_unknown_and_verified_false_remain_distinct(observed_foundation_fixture):
    import copy
    missing = copy.deepcopy(observed_foundation_fixture)
    missing["processes"]["guard"] = None
    stopped = copy.deepcopy(observed_foundation_fixture)
    stopped["processes"]["guard"] = False
    a = build_foundation_truth_consistency_contract(missing).entries[1]
    b = build_foundation_truth_consistency_contract(stopped).entries[1]
    assert a.process_truth is None and a.derived_status == "UNKNOWN"
    assert b.process_truth is False and b.derived_status == "DEAD"
