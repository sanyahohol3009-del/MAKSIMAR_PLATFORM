from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_policy_handoff_contract import (
    build_gesture_policy_handoff_contract,
)


def test_gesture_policy_handoff_contract_builds() -> None:
    contract = build_gesture_policy_handoff_contract()
    assert contract.contract_id == "gesture_policy_handoff_contract_001"
    assert contract.total_entries == 3
    assert contract.policy_bound_entries == 3
    assert contract.approval_required_entries == 3
    assert contract.guarded_entries == 3
