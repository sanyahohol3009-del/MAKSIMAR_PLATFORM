from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)


def test_layout_composition_contract_builds() -> None:
    contract = build_layout_composition_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].workspace_id == "workspace_foundation_monitoring"
    assert contract.entries[-1].workspace_id == "workspace_operator_interaction"


def test_layout_composition_foundation_entries() -> None:
    contract = build_layout_composition_contract()
    foundation_entries = tuple(
        entry for entry in contract.entries
        if entry.workspace_id == "workspace_foundation_monitoring"
    )

    assert len(foundation_entries) == 5
    assert foundation_entries[0].panel_id == "system_status"
    assert foundation_entries[0].layout_slot_id == "slot_foundation_main_0"
    assert foundation_entries[-1].panel_id == "topology"
    assert foundation_entries[-1].layout_slot_id == "slot_foundation_secondary_1"


def test_layout_composition_operator_entries() -> None:
    contract = build_layout_composition_contract()
    operator_entries = tuple(
        entry for entry in contract.entries
        if entry.workspace_id == "workspace_operator_interaction"
    )

    assert len(operator_entries) == 3
    assert operator_entries[0].panel_id == "action_queue"
    assert operator_entries[0].layout_slot_id == "slot_operator_main_0"
    assert operator_entries[-1].panel_id == "audit_timeline"
    assert operator_entries[-1].layout_slot_id == "slot_operator_main_2"
