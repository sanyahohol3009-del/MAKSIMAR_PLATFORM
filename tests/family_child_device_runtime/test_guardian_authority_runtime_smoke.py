from MAKSIMAR_CORE_LIB.family_child_device_control.guardian_authority_contract import (
    GuardianAuthorityContract,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.guardian_authority_runtime import (
    GuardianAuthorityRuntime,
)


def test_guardian_authority_runtime_smoke() -> None:
    authority = GuardianAuthorityContract(
        guardian_id="guardian_001",
        child_profile_id="child_profile_001",
        guardian_authority_verified=True,
        authority_scope="family_child_device_control",
        audit_required=True,
        expires_epoch_ms=999999,
    )

    decision = GuardianAuthorityRuntime().evaluate(authority)

    assert decision.authorized is True
    assert decision.reason == "guardian_authority_verified"
