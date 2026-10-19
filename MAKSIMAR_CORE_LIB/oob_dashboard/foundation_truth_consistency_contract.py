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
    heartbeat_truth: bool
    process_truth: bool
    session_truth: bool
    api_truth: bool
    log_truth: bool
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
    *,
    heartbeat_truth: bool,
    process_truth: bool,
    session_truth: bool,
    api_truth: bool,
    log_truth: bool,
) -> FoundationConsistencyStatus:
    """Derive consistency status from truth-source booleans."""
    truth_values = (
        heartbeat_truth,
        process_truth,
        session_truth,
        api_truth,
        log_truth,
    )

    if all(truth_values):
        return "CONSISTENT"

    if not any(truth_values):
        return "UNKNOWN"

    true_count = sum(1 for value in truth_values if value)
    false_count = len(truth_values) - true_count

    if true_count >= 1 and false_count >= 1:
        if true_count >= 3:
            return "PARTIAL"
        return "MISMATCH"

    return "UNKNOWN"


def _observe_foundation_consistency() -> dict:
    """Read existing runtime observations without starting or repairing services."""
    from SUPERVISOR.runtime_preflight import inspect_runtime_state
    from CORE_ROOT.heartbeat_io import safe_read_json, heartbeat_process_alive
    from CORE_ROOT import runtime_paths as paths

    observation = inspect_runtime_state()
    bindings = {
        "runtime": (paths.RUNTIME_HEARTBEAT_FILE, "SUPERVISOR.process_supervisor", paths.RUNTIME_SESSION_NAME, paths.RUNTIME_LOG_FILE),
        "guard": (paths.GUARD_HEARTBEAT_FILE, "CORE_ROOT.stop_gate_watcher", paths.GUARD_SESSION_NAME, paths.GUARD_LOG_FILE),
        "core_guard": (paths.CORE_GUARD_HEARTBEAT_FILE, "CORE_ROOT.core_guard", paths.CORE_GUARD_SESSION_NAME, paths.CORE_GUARD_LOG_FILE),
        "kernel_guard": (paths.KERNEL_HEARTBEAT_FILE, "CORE_ROOT.kernel_watchdog", paths.KERNEL_GUARD_SESSION_NAME, paths.KERNEL_GUARD_LOG_FILE),
    }
    sessions = set(observation["tmux"]["sessions"])
    processes, session_truth, logs = {}, {}, {}
    for scope, (heartbeat_path, module, session, log_path) in bindings.items():
        payload = safe_read_json(heartbeat_path)
        processes[scope] = bool(payload and heartbeat_process_alive(payload, module))
        session_truth[scope] = session in sessions
        # This field means retained log evidence is present, not log freshness.
        logs[scope] = log_path.is_file()
    return {
        "heartbeats": observation["heartbeats"],
        "processes": processes,
        "sessions": session_truth,
        "logs": logs,
        "runtime_api": observation["health"]["ok"] and observation["port"]["owned_by_project"],
    }


def build_foundation_truth_consistency_contract() -> FoundationTruthConsistencyContract:
    """Project observed foundation truth through the existing contract."""
    observation = _observe_foundation_consistency()
    sources = {
        "runtime": "process_supervisor", "guard": "stop_gate_watcher",
        "core_guard": "core_guard", "kernel_guard": "kernel_watchdog",
    }
    entries = []
    for scope, expected_source in sources.items():
        heartbeat = observation["heartbeats"].get(scope, {})
        source_matches = heartbeat.get("source") == expected_source
        heartbeat_truth = bool(heartbeat.get("fresh") and source_matches and heartbeat.get("status") == "alive")
        process_truth = bool(observation["processes"].get(scope))
        session_truth = bool(observation["sessions"].get(scope))
        api_truth = bool(scope == "runtime" and observation["runtime_api"])
        log_truth = bool(observation["logs"].get(scope))
        if not heartbeat.get("exists") and not process_truth:
            status = "UNKNOWN"
        elif heartbeat.get("source") and not source_matches:
            status = "BROKEN"
        elif heartbeat.get("status") == "stopped" or not process_truth:
            status = "DEAD"
        elif heartbeat_truth and session_truth and (api_truth or scope != "runtime"):
            status = "ALIVE"
        else:
            status = "DEGRADED"
        if heartbeat_truth:
            last_seen = "fresh"
        elif not heartbeat.get("exists"):
            last_seen = "missing"
        elif source_matches and heartbeat.get("age_seconds") is not None:
            last_seen = "stale"
        else:
            last_seen = "unknown"
        entries.append(FoundationTruthConsistencyEntry(
            consistency_entry_id=f"foundationconsistency_{scope}_001",
            component_id=f"foundation_{scope}_component_001", truth_scope=scope,
            heartbeat_truth=heartbeat_truth, process_truth=process_truth,
            session_truth=session_truth, api_truth=api_truth, log_truth=log_truth,
            derived_status=_validate_status(status),
            consistency_status=_derive_consistency_status(
                heartbeat_truth=heartbeat_truth, process_truth=process_truth,
                session_truth=session_truth, api_truth=api_truth, log_truth=log_truth),
            description=f"Observed foundation truth for {scope}; log truth denotes retained log presence and API truth applies only to runtime.",
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
