from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.module_registry_audit_contract import (
    build_module_registry_audit_contract,
)


def test_module_registry_audit_contract_builds() -> None:
    contract = build_module_registry_audit_contract()
    assert contract.contract_id == "module_registry_audit_contract_001"
    assert contract.total_entries == 3
    assert contract.audit_visible_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3
