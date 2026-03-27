from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_zone_slot_vocabulary_contract,
)


def test_panel_zone_slot_vocabulary_contract_builds() -> None:
    """Panel zone/slot vocabulary contract should build successfully."""
    contract = build_panel_zone_slot_vocabulary_contract()

    assert contract.total_zones == 4
    assert contract.total_slots == 8
    assert contract.used_zones == 4
    assert contract.used_slots == 6


def test_panel_zone_slot_vocabulary_zone_entries() -> None:
    """Zone vocabulary should expose canonical zone list."""
    contract = build_panel_zone_slot_vocabulary_contract()

    assert [entry.panel_zone for entry in contract.zone_entries] == [
        "left_sidebar",
        "main_focus",
        "diagnostics_strip",
        "secondary_zone",
    ]


def test_panel_zone_slot_vocabulary_slot_entries() -> None:
    """Slot vocabulary should expose canonical slot list."""
    contract = build_panel_zone_slot_vocabulary_contract()

    assert contract.slot_entries[0].panel_slot == "slot_left_1"
    assert contract.slot_entries[2].panel_slot == "slot_main_1"
    assert contract.slot_entries[4].panel_slot == "slot_diag_1"
    assert contract.slot_entries[-1].panel_slot == "slot_secondary_2"


def test_panel_zone_slot_vocabulary_parent_zone_mapping() -> None:
    """Slot vocabulary should preserve canonical parent-zone mapping."""
    contract = build_panel_zone_slot_vocabulary_contract()
    slot_map = {entry.panel_slot: entry.parent_zone for entry in contract.slot_entries}

    assert slot_map["slot_left_1"] == "left_sidebar"
    assert slot_map["slot_main_1"] == "main_focus"
    assert slot_map["slot_diag_1"] == "diagnostics_strip"
    assert slot_map["slot_secondary_1"] == "secondary_zone"
