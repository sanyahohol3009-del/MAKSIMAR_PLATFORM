from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)


PanelZone = Literal[
    "foundation_layout_zone",
    "operator_layout_zone",
]

PanelSlot = Literal[
    "slot_foundation_main_0",
    "slot_foundation_main_1",
    "slot_foundation_main_2",
    "slot_foundation_secondary_0",
    "slot_foundation_secondary_1",
    "slot_operator_main_0",
    "slot_operator_main_1",
    "slot_operator_main_2",
]


@dataclass(frozen=True, slots=True)
class PanelZoneVocabularyEntry:
    """Canonical panel-zone vocabulary entry."""

    panel_zone: PanelZone
    description: str


@dataclass(frozen=True, slots=True)
class PanelSlotVocabularyEntry:
    """Canonical panel-slot vocabulary entry."""

    panel_slot: PanelSlot
    parent_zone: PanelZone
    description: str


@dataclass(frozen=True, slots=True)
class PanelZoneSlotVocabularyContract:
    """Canonical panel zone/slot vocabulary contract."""

    total_zones: int
    total_slots: int
    used_zones: int
    used_slots: int
    zone_entries: tuple[PanelZoneVocabularyEntry, ...]
    slot_entries: tuple[PanelSlotVocabularyEntry, ...]


def build_panel_zone_slot_vocabulary_contract() -> PanelZoneSlotVocabularyContract:
    """Build canonical panel zone/slot vocabulary contract."""
    layout_contract = build_layout_composition_contract()

    zone_entries = (
        PanelZoneVocabularyEntry(
            panel_zone="foundation_layout_zone",
            description="Canonical layout zone for foundation monitoring workspace panels.",
        ),
        PanelZoneVocabularyEntry(
            panel_zone="operator_layout_zone",
            description="Canonical layout zone for operator interaction workspace panels.",
        ),
    )

    slot_entries = (
        PanelSlotVocabularyEntry(
            panel_slot="slot_foundation_main_0",
            parent_zone="foundation_layout_zone",
            description="Canonical first foundation main slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_foundation_main_1",
            parent_zone="foundation_layout_zone",
            description="Canonical second foundation main slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_foundation_main_2",
            parent_zone="foundation_layout_zone",
            description="Canonical third foundation main slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_foundation_secondary_0",
            parent_zone="foundation_layout_zone",
            description="Canonical first foundation secondary slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_foundation_secondary_1",
            parent_zone="foundation_layout_zone",
            description="Canonical second foundation secondary slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_operator_main_0",
            parent_zone="operator_layout_zone",
            description="Canonical first operator main slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_operator_main_1",
            parent_zone="operator_layout_zone",
            description="Canonical second operator main slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_operator_main_2",
            parent_zone="operator_layout_zone",
            description="Canonical third operator main slot.",
        ),
    )

    used_zones = {entry.layout_zone for entry in layout_contract.entries}
    used_slots = {entry.layout_slot_id for entry in layout_contract.entries}

    return PanelZoneSlotVocabularyContract(
        total_zones=len(zone_entries),
        total_slots=len(slot_entries),
        used_zones=sum(1 for entry in zone_entries if entry.panel_zone in used_zones),
        used_slots=sum(1 for entry in slot_entries if entry.panel_slot in used_slots),
        zone_entries=zone_entries,
        slot_entries=slot_entries,
    )
