from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_input_contract import (
    GestureInputEntry,
    build_gesture_input_contract,
)


def test_gesture_input_contract_builds() -> None:
    contract = build_gesture_input_contract()
    assert contract.contract_id == "gesture_input_contract_001"
    assert contract.total_entries == 3
    assert contract.normalized_entries == 3
    assert contract.guarded_entries == 3


def test_gesture_input_rejects_direct_action() -> None:
    with pytest.raises(
        ValueError,
        match="direct_action_allowed must remain false for canonical gesture input entries.",
    ):
        GestureInputEntry(
            gesture_input_id="bad_gesture_input",
            gesture_kind="gesture_pointer_input",
            source_device_id="gesture_sensor_primary",
            normalized_input_ready=True,
            direct_action_allowed=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid gesture input entry.",
        )
