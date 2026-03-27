from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)


ResolverState = Literal[
    "resolved",
    "hidden_internal",
]

DisplayAvailability = Literal[
    "available",
]


@dataclass(frozen=True, slots=True)
class DisplayRuntimeResolverEntry:
    """Canonical display runtime / resolver integration entry."""

    panel_id: str
    view_id: str
    display_target_id: str
    resolver_state: ResolverState
    display_availability: DisplayAvailability
    participates_in_runtime_resolution: bool
    description: str


@dataclass(frozen=True, slots=True)
class DisplayRuntimeResolverIntegrationContract:
    """Canonical display runtime / resolver integration contract."""

    total_entries: int
    resolved_entries: int
    hidden_internal_entries: int
    runtime_resolved_entries: int
    entries: tuple[DisplayRuntimeResolverEntry, ...]


def build_display_runtime_resolver_integration_contract() -> (
    DisplayRuntimeResolverIntegrationContract
):
    """Build canonical display runtime / resolver integration contract."""
    chain_contract = build_panel_view_display_chain_contract()
    display_contract = build_display_target_vocabulary_contract()

    valid_display_target_ids = {
        entry.display_target_id for entry in display_contract.entries
    }

    def resolve_resolver_state(panel_id: str) -> ResolverState:
        if panel_id == "panel_navigation":
            return "hidden_internal"
        return "resolved"

    entries = tuple(
        DisplayRuntimeResolverEntry(
            panel_id=entry.panel_id,
            view_id=entry.view_id,
            display_target_id=entry.display_target_id,
            resolver_state=resolve_resolver_state(entry.panel_id),
            display_availability="available",
            participates_in_runtime_resolution=(
                entry.display_target_id in valid_display_target_ids
                and resolve_resolver_state(entry.panel_id) == "resolved"
            ),
            description=(
                f"Canonical display runtime/resolver integration entry for {entry.panel_id}."
            ),
        )
        for entry in chain_contract.entries
    )

    return DisplayRuntimeResolverIntegrationContract(
        total_entries=len(entries),
        resolved_entries=sum(
            1 for entry in entries if entry.resolver_state == "resolved"
        ),
        hidden_internal_entries=sum(
            1 for entry in entries if entry.resolver_state == "hidden_internal"
        ),
        runtime_resolved_entries=sum(
            1 for entry in entries if entry.participates_in_runtime_resolution
        ),
        entries=entries,
    )
