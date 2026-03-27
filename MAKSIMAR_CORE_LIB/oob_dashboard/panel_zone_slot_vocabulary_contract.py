from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)


PanelZone = Literal[
    "left_sidebar",
    "main_focus",
    "diagnostics_strip",
    "secondary_zone",
]

PanelSlot = Literal[
    "slot_left_1",
    "slot_left_2",
    "slot_main_1",
    "slot_main_2",
    "slot_diag_1",
    "slot_diag_2",
    "slot_secondary_1",
    "slot_secondary_2",
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
            panel_zone="left_sidebar",
            description="Canonical sidebar zone for navigation/monitoring surfaces.",
        ),
        PanelZoneVocabularyEntry(
            panel_zone="main_focus",
            description="Canonical main-focus zone for primary workspace surfaces.",
        ),
        PanelZoneVocabularyEntry(
            panel_zone="diagnostics_strip",
            description="Canonical diagnostics strip zone for incident/diagnostic surfaces.",
        ),
        PanelZoneVocabularyEntry(
            panel_zone="secondary_zone",
            description="Canonical secondary zone for expansion/supporting surfaces.",
        ),
    )

    slot_entries = (
        PanelSlotVocabularyEntry(
            panel_slot="slot_left_1",
            parent_zone="left_sidebar",
            description="Canonical first sidebar slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_left_2",
            parent_zone="left_sidebar",
            description="Canonical second sidebar slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_main_1",
            parent_zone="main_focus",
            description="Canonical first main-focus slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_main_2",
            parent_zone="main_focus",
            description="Canonical second main-focus slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_diag_1",
            parent_zone="diagnostics_strip",
            description="Canonical first diagnostics-strip slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_diag_2",
            parent_zone="diagnostics_strip",
            description="Canonical second diagnostics-strip slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_secondary_1",
            parent_zone="secondary_zone",
            description="Canonical first secondary-zone slot.",
        ),
        PanelSlotVocabularyEntry(
            panel_slot="slot_secondary_2",
            parent_zone="secondary_zone",
            description="Canonical second secondary-zone slot.",
        ),
    )

    used_zones = {entry.layout_zone for entry in layout_contract.entries}
    used_slots = {entry.layout_slot for entry in layout_contract.entries}

    return PanelZoneSlotVocabularyContract(
        total_zones=len(zone_entries),
        total_slots=len(slot_entries),
        used_zones=sum(1 for entry in zone_entries if entry.panel_zone in used_zones),
        used_slots=sum(1 for entry in slot_entries if entry.panel_slot in used_slots),
        zone_entries=zone_entries,
        slot_entries=slot_entries,
    )
