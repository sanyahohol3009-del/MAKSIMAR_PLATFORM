from MAKSIMAR_CORE_LIB.family_child_device_control.child_screen_time_policy_contract import (
    ChildScreenTimePolicyContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_screen_time_policy_runtime import (
    ChildScreenTimePolicyRuntime,
)


def test_child_screen_time_policy_runtime_smoke() -> None:
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

    decision = ChildScreenTimePolicyRuntime().evaluate(policy)

    assert decision.screen_time_limited is True
    assert decision.emergency_lock_policy_allowed is True
    assert decision.runtime_execution_allowed is False
