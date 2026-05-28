from __future__ import annotations

from shared_mobile_core.app_memory.app_memory_store_contract import (
    AppMemoryStoreContract,
)


def test_app_memory_store_contract_smoke() -> None:
    store = AppMemoryStoreContract.default_mobile_store(
        store_id="app_memory_store_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
    )

    assert store.encrypted_at_rest_required is True
    assert store.retention_required is True
    assert store.offline_first is True
    assert store.shell_adapter_only is True
    assert store.canonical_truth is False
    assert store.core_write_allowed is False
    assert store.direct_server_write_allowed is False
    assert store.supported_record_kinds
