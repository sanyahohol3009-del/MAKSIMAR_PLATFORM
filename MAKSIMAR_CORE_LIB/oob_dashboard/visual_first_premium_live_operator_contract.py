from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PremiumLiveOperatorMode = Literal[
    "first_premium_live_operator",
]

PremiumLiveOperatorStatus = Literal[
    "premium_live_operator_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPremiumLiveOperatorEntry:
    """Canonical first premium live operator entry."""

    premium_live_operator_id: str
    investor_presentable_live_operator_id: str
    premium_live_operator_mode: PremiumLiveOperatorMode
    premium_live_operator_status: PremiumLiveOperatorStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    investor_presentable_live_operator_ready: bool
    premium_live_operator_ready: bool
    truth_bound_premium_live_operator: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPremiumLiveOperatorContract:
    """Canonical first premium live operator contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPremiumLiveOperatorEntry, ...]


def build_visual_first_premium_live_operator_contract(
) -> VisualFirstPremiumLiveOperatorContract:
    """Build canonical first premium live operator contract."""
    from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_investor_presentable_live_operator_contract import (
        build_visual_first_investor_presentable_live_operator_contract,
    )

    investor_presentable_live_operator_contract = (
        build_visual_first_investor_presentable_live_operator_contract()
    )
    investor_presentable_live_operator_entry = (
        investor_presentable_live_operator_contract.entries[0]
    )

    entries = (
        VisualFirstPremiumLiveOperatorEntry(
            premium_live_operator_id="visual_first_premium_live_operator_001",
            investor_presentable_live_operator_id=(
                investor_presentable_live_operator_entry.investor_presentable_live_operator_id
            ),
            premium_live_operator_mode="first_premium_live_operator",
            premium_live_operator_status="premium_live_operator_ready",
            renderer_surface_id=(
                investor_presentable_live_operator_entry.renderer_surface_id
            ),
            theme_id=investor_presentable_live_operator_entry.theme_id,
            screen_id=investor_presentable_live_operator_entry.screen_id,
            preview_artifact_id=(
                investor_presentable_live_operator_entry.preview_artifact_id
            ),
            investor_presentable_live_operator_ready=(
                investor_presentable_live_operator_entry.investor_presentable_live_operator_ready
            ),
            premium_live_operator_ready=True,
            truth_bound_premium_live_operator=True,
            read_only=True,
            description=(
                "Canonical first premium live operator entry after assembly of "
                "the first truth-preserving investor-presentable live operator."
            ),
        ),
    )

    return VisualFirstPremiumLiveOperatorContract(
        contract_id="visual_first_premium_live_operator_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.premium_live_operator_status == "premium_live_operator_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
