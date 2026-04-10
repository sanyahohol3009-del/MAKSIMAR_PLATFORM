from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


InvestorPresentableLiveOperatorMode = Literal[
    "first_investor_presentable_live_operator",
]

InvestorPresentableLiveOperatorStatus = Literal[
    "investor_presentable_live_operator_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstInvestorPresentableLiveOperatorEntry:
    """Canonical first investor-presentable live operator entry."""

    investor_presentable_live_operator_id: str
    demo_ready_live_operator_id: str
    investor_presentable_live_operator_mode: InvestorPresentableLiveOperatorMode
    investor_presentable_live_operator_status: InvestorPresentableLiveOperatorStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    demo_ready_live_operator_ready: bool
    investor_presentable_live_operator_ready: bool
    truth_bound_investor_presentable_live_operator: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstInvestorPresentableLiveOperatorContract:
    """Canonical first investor-presentable live operator contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstInvestorPresentableLiveOperatorEntry, ...]


def build_visual_first_investor_presentable_live_operator_contract(
) -> VisualFirstInvestorPresentableLiveOperatorContract:
    """Build canonical first investor-presentable live operator contract."""
    from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_demo_ready_live_operator_contract import (
        build_visual_first_demo_ready_live_operator_contract,
    )

    demo_ready_live_operator_contract = (
        build_visual_first_demo_ready_live_operator_contract()
    )
    demo_ready_live_operator_entry = demo_ready_live_operator_contract.entries[0]

    entries = (
        VisualFirstInvestorPresentableLiveOperatorEntry(
            investor_presentable_live_operator_id=(
                "visual_first_investor_presentable_live_operator_001"
            ),
            demo_ready_live_operator_id=(
                demo_ready_live_operator_entry.demo_ready_live_operator_id
            ),
            investor_presentable_live_operator_mode=(
                "first_investor_presentable_live_operator"
            ),
            investor_presentable_live_operator_status=(
                "investor_presentable_live_operator_ready"
            ),
            renderer_surface_id=demo_ready_live_operator_entry.renderer_surface_id,
            theme_id=demo_ready_live_operator_entry.theme_id,
            screen_id=demo_ready_live_operator_entry.screen_id,
            preview_artifact_id=demo_ready_live_operator_entry.preview_artifact_id,
            demo_ready_live_operator_ready=(
                demo_ready_live_operator_entry.demo_ready_live_operator_ready
            ),
            investor_presentable_live_operator_ready=True,
            truth_bound_investor_presentable_live_operator=True,
            read_only=True,
            description=(
                "Canonical first investor-presentable live operator entry after "
                "assembly of the first truth-preserving demo-ready live operator."
            ),
        ),
    )

    return VisualFirstInvestorPresentableLiveOperatorContract(
        contract_id=(
            "visual_first_investor_presentable_live_operator_contract_001"
        ),
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.investor_presentable_live_operator_status
            == "investor_presentable_live_operator_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
