from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_panel_hierarchy_hardening_contract import (
    build_visual_panel_hierarchy_hardening_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_signal_overlay_contract import (
    build_visual_signal_overlay_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_topology_overlay_contract import (
    build_visual_topology_overlay_contract,
)


CenterCoreRefinementMode = Literal[
    "phase_1_center_core_refinement",
]

CoreGravityProfile = Literal[
    "strong_center_gravity",
]

SignalRouteProfile = Literal[
    "readable_core_signal_routes",
]

DepthDisciplineProfile = Literal[
    "controlled_center_depth",
]

RotationPolicy = Literal[
    "rotation_not_enabled_yet",
]


@dataclass(frozen=True, slots=True)
class VisualCenterCoreRefinementEntry:
    """Canonical Phase 1 center-core refinement entry."""

    refinement_id: str
    hierarchy_hardening_id: str
    refinement_mode: CenterCoreRefinementMode
    core_gravity_profile: CoreGravityProfile
    signal_route_profile: SignalRouteProfile
    depth_discipline_profile: DepthDisciplineProfile
    rotation_policy: RotationPolicy
    total_signal_routes: int
    topology_overlay_entries: int
    stronger_center_core_gravity: bool
    stronger_signal_route_readability: bool
    stronger_depth_hierarchy: bool
    no_fake_runtime_activity: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualCenterCoreRefinementContract:
    """Canonical Phase 1 center-core refinement contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    stronger_gravity_entries: int
    stronger_signal_entries: int
    entries: tuple[VisualCenterCoreRefinementEntry, ...]


def build_visual_center_core_refinement_contract(
    ) -> VisualCenterCoreRefinementContract:
    """Build canonical Phase 1 center-core refinement contract."""
    hierarchy_contract = build_visual_panel_hierarchy_hardening_contract()
    signal_overlay_contract = build_visual_signal_overlay_contract()
    topology_overlay_contract = build_visual_topology_overlay_contract()

    hierarchy_entry = hierarchy_contract.entries[0]

    entries = (
        VisualCenterCoreRefinementEntry(
            refinement_id="visual_center_core_refinement_001",
            hierarchy_hardening_id=hierarchy_entry.hardening_id,
            refinement_mode="phase_1_center_core_refinement",
            core_gravity_profile="strong_center_gravity",
            signal_route_profile="readable_core_signal_routes",
            depth_discipline_profile="controlled_center_depth",
            rotation_policy="rotation_not_enabled_yet",
            total_signal_routes=signal_overlay_contract.total_entries,
            topology_overlay_entries=topology_overlay_contract.total_entries,
            stronger_center_core_gravity=True,
            stronger_signal_route_readability=True,
            stronger_depth_hierarchy=True,
            no_fake_runtime_activity=True,
            read_only=True,
            description=(
                "Canonical Phase 1 center-core refinement entry for "
                "truth-preserving operator HUD polish."
            ),
        ),
    )

    return VisualCenterCoreRefinementContract(
        contract_id="visual_center_core_refinement_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        stronger_gravity_entries=sum(
            1 for entry in entries if entry.stronger_center_core_gravity
        ),
        stronger_signal_entries=sum(
            1 for entry in entries if entry.stronger_signal_route_readability
        ),
        entries=entries,
    )
