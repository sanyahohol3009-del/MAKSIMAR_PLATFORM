from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DigitalTwinPanelEntry:
    """Canonical digital-twin panel entry."""

    twin_component_id: str
    twin_state: str
    sync_state: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class DigitalTwinPanelContract:
    """Canonical digital-twin panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[DigitalTwinPanelEntry, ...]
    operator_visible: bool
    description: str


def build_digital_twin_panel_contract() -> DigitalTwinPanelContract:
    """Build canonical digital-twin panel contract."""
    entries = (
        DigitalTwinPanelEntry(
            twin_component_id="surface_model",
            twin_state="ready",
            sync_state="in_sync",
            operator_visible=True,
            description="Canonical digital-twin surface model state.",
        ),
        DigitalTwinPanelEntry(
            twin_component_id="toolpath_model",
            twin_state="ready",
            sync_state="in_sync",
            operator_visible=True,
            description="Canonical digital-twin toolpath model state.",
        ),
        DigitalTwinPanelEntry(
            twin_component_id="material_profile",
            twin_state="ready",
            sync_state="in_sync",
            operator_visible=True,
            description="Canonical digital-twin material profile state.",
        ),
    )

    return DigitalTwinPanelContract(
        panel_id="panel_digital_twin",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical digital-twin panel contract.",
    )
