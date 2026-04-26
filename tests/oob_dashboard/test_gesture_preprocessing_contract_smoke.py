from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_preprocessing_contract import (
    build_gesture_preprocessing_contract,
)


def test_gesture_preprocessing_contract_builds() -> None:
    contract = build_gesture_preprocessing_contract()
    assert contract.contract_id == "gesture_preprocessing_contract_001"
    assert contract.total_entries == 3
    assert contract.valid_entries == 3
    assert contract.guarded_entries == 3
