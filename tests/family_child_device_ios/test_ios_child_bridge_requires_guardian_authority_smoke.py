import pytest

from IOS_SHELL.family_child_device.ios_guardian_authority_bridge import (
    IOSGuardianAuthorityBridge,
)


def test_ios_child_bridge_requires_guardian_authority_smoke() -> None:
    with pytest.raises(ValueError, match="guardian_authority_verified must be True"):
        IOSGuardianAuthorityBridge(
            guardian_id="guardian_001",
            child_profile_id="child_profile_001",
            guardian_authority_verified=False,
            authority_scope="family_child_device_control",
            audit_required=True,
            expires_epoch_ms=999999,
            dashboard_bypass_allowed=False,
            ios_platform_api_call_allowed=False,
            runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
