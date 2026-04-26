from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PhysicsStatusPanelEntry:
    """Canonical physics-status panel entry."""

    subsystem_id: str
    physics_mode: str
    validation_state: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class PhysicsStatusPanelContract:
    """Canonical physics-status panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[PhysicsStatusPanelEntry, ...]
    operator_visible: bool
    description: str


def build_physics_status_panel_contract() -> PhysicsStatusPanelContract:
    """Build canonical physics-status panel contract."""
    entries = (
        PhysicsStatusPanelEntry(
            subsystem_id="surface_intelligence",
            physics_mode="engineering_realistic",
            validation_state="validated",
            operator_visible=True,
            description="Canonical surface-intelligence physics status.",
        ),
        PhysicsStatusPanelEntry(
            subsystem_id="simulation_engine",
            physics_mode="strict_physics",
            validation_state="validated",
            operator_visible=True,
            description="Canonical simulation-engine physics status.",
        ),
        PhysicsStatusPanelEntry(
            subsystem_id="candidate_evaluation",
            physics_mode="control_learning",
            validation_state="review_required",
            operator_visible=True,
            description="Canonical candidate-evaluation physics status.",
        ),
    )

    return PhysicsStatusPanelContract(
        panel_id="panel_physics_status",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical physics-status panel contract.",
    )
