from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_role_contract import (
    build_display_role_contract,
)


def test_display_role_contract_builds() -> None:
    contract = build_display_role_contract()

    assert len(contract.entries) == 3
    assert contract.entries[0].display_target_id == "display_foundation_primary"
    assert contract.entries[-1].display_target_id == "display_operator_interaction"


def test_display_role_contract_values_are_canonical() -> None:
    contract = build_display_role_contract()
    role_map = {entry.display_target_id: entry for entry in contract.entries}

    assert role_map["display_foundation_primary"].display_role == (
        "foundation_primary_display"
    )
    assert role_map["display_foundation_secondary"].display_role == (
        "foundation_secondary_display"
    )
    assert role_map["display_operator_interaction"].display_role == (
        "operator_interaction_display"
    )
