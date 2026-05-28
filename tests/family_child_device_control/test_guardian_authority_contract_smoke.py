import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.guardian_authority_contract import (
    GuardianAuthorityContract,
)


def test_guardian_authority_contract_smoke() -> None:
    authority = GuardianAuthorityContract(
        guardian_id="guardian_001",
        child_profile_id="child_profile_001",
        guardian_authority_verified=True,
        authority_scope="family_child_device_control",
        audit_required=True,
        expires_epoch_ms=2000,
    )

    assert authority.can_authorize_child_control() is True


def test_guardian_authority_rejects_unverified_guardian() -> None:
    with pytest.raises(ValueError, match="guardian_authority_verified must be True"):
        GuardianAuthorityContract(
            guardian_id="guardian_001",
            child_profile_id="child_profile_001",
            guardian_authority_verified=False,
            authority_scope="family_child_device_control",
            audit_required=True,
            expires_epoch_ms=2000,
        )
