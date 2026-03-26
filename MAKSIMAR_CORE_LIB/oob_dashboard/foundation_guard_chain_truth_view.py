from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_contract import (
    build_foundation_truth_consistency_contract,
)


@dataclass(frozen=True)
class FoundationGuardChainTruthEntry:
    """Canonical guard-chain truth entry for foundation dashboards."""

    guard_entry_id: str
    chain_order_index: int
    truth_scope: str
    display_title: str
    heartbeat_truth: bool
    process_truth: bool
    session_truth: bool
    api_truth: bool
    log_truth: bool
    derived_status: str
    consistency_status: str
    last_seen_label: str
    reason: str | None
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationGuardChainTruthView:
    """Canonical guard-chain truth view for foundation dashboards."""

    view_id: str
    total_entries: int
    consistent_entries: int
    partial_entries: int
    mismatch_entries: int
    unknown_entries: int
    alive_entries: int
    degraded_entries: int
    dead_entries: int
    broken_entries: int
    entries: tuple[FoundationGuardChainTruthEntry, ...]


_SCOPE_TO_TITLE = {
    "runtime": "Runtime Core",
    "guard": "Stop-Gate Watcher",
    "core_guard": "Core Guard",
    "kernel_guard": "Kernel Watchdog",
}

_SCOPE_TO_ORDER = {
    "runtime": 1,
    "guard": 2,
    "core_guard": 3,
    "kernel_guard": 4,
}


def _reason_for_entry(consistency_status: str, derived_status: str) -> str | None:
    """Return human-readable reason for current truth/derived combination."""
    if derived_status == "BROKEN":
        return "Broken foundation state requires operator investigation."
    if derived_status == "DEAD":
        return "Foundation component is currently not alive."
    if derived_status == "DEGRADED":
        return "Foundation component is degraded or partially inconsistent."
    if consistency_status == "PARTIAL":
        return "Truth sources are only partially aligned."
    if consistency_status == "MISMATCH":
        return "Truth sources are mismatched."
    if consistency_status == "UNKNOWN":
        return "Truth sources are insufficient for a safe conclusion."
    return None


def build_foundation_guard_chain_truth_view() -> FoundationGuardChainTruthView:
    """Build canonical guard-chain truth view from truth consistency contract."""
    contract = build_foundation_truth_consistency_contract()

    ordered_entries = sorted(
        contract.entries,
        key=lambda entry: _SCOPE_TO_ORDER[entry.truth_scope],
    )

    entries = tuple(
        FoundationGuardChainTruthEntry(
            guard_entry_id=f"foundation_guard_chain_{entry.truth_scope}_001",
            chain_order_index=_SCOPE_TO_ORDER[entry.truth_scope],
            truth_scope=entry.truth_scope,
            display_title=_SCOPE_TO_TITLE[entry.truth_scope],
            heartbeat_truth=entry.heartbeat_truth,
            process_truth=entry.process_truth,
            session_truth=entry.session_truth,
            api_truth=entry.api_truth,
            log_truth=entry.log_truth,
            derived_status=entry.derived_status,
            consistency_status=entry.consistency_status,
            last_seen_label="fresh",
            reason=_reason_for_entry(
                entry.consistency_status,
                entry.derived_status,
            ),
            read_only=True,
            description=(
                "Canonical guard-chain truth entry derived from foundation truth "
                f"consistency contract for scope={entry.truth_scope}."
            ),
        )
        for entry in ordered_entries
    )

    return FoundationGuardChainTruthView(
        view_id="foundation_guard_chain_truth_view_001",
        total_entries=len(entries),
        consistent_entries=sum(
            1 for entry in entries if entry.consistency_status == "CONSISTENT"
        ),
        partial_entries=sum(
            1 for entry in entries if entry.consistency_status == "PARTIAL"
        ),
        mismatch_entries=sum(
            1 for entry in entries if entry.consistency_status == "MISMATCH"
        ),
        unknown_entries=sum(
            1 for entry in entries if entry.consistency_status == "UNKNOWN"
        ),
        alive_entries=sum(1 for entry in entries if entry.derived_status == "ALIVE"),
        degraded_entries=sum(
            1 for entry in entries if entry.derived_status == "DEGRADED"
        ),
        dead_entries=sum(1 for entry in entries if entry.derived_status == "DEAD"),
        broken_entries=sum(
            1 for entry in entries if entry.derived_status == "BROKEN"
        ),
        entries=entries,
    )
