from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.base_family_mount_plan_contract import (
    build_base_family_mount_plan_contract,
)


def test_base_family_mount_plan_contract_builds() -> None:
    contract = build_base_family_mount_plan_contract()
    assert contract.contract_id == "base_family_mount_plan_contract_001"
    assert contract.total_entries == 2
    assert contract.mount_planned_entries == 2
    assert contract.operator_visible_entries == 2
    assert contract.truth_bound_entries == 2
