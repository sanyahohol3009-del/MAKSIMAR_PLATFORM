from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_sidebar_navigation_refinement_contract import (
    build_visual_sidebar_navigation_refinement_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_bar_contract import (
    build_visual_status_bar_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_bottom_ticker_contract import (
    build_visual_bottom_ticker_contract,
)


StatusTickerRefinementMode = Literal[
    "phase_1_status_ticker_refinement",
]

StatusClarityProfile = Literal[
    "strong_top_status_readability",
]

TickerClarityProfile = Literal[
    "strong_bottom_ticker_readability",
]

OperatorSignalProfile = Literal[
    "clear_operator_signal_ribbon",
]


@dataclass(frozen=True, slots=True)
class VisualStatusTickerRefinementEntry:
    """Canonical Phase 1 status/ticker refinement entry."""

    refinement_id: str
    sidebar_navigation_refinement_id: str
    refinement_mode: StatusTickerRefinementMode
    status_clarity_profile: StatusClarityProfile
    ticker_clarity_profile: TickerClarityProfile
    operator_signal_profile: OperatorSignalProfile
    status_entries: int
    ticker_entries: int
    stronger_top_status_readability: bool
    stronger_bottom_ticker_readability: bool
    stronger_status_hierarchy: bool
    stronger_signal_ribbon_clarity: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualStatusTickerRefinementContract:
    """Canonical Phase 1 status/ticker refinement contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    stronger_status_entries: int
    stronger_ticker_entries: int
    entries: tuple[VisualStatusTickerRefinementEntry, ...]


def build_visual_status_ticker_refinement_contract(
    ) -> VisualStatusTickerRefinementContract:
    """Build canonical Phase 1 status/ticker refinement contract."""
    sidebar_navigation_contract = build_visual_sidebar_navigation_refinement_contract()
    status_bar_contract = build_visual_status_bar_contract()
    bottom_ticker_contract = build_visual_bottom_ticker_contract()

    sidebar_navigation_entry = sidebar_navigation_contract.entries[0]

    entries = (
        VisualStatusTickerRefinementEntry(
            refinement_id="visual_status_ticker_refinement_001",
            sidebar_navigation_refinement_id=sidebar_navigation_entry.refinement_id,
            refinement_mode="phase_1_status_ticker_refinement",
            status_clarity_profile="strong_top_status_readability",
            ticker_clarity_profile="strong_bottom_ticker_readability",
            operator_signal_profile="clear_operator_signal_ribbon",
            status_entries=status_bar_contract.total_entries,
            ticker_entries=bottom_ticker_contract.total_entries,
            stronger_top_status_readability=True,
            stronger_bottom_ticker_readability=True,
            stronger_status_hierarchy=True,
            stronger_signal_ribbon_clarity=True,
            read_only=True,
            description=(
                "Canonical Phase 1 status/ticker refinement entry for "
                "truth-preserving operator HUD polish."
            ),
        ),
    )

    return VisualStatusTickerRefinementContract(
        contract_id="visual_status_ticker_refinement_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        stronger_status_entries=sum(
            1 for entry in entries if entry.stronger_top_status_readability
        ),
        stronger_ticker_entries=sum(
            1 for entry in entries if entry.stronger_bottom_ticker_readability
        ),
        entries=entries,
    )
