from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_canonical_status_model import (
    build_foundation_canonical_status_model,
)


FoundationTruthScope = Literal[
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
]

FoundationConsistencyStatus = Literal[
    "CONSISTENT",
    "MISMATCH",
    "PARTIAL",
    "UNKNOWN",
]

FoundationCanonicalStatus = Literal[
    "WARMING_UP",
    "ALIVE",
    "DEGRADED",
    "DEAD",
    "BROKEN",
    "UNKNOWN",
]


@dataclass(frozen=True)
class FoundationTruthConsistencyEntry:
    """Canonical truth consistency entry for a foundation component."""

    consistency_entry_id: str
    component_id: str
    truth_scope: FoundationTruthScope
    heartbeat_truth: bool | None
    process_truth: bool | None
    session_truth: bool | None
    api_truth: bool | None
    log_truth: bool | None
    derived_status: FoundationCanonicalStatus
    consistency_status: FoundationConsistencyStatus
    description: str
    last_seen_label: str = "unknown"


@dataclass(frozen=True)
class FoundationTruthConsistencyContract:
    """Canonical truth consistency contract for foundation dashboard hardening."""

    total_entries: int
    consistent_entries: int
    mismatch_entries: int
    partial_entries: int
    unknown_entries: int
    entries: tuple[FoundationTruthConsistencyEntry, ...]


def _validate_status(status: str) -> FoundationCanonicalStatus:
    """Validate canonical status against the canonical status model."""
    allowed = {entry.status for entry in build_foundation_canonical_status_model().entries}
    if status not in allowed:
        raise ValueError(f"unsupported canonical status: {status}")
    return status  # type: ignore[return-value]


def _derive_consistency_status(
    *, heartbeat_truth: bool | None, process_truth: bool | None,
    session_truth: bool | None, api_truth: bool | None, log_truth: bool | None,
    api_required: bool = True,
) -> FoundationConsistencyStatus:
    """Project applicable current-health facts; retained log presence is not health."""
    values = (heartbeat_truth, process_truth, session_truth)
    if api_required:
        values += (api_truth,)
    if any(type(value) is not bool for value in values):
        return "UNKNOWN"
    if all(value is True for value in values):
        return "CONSISTENT"
    if all(value is False for value in values):
        return "UNKNOWN"
    return "PARTIAL" if sum(value is True for value in values) >= 2 else "MISMATCH"


def _observe_foundation_consistency() -> dict:
    """Unobserved compatibility default; only the server acquires runtime facts."""
    return {}


def build_foundation_truth_consistency_contract(observation: dict | None = None) -> FoundationTruthConsistencyContract:
    """Pure projection of one server-owned canonical observation; never probes."""
    supplied = _observe_foundation_consistency() if observation is None else observation
    observation = supplied if isinstance(supplied, dict) else {}
    def mapping(value):
        return value if isinstance(value, dict) else {}
    def truth(value):
        return value if type(value) is bool else None
    heartbeats = mapping(observation.get("heartbeats"))
    processes = mapping(observation.get("processes"))
    sessions = mapping(observation.get("sessions"))
    logs = mapping(observation.get("logs"))
    meta = mapping(observation.get("run_metadata"))
    decision = mapping(observation.get("canonical_decision"))
    epoch_verified = (observation.get("epoch_verified") is True
                      and decision.get("heartbeat_chain_valid") is True)
    sources = {
        "runtime": "process_supervisor", "guard": "stop_gate_watcher",
        "core_guard": "core_guard", "kernel_guard": "kernel_watchdog",
    }
    entries = []
    for scope, expected_source in sources.items():
        heartbeat = mapping(heartbeats.get(scope))
        exists, fresh = truth(heartbeat.get("exists")), truth(heartbeat.get("fresh"))
        source_matches = heartbeat.get("source") == expected_source
        same_epoch = (epoch_verified and bool(meta)
                      and all(isinstance(meta.get(key), str) and meta[key]
                              and heartbeat.get(key) == meta[key] for key in ("run_id", "boot_id"))
                      and type(meta.get("monotonic_time")) in (int, float)
                      and type(heartbeat.get("run_monotonic_time")) in (int, float)
                      and heartbeat["run_monotonic_time"] == meta["monotonic_time"])
        process_truth, session_truth = truth(processes.get(scope)), truth(sessions.get(scope))
        api_truth = truth(observation.get("runtime_api")) if scope == "runtime" else False
        log_truth = truth(logs.get(scope))
        heartbeat_truth = None
        if exists is False or fresh is False or (heartbeat.get("source") is not None and not source_matches):
            heartbeat_truth = False
        elif exists is True and fresh is True and source_matches and same_epoch:
            heartbeat_truth = heartbeat.get("status") == "alive" if isinstance(heartbeat.get("status"), str) else None
        if heartbeat.get("source") is not None and not source_matches:
            status = "BROKEN"
        elif exists is True and (heartbeat.get("status") == "stopped" or process_truth is False):
            status = "DEAD"
        elif (not same_epoch or exists is not True or fresh is not True
              or heartbeat_truth is None or process_truth is None or session_truth is None
              or (scope == "runtime" and api_truth is None)):
            status = "UNKNOWN"
        elif heartbeat_truth is True and process_truth is True and session_truth is True and (scope != "runtime" or api_truth is True):
            status = "ALIVE"
        else:
            status = "DEGRADED"
        if exists is False or not heartbeat:
            last_seen = "missing"
        elif fresh is False:
            last_seen = "stale"
        elif heartbeat_truth is True:
            last_seen = "fresh"
        else:
            last_seen = "unknown"
        consistency = _derive_consistency_status(
            heartbeat_truth=heartbeat_truth, process_truth=process_truth,
            session_truth=session_truth, api_truth=api_truth, log_truth=log_truth,
            api_required=scope == "runtime")
        if not same_epoch:
            consistency = "UNKNOWN"
        entries.append(FoundationTruthConsistencyEntry(
            consistency_entry_id=f"foundationconsistency_{scope}_001",
            component_id=f"foundation_{scope}_component_001", truth_scope=scope,
            heartbeat_truth=heartbeat_truth, process_truth=process_truth,
            session_truth=session_truth, api_truth=api_truth, log_truth=log_truth,
            derived_status=_validate_status(status), consistency_status=consistency,
            description=f"Canonical observed foundation truth for {scope}; unknown facts remain unavailable; API is applicable only to runtime; retained logs do not grant current health.",
            last_seen_label=last_seen,
        ))
    values = tuple(entries)
    return FoundationTruthConsistencyContract(
        total_entries=len(values),
        consistent_entries=sum(item.consistency_status == "CONSISTENT" for item in values),
        mismatch_entries=sum(item.consistency_status == "MISMATCH" for item in values),
        partial_entries=sum(item.consistency_status == "PARTIAL" for item in values),
        unknown_entries=sum(item.consistency_status == "UNKNOWN" for item in values),
        entries=values,
    )
