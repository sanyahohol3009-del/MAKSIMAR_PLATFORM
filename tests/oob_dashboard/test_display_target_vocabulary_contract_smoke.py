from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)


def test_display_target_vocabulary_contract_builds() -> None:
    contract = build_display_target_vocabulary_contract()

    assert len(contract.entries) == 3
    assert contract.entries[0].display_target_id == "display_foundation_primary"
    assert contract.entries[-1].display_target_id == "display_operator_interaction"


def test_display_target_vocabulary_contract_roles_and_zones_are_canonical() -> None:
    contract = build_display_target_vocabulary_contract()
    target_map = {entry.display_target_id: entry for entry in contract.entries}

    assert target_map["display_foundation_primary"].display_role == (
        "foundation_primary_display"
    )
    assert target_map["display_foundation_primary"].display_zone == (
        "foundation_main_zone"
    )

    assert target_map["display_foundation_secondary"].display_role == (
        "foundation_secondary_display"
    )
    assert target_map["display_foundation_secondary"].display_zone == (
        "foundation_secondary_zone"
    )

    assert target_map["display_operator_interaction"].display_role == (
        "operator_interaction_display"
    )
    assert target_map["display_operator_interaction"].display_zone == (
        "operator_interaction_zone"
    )
