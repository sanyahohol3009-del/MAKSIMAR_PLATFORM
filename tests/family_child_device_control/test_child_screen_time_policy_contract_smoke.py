import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_time_policy_contract import (
    ChildScreenTimePolicyContract,
)


def test_child_screen_time_policy_contract_smoke() -> None:
    policy = ChildScreenTimePolicyContract(
        policy_id="child_time_policy_001",
        child_device_id="child_device_001",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        daily_limit_minutes=90,
        emergency_lock_allowed_by_guardian_policy=True,
        audit_required=True,
        dashboard_bypass_allowed=False,
        runtime_execution_allowed=False,
    )

    assert policy.is_screen_time_limited() is True


def test_child_screen_time_policy_rejects_negative_limit() -> None:
    with pytest.raises(ValueError, match="daily_limit_minutes must be a non-negative integer"):
        ChildScreenTimePolicyContract(
            policy_id="child_time_policy_bad",
            child_device_id="child_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            daily_limit_minutes=-1,
            emergency_lock_allowed_by_guardian_policy=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            runtime_execution_allowed=False,
        )
