from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


ThemeHardeningMode = Literal[
    "phase_1_theme_hardening",
]

AccentDiscipline = Literal[
    "blue_orange_operator_hud",
]

DepthProfile = Literal[
    "deep_glass_hud",
]

GlowProfile = Literal[
    "controlled_core_glow",
]

MotionPolicy = Literal[
    "static_first",
]


@dataclass(frozen=True, slots=True)
class VisualThemeHardeningEntry:
    """Canonical Phase 1 visual theme hardening entry."""

    hardening_id: str
    theme_id: str
    hardening_mode: ThemeHardeningMode
    accent_discipline: AccentDiscipline
    depth_profile: DepthProfile
    glow_profile: GlowProfile
    motion_policy: MotionPolicy
    stronger_panel_hierarchy: bool
    stronger_zone_separation: bool
    stronger_center_core_gravity: bool
    stronger_sidebar_navigation_clarity: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualThemeHardeningContract:
    """Canonical Phase 1 visual theme hardening contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    static_first_entries: int
    entries: tuple[VisualThemeHardeningEntry, ...]


def build_visual_theme_hardening_contract() -> VisualThemeHardeningContract:
    """Build canonical Phase 1 visual theme hardening contract."""
    theme_contract = build_visual_theme_contract()
    theme_entry = theme_contract.entries[0]

    entries = (
        VisualThemeHardeningEntry(
            hardening_id="visual_theme_hardening_001",
            theme_id=theme_entry.theme_id,
            hardening_mode="phase_1_theme_hardening",
            accent_discipline="blue_orange_operator_hud",
            depth_profile="deep_glass_hud",
            glow_profile="controlled_core_glow",
            motion_policy="static_first",
            stronger_panel_hierarchy=True,
            stronger_zone_separation=True,
            stronger_center_core_gravity=True,
            stronger_sidebar_navigation_clarity=True,
            read_only=True,
            description=(
                "Canonical Phase 1 visual theme hardening entry for "
                "truth-preserving HUD polish."
            ),
        ),
    )

    return VisualThemeHardeningContract(
        contract_id="visual_theme_hardening_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        static_first_entries=sum(
            1 for entry in entries if entry.motion_policy == "static_first"
        ),
        entries=entries,
    )
