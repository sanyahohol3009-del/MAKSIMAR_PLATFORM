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


def build_foundation_truth_consistency_contract() -> (
    FoundationTruthConsistencyContract
):
    """Build canonical truth consistency contract for foundation components."""
    entries = (
        FoundationTruthConsistencyEntry(
            consistency_entry_id="foundationconsistency_runtime_001",
            component_id="foundation_runtime_component_001",
            truth_scope="runtime",
            heartbeat_truth=True,
            process_truth=True,
            session_truth=True,
            api_truth=True,
            log_truth=True,
            derived_status=_validate_status("ALIVE"),
            consistency_status=_derive_consistency_status(
                heartbeat_truth=True,
                process_truth=True,
                session_truth=True,
                api_truth=True,
                log_truth=True,
            ),
            description="Canonical truth consistency entry for runtime component.",
        ),
        FoundationTruthConsistencyEntry(
            consistency_entry_id="foundationconsistency_guard_001",
            component_id="foundation_guard_component_001",
            truth_scope="guard",
            heartbeat_truth=True,
            process_truth=True,
            session_truth=True,
            api_truth=False,
            log_truth=True,
            derived_status=_validate_status("ALIVE"),
            consistency_status=_derive_consistency_status(
                heartbeat_truth=True,
                process_truth=True,
                session_truth=True,
                api_truth=False,
                log_truth=True,
            ),
            description="Canonical truth consistency entry for stop-gate watcher.",
        ),
        FoundationTruthConsistencyEntry(
            consistency_entry_id="foundationconsistency_core_guard_001",
            component_id="foundation_core_guard_component_001",
            truth_scope="core_guard",
            heartbeat_truth=True,
            process_truth=True,
            session_truth=True,
            api_truth=False,
            log_truth=True,
            derived_status=_validate_status("ALIVE"),
            consistency_status=_derive_consistency_status(
                heartbeat_truth=True,
                process_truth=True,
                session_truth=True,
                api_truth=False,
                log_truth=True,
            ),
            description="Canonical truth consistency entry for core guard.",
        ),
        FoundationTruthConsistencyEntry(
            consistency_entry_id="foundationconsistency_kernel_guard_001",
            component_id="foundation_kernel_guard_component_001",
            truth_scope="kernel_guard",
            heartbeat_truth=True,
            process_truth=True,
            session_truth=True,
            api_truth=False,
            log_truth=True,
            derived_status=_validate_status("ALIVE"),
            consistency_status=_derive_consistency_status(
                heartbeat_truth=True,
                process_truth=True,
                session_truth=True,
                api_truth=False,
                log_truth=True,
            ),
            description="Canonical truth consistency entry for kernel watchdog.",
        ),
    )

    return FoundationTruthConsistencyContract(
        total_entries=len(entries),
        consistent_entries=sum(
            1 for entry in entries if entry.consistency_status == "CONSISTENT"
        ),
        mismatch_entries=sum(
            1 for entry in entries if entry.consistency_status == "MISMATCH"
        ),
        partial_entries=sum(
            1 for entry in entries if entry.consistency_status == "PARTIAL"
        ),
        unknown_entries=sum(
            1 for entry in entries if entry.consistency_status == "UNKNOWN"
        ),
        entries=entries,
    )
