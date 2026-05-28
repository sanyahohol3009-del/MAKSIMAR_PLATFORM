import pytest

from MAKSIMAR_CORE_LIB.family_child_device_control.guardian_authority_contract import (
    GuardianAuthorityContract,
)


def test_child_runtime_requires_guardian_authority_smoke() -> None:
    with pytest.raises(ValueError, match="guardian_authority_verified must be True"):
        GuardianAuthorityContract(
            guardian_id="guardian_001",
            child_profile_id="child_profile_001",
            guardian_authority_verified=False,
            authority_scope="family_child_device_control",
            audit_required=True,
            expires_epoch_ms=999999,
        )
