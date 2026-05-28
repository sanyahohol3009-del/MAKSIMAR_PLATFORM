from MAKSIMAR_CORE_LIB.family_child_device_control.child_app_control_policy_contract import (
    ChildAppControlPolicyContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_app_control_policy_runtime import (
    ChildAppControlPolicyRuntime,
)


def test_child_app_control_policy_runtime_smoke() -> None:
    policy = ChildAppControlPolicyContract(
        policy_id="child_app_policy_001",
        child_device_id="child_device_001",
        guardian_authority_verified=True,
        family_policy_enabled=True,
        app_blocking_allowed_by_guardian_policy=True,
        install_approval_required=True,
        audit_required=True,
        dashboard_bypass_allowed=False,
        runtime_execution_allowed=False,
    )

    decision = ChildAppControlPolicyRuntime().evaluate(policy)

    assert decision.app_blocking_allowed is True
    assert decision.install_approval_required is True
    assert decision.runtime_execution_allowed is False
