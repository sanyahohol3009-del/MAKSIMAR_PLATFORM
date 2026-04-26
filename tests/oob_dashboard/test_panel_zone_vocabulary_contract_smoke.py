from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_zone_vocabulary_contract import (
    build_panel_zone_vocabulary_contract,
    resolve_slot_family,
)


def test_panel_zone_vocabulary_contract_builds() -> None:
    contract = build_panel_zone_vocabulary_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].layout_zone == "foundation_layout_zone"
    assert contract.entries[-1].layout_zone == "operator_layout_zone"


def test_panel_zone_vocabulary_foundation_entries() -> None:
    contract = build_panel_zone_vocabulary_contract()
    foundation_entries = tuple(
        entry for entry in contract.entries if entry.layout_zone == "foundation_layout_zone"
    )

    assert len(foundation_entries) == 5
    assert foundation_entries[0].layout_slot_id == "slot_foundation_main_0"
    assert foundation_entries[0].slot_family == "foundation_main"
    assert foundation_entries[-1].layout_slot_id == "slot_foundation_secondary_1"
    assert foundation_entries[-1].slot_family == "foundation_secondary"


def test_panel_zone_vocabulary_operator_entries() -> None:
    contract = build_panel_zone_vocabulary_contract()
    operator_entries = tuple(
        entry for entry in contract.entries if entry.layout_zone == "operator_layout_zone"
    )

    assert len(operator_entries) == 3
    assert operator_entries[0].layout_slot_id == "slot_operator_main_0"
    assert operator_entries[0].slot_family == "operator_main"
    assert operator_entries[-1].layout_slot_id == "slot_operator_main_2"


def test_resolve_slot_family_smoke() -> None:
    assert resolve_slot_family("slot_foundation_main_0") == "foundation_main"
    assert resolve_slot_family("slot_foundation_secondary_0") == "foundation_secondary"
    assert resolve_slot_family("slot_operator_main_0") == "operator_main"
