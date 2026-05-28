import pytest

from IOS_SHELL.family_child_device.ios_guardian_authority_bridge import (
    IOSGuardianAuthorityBridge,
)
from MAKSIMAR_CORE_LIB.family_child_device_control.guardian_authority_contract import (
    GuardianAuthorityContract,
)


def test_ios_guardian_authority_bridge_smoke() -> None:
    bridge = IOSGuardianAuthorityBridge(
        guardian_id="guardian_001",
        child_profile_id="child_profile_001",
        guardian_authority_verified=True,
        authority_scope="family_child_device_control",
        audit_required=True,
        expires_epoch_ms=999999,
        dashboard_bypass_allowed=False,
        ios_platform_api_call_allowed=False,
        runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    contract = bridge.build_authority_contract()
    read_model = bridge.to_read_model()

    assert isinstance(contract, GuardianAuthorityContract)
    assert contract.guardian_id == "guardian_001"
    assert contract.child_profile_id == "child_profile_001"
    assert contract.guardian_authority_verified is True
    assert contract.authority_scope == "family_child_device_control"
    assert contract.audit_required is True
    assert contract.expires_epoch_ms == 999999

    assert read_model["bridge"] == "guardian_authority"
    assert read_model["guardian_authority_verified"] is True
    assert read_model["dashboard_bypass_allowed"] is False
    assert read_model["ios_platform_api_call_allowed"] is False
    assert read_model["runtime_execution_allowed"] is False


def test_ios_guardian_authority_bridge_rejects_wrong_scope() -> None:
    with pytest.raises(ValueError, match="authority_scope must be family_child_device_control"):
        IOSGuardianAuthorityBridge(
            guardian_id="guardian_001",
            child_profile_id="child_profile_001",
            guardian_authority_verified=True,
            authority_scope="wrong_scope",
            audit_required=True,
            expires_epoch_ms=999999,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
