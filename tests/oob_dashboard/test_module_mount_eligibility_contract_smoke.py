from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.module_mount_eligibility_contract import (
    build_module_mount_eligibility_contract,
)


def test_module_mount_eligibility_contract_builds() -> None:
    contract = build_module_mount_eligibility_contract()
    assert contract.contract_id == "module_mount_eligibility_contract_001"
    assert contract.total_entries == 3
    assert contract.mount_allowed_entries == 3
    assert contract.permission_valid_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3
