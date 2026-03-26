from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationCanonicalStatus = Literal[
    "WARMING_UP",
    "ALIVE",
    "DEGRADED",
    "DEAD",
    "BROKEN",
    "UNKNOWN",
]


@dataclass(frozen=True)
class FoundationCanonicalStatusEntry:
    """Canonical status entry used across foundation dashboard hardening."""

    status_id: str
    status: FoundationCanonicalStatus
    terminal: bool
    live_state: bool
    historical_only: bool
    severity: str
    description: str


@dataclass(frozen=True)
class FoundationCanonicalStatusModel:
    """Canonical status model for all foundation dashboard layers."""

    total_statuses: int
    live_statuses: int
    terminal_statuses: int
    historical_only_statuses: int
    entries: tuple[FoundationCanonicalStatusEntry, ...]


def build_foundation_canonical_status_model() -> FoundationCanonicalStatusModel:
    """Build canonical foundation status model."""
    entries = (
        FoundationCanonicalStatusEntry(
            status_id="foundation_status_warming_up_001",
            status="WARMING_UP",
            terminal=False,
            live_state=True,
            historical_only=False,
            severity="info",
            description="Foundation component is starting and not yet fully ready.",
        ),
        FoundationCanonicalStatusEntry(
            status_id="foundation_status_alive_001",
            status="ALIVE",
            terminal=False,
            live_state=True,
            historical_only=False,
            severity="info",
            description="Foundation component is healthy and currently alive.",
        ),
        FoundationCanonicalStatusEntry(
            status_id="foundation_status_degraded_001",
            status="DEGRADED",
            terminal=False,
            live_state=True,
            historical_only=False,
            severity="warning",
            description="Foundation component is alive but degraded or inconsistent.",
        ),
        FoundationCanonicalStatusEntry(
            status_id="foundation_status_dead_001",
            status="DEAD",
            terminal=True,
            live_state=True,
            historical_only=False,
            severity="warning",
            description="Foundation component is not alive.",
        ),
        FoundationCanonicalStatusEntry(
            status_id="foundation_status_broken_001",
            status="BROKEN",
            terminal=True,
            live_state=True,
            historical_only=False,
            severity="critical",
            description="Foundation component is in broken or mismatched state.",
        ),
        FoundationCanonicalStatusEntry(
            status_id="foundation_status_unknown_001",
            status="UNKNOWN",
            terminal=False,
            live_state=False,
            historical_only=True,
            severity="warning",
            description=(
                "Foundation status cannot be safely derived from current truth inputs."
            ),
        ),
    )

    return FoundationCanonicalStatusModel(
        total_statuses=len(entries),
        live_statuses=sum(1 for entry in entries if entry.live_state),
        terminal_statuses=sum(1 for entry in entries if entry.terminal),
        historical_only_statuses=sum(
            1 for entry in entries if entry.historical_only
        ),
        entries=entries,
    )
