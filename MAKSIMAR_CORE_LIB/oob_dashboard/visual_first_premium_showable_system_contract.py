from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PremiumShowableSystemMode = Literal[
    "first_premium_showable_system",
]

PremiumShowableSystemStatus = Literal[
    "premium_showable_system_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPremiumShowableSystemEntry:
    """Canonical first premium showable system entry."""

    premium_showable_system_id: str
    premium_live_operator_id: str
    premium_showable_system_mode: PremiumShowableSystemMode
    premium_showable_system_status: PremiumShowableSystemStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    premium_live_operator_ready: bool
    premium_showable_system_ready: bool
    truth_bound_premium_showable_system: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPremiumShowableSystemContract:
    """Canonical first premium showable system contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPremiumShowableSystemEntry, ...]


def build_visual_first_premium_showable_system_contract(
) -> VisualFirstPremiumShowableSystemContract:
    """Build canonical first premium showable system contract."""
    from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_premium_live_operator_contract import (
        build_visual_first_premium_live_operator_contract,
    )

    premium_live_operator_contract = build_visual_first_premium_live_operator_contract()
    premium_live_operator_entry = premium_live_operator_contract.entries[0]

    entries = (
        VisualFirstPremiumShowableSystemEntry(
            premium_showable_system_id="visual_first_premium_showable_system_001",
            premium_live_operator_id=premium_live_operator_entry.premium_live_operator_id,
            premium_showable_system_mode="first_premium_showable_system",
            premium_showable_system_status="premium_showable_system_ready",
            renderer_surface_id=premium_live_operator_entry.renderer_surface_id,
            theme_id=premium_live_operator_entry.theme_id,
            screen_id=premium_live_operator_entry.screen_id,
            preview_artifact_id=premium_live_operator_entry.preview_artifact_id,
            premium_live_operator_ready=premium_live_operator_entry.premium_live_operator_ready,
            premium_showable_system_ready=True,
            truth_bound_premium_showable_system=True,
            read_only=True,
            description=(
                "Canonical first premium showable system entry after assembly "
                "of the first truth-preserving premium live operator."
            ),
        ),
    )

    return VisualFirstPremiumShowableSystemContract(
        contract_id="visual_first_premium_showable_system_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.premium_showable_system_status == "premium_showable_system_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
