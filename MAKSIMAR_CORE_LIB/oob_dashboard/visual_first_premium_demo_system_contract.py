from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_premium_showable_system_contract import (
    build_visual_first_premium_showable_system_contract,
)


PremiumDemoSystemMode = Literal[
    "first_premium_demo_system",
]

PremiumDemoSystemStatus = Literal[
    "premium_demo_system_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPremiumDemoSystemEntry:
    """Canonical first premium demo system entry."""

    premium_demo_system_id: str
    premium_showable_system_id: str
    premium_demo_system_mode: PremiumDemoSystemMode
    premium_demo_system_status: PremiumDemoSystemStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    premium_showable_system_ready: bool
    premium_demo_system_ready: bool
    truth_bound_premium_demo_system: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPremiumDemoSystemContract:
    """Canonical first premium demo system contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPremiumDemoSystemEntry, ...]


def build_visual_first_premium_demo_system_contract(
) -> VisualFirstPremiumDemoSystemContract:
    """Build canonical first premium demo system contract."""
    premium_showable_system_contract = (
        build_visual_first_premium_showable_system_contract()
    )
    premium_showable_system_entry = premium_showable_system_contract.entries[0]

    entries = (
        VisualFirstPremiumDemoSystemEntry(
            premium_demo_system_id="visual_first_premium_demo_system_001",
            premium_showable_system_id=(
                premium_showable_system_entry.premium_showable_system_id
            ),
            premium_demo_system_mode="first_premium_demo_system",
            premium_demo_system_status="premium_demo_system_ready",
            renderer_surface_id=premium_showable_system_entry.renderer_surface_id,
            theme_id=premium_showable_system_entry.theme_id,
            screen_id=premium_showable_system_entry.screen_id,
            preview_artifact_id=premium_showable_system_entry.preview_artifact_id,
            premium_showable_system_ready=(
                premium_showable_system_entry.premium_showable_system_ready
            ),
            premium_demo_system_ready=True,
            truth_bound_premium_demo_system=True,
            read_only=True,
            description=(
                "Canonical first premium demo system entry after assembly of "
                "the first truth-preserving premium showable system."
            ),
        ),
    )

    return VisualFirstPremiumDemoSystemContract(
        contract_id="visual_first_premium_demo_system_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.premium_demo_system_status == "premium_demo_system_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
