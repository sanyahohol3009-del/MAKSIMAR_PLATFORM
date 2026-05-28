import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.child_app_control_policy_contract import (
    ChildAppControlPolicyContract,
)


def test_child_app_control_policy_contract_smoke() -> None:
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

    assert policy.requires_install_approval() is True


def test_child_app_control_policy_rejects_runtime_execution() -> None:
    with pytest.raises(ValueError, match="runtime_execution_allowed must be False in BATCH 4.2"):
        ChildAppControlPolicyContract(
            policy_id="child_app_policy_bad",
            child_device_id="child_device_001",
            guardian_authority_verified=True,
            family_policy_enabled=True,
            app_blocking_allowed_by_guardian_policy=True,
            install_approval_required=True,
            audit_required=True,
            dashboard_bypass_allowed=False,
            runtime_execution_allowed=True,
        )
