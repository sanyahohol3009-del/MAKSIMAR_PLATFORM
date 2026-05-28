from __future__ import annotations

from shared_mobile_core.app_memory.app_memory_encryption_contract import (
    AppMemoryEncryptionContract,
)


def test_app_memory_encryption_contract_smoke() -> None:
    contract = AppMemoryEncryptionContract.default_mobile_encryption(
        encryption_policy_id="encryption_001",
        key_ref="keystore://app-memory/key_001",
    )

    assert contract.encryption_required is True
    assert contract.at_rest_required is True
    assert contract.in_transit_requires_sync_policy is True
    assert contract.key_material_embedded is False
    assert contract.shell_keystore_required is True
    assert contract.plaintext_allowed is False
