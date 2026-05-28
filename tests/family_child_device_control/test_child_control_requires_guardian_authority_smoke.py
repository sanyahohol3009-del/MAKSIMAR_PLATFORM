import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_remote_control_intent_contract import (
    ChildRemoteControlIntentContract,
)


def test_child_control_requires_guardian_authority_smoke() -> None:
    with pytest.raises(ValueError, match="guardian_authority_verified must be True"):
        ChildRemoteControlIntentContract(
            intent_id="child_remote_intent_no_guardian",
            child_device_id="child_device_001",
            guardian_id="guardian_001",
            intent_type="touch_control",
            guardian_authority_verified=False,
            family_policy_enabled=True,
            audit_required=True,
            visible_child_device_status_required=True,
            dashboard_bypass_allowed=False,
            runtime_execution_allowed=False,
        )
