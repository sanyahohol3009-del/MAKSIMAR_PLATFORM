import pytest

from ANDROID_SHELL.memory_adapter.android_app_memory_store import AndroidAppMemoryStoreAdapter
from ANDROID_SHELL.memory_adapter.android_memory_state_bridge import AndroidMemoryStateBridge


def _adapter() -> AndroidAppMemoryStoreAdapter:
    return AndroidAppMemoryStoreAdapter.default_adapter(
        adapter_id="android_app_memory_adapter_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
    )


def test_android_memory_state_bridge_is_read_only_snapshot() -> None:
    state = AndroidMemoryStateBridge.from_store_adapter(
        bridge_id="android_memory_state_bridge_001",
        store_adapter=_adapter(),
        record_count=3,
        last_audit_ref="ref://audit/android_memory_state_bridge_001",
    )

    assert state.record_count == 3
    assert state.encrypted_at_rest_required is True
    assert state.retention_required is True
    assert state.sync_policy_required is True
    assert state.offline_first is True
    assert state.state_read_only is True
    assert state.local_app_memory_only is True
    assert state.canonical_truth is False
    assert state.core_write_allowed is False
    assert state.direct_server_write_allowed is False
    assert state.network_allowed is False
    assert state.mutation_allowed is False


def test_android_memory_state_bridge_rejects_mutation() -> None:
    adapter = _adapter()

    with pytest.raises(ValueError, match="mutation_allowed must be False"):
        AndroidMemoryStateBridge(
            bridge_id="bad_state_bridge",
            device_id=adapter.device_id,
            app_id=adapter.app_id,
            android_package_name=adapter.android_package_name,
            store_adapter_ref=f"ref://{adapter.adapter_id}",
            record_count=0,
            encrypted_at_rest_required=True,
            retention_required=True,
            sync_policy_required=True,
            offline_first=True,
            last_audit_ref="ref://audit/bad_state_bridge",
            state_read_only=True,
            local_app_memory_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            mutation_allowed=True,
        )
