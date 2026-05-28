import pytest

from ANDROID_SHELL.memory_adapter.android_chat_memory_store import AndroidChatMemoryStoreAdapter


def test_android_chat_memory_store_is_adapter_only() -> None:
    adapter = AndroidChatMemoryStoreAdapter.default_adapter(
        adapter_id="android_chat_memory_adapter_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
    )

    assert adapter.shell_adapter_only is True
    assert adapter.local_chat_memory_only is True
    assert adapter.openim_truth is False
    assert adapter.core_chat_truth is False
    assert adapter.canonical_truth is False
    assert adapter.core_write_allowed is False
    assert adapter.direct_server_write_allowed is False
    assert adapter.network_allowed is False
    assert adapter.platform_api_calls_allowed is False
    assert adapter.sync_runtime_allowed is False


def test_android_chat_memory_store_rejects_openim_truth() -> None:
    base = AndroidChatMemoryStoreAdapter.default_adapter(
        adapter_id="android_chat_memory_adapter_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
    )

    with pytest.raises(ValueError, match="openim_truth must be False"):
        AndroidChatMemoryStoreAdapter(
            adapter_id="bad_adapter",
            store_contract=base.store_contract,
            device_id=base.device_id,
            app_id=base.app_id,
            owner_identity_id=base.owner_identity_id,
            android_package_name=base.android_package_name,
            local_store_ref=base.local_store_ref,
            index_ref=base.index_ref,
            offline_replay_state_ref=base.offline_replay_state_ref,
            export_bridge_ref=base.export_bridge_ref,
            shell_adapter_only=True,
            local_chat_memory_only=True,
            openim_truth=True,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
        )
