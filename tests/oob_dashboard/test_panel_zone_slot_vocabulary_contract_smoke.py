from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_zone_slot_vocabulary_contract,
)


def test_panel_zone_slot_vocabulary_contract_builds() -> None:
    """Panel zone/slot vocabulary contract should build successfully."""
    contract = build_panel_zone_slot_vocabulary_contract()

    assert contract.total_zones == 2
    assert contract.total_slots == 8
    assert contract.used_zones == 2
    assert contract.used_slots == 8


def test_panel_zone_slot_vocabulary_zone_entries() -> None:
    """Zone vocabulary should expose canonical zone list."""
    contract = build_panel_zone_slot_vocabulary_contract()

    assert [entry.panel_zone for entry in contract.zone_entries] == [
        "foundation_layout_zone",
        "operator_layout_zone",
    ]


def test_panel_zone_slot_vocabulary_slot_entries() -> None:
    """Slot vocabulary should expose canonical slot list."""
    contract = build_panel_zone_slot_vocabulary_contract()

    assert contract.slot_entries[0].panel_slot == "slot_foundation_main_0"
    assert contract.slot_entries[2].panel_slot == "slot_foundation_main_2"
    assert contract.slot_entries[4].panel_slot == "slot_foundation_secondary_1"
    assert contract.slot_entries[-1].panel_slot == "slot_operator_main_2"


def test_panel_zone_slot_vocabulary_parent_zone_mapping() -> None:
    """Slot vocabulary should preserve canonical parent-zone mapping."""
    contract = build_panel_zone_slot_vocabulary_contract()
    slot_map = {entry.panel_slot: entry.parent_zone for entry in contract.slot_entries}

    assert slot_map["slot_foundation_main_0"] == "foundation_layout_zone"
    assert slot_map["slot_foundation_secondary_0"] == "foundation_layout_zone"
    assert slot_map["slot_operator_main_0"] == "operator_layout_zone"
    assert slot_map["slot_operator_main_2"] == "operator_layout_zone"
