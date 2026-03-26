from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FoundationDegradedStateEntry:
    """Canonical degraded-state entry for foundation dashboard hardening."""

    degraded_entry_id: str
    component_id: str
    truth_scope: str
    is_currently_degraded: bool
    degraded_since_monotonic: float | None
    degraded_reason: str | None
    recovered_at_monotonic: float | None
    historical_only: bool
    description: str


@dataclass(frozen=True)
class FoundationDegradedStateContract:
    """Canonical degraded-state contract for foundation dashboard hardening."""

    total_entries: int
    currently_degraded_entries: int
    historical_only_entries: int
    recovered_entries: int
    entries: tuple[FoundationDegradedStateEntry, ...]


def build_foundation_degraded_state_contract() -> FoundationDegradedStateContract:
    """Build canonical degraded-state contract for foundation components."""
    entries = (
        FoundationDegradedStateEntry(
            degraded_entry_id="foundationdegraded_runtime_001",
            component_id="foundation_runtime_component_001",
            truth_scope="runtime",
            is_currently_degraded=False,
            degraded_since_monotonic=None,
            degraded_reason=None,
            recovered_at_monotonic=None,
            historical_only=False,
            description="Canonical degraded-state entry for runtime component.",
        ),
        FoundationDegradedStateEntry(
            degraded_entry_id="foundationdegraded_guard_001",
            component_id="foundation_guard_component_001",
            truth_scope="guard",
            is_currently_degraded=False,
            degraded_since_monotonic=None,
            degraded_reason=None,
            recovered_at_monotonic=None,
            historical_only=False,
            description="Canonical degraded-state entry for stop-gate watcher.",
        ),
        FoundationDegradedStateEntry(
            degraded_entry_id="foundationdegraded_core_guard_001",
            component_id="foundation_core_guard_component_001",
            truth_scope="core_guard",
            is_currently_degraded=False,
            degraded_since_monotonic=None,
            degraded_reason=None,
            recovered_at_monotonic=None,
            historical_only=False,
            description="Canonical degraded-state entry for core guard.",
        ),
        FoundationDegradedStateEntry(
            degraded_entry_id="foundationdegraded_kernel_guard_001",
            component_id="foundation_kernel_guard_component_001",
            truth_scope="kernel_guard",
            is_currently_degraded=False,
            degraded_since_monotonic=None,
            degraded_reason=None,
            recovered_at_monotonic=None,
            historical_only=False,
            description="Canonical degraded-state entry for kernel watchdog.",
        ),
    )

    return FoundationDegradedStateContract(
        total_entries=len(entries),
        currently_degraded_entries=sum(
            1 for entry in entries if entry.is_currently_degraded
        ),
        historical_only_entries=sum(1 for entry in entries if entry.historical_only),
        recovered_entries=sum(
            1 for entry in entries if entry.recovered_at_monotonic is not None
        ),
        entries=entries,
    )
