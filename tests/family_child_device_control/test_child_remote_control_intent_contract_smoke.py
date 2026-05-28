import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_remote_control_intent_contract import (
    ChildRemoteControlIntentContract,
)


def test_child_remote_control_intent_contract_smoke() -> None:
    intent = ChildRemoteControlIntentContract(
        intent_id="child_remote_intent_001",
        child_device_id="child_device_001",
        guardian_id="guardian_001",
        intent_type="touch_control",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        audit_required=True,
        visible_child_device_status_required=True,
        dashboard_bypass_allowed=False,
        runtime_execution_allowed=False,
    )

    assert intent.is_policy_intent_only() is True


def test_child_remote_control_intent_rejects_runtime_execution_in_batch_4_2() -> None:
    with pytest.raises(ValueError, match="runtime_execution_allowed must be False in BATCH 4.2"):
        ChildRemoteControlIntentContract(
            intent_id="child_remote_intent_bad",
            child_device_id="child_device_001",
            guardian_id="guardian_001",
            intent_type="touch_control",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=False,
            runtime_execution_allowed=True,
        )
