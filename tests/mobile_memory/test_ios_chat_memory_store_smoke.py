import pytest

from IOS_SHELL.memory_adapter.ios_chat_memory_store import IOSChatMemoryStoreAdapter


def test_ios_chat_memory_store_is_local_reference_adapter_only() -> None:
    adapter = IOSChatMemoryStoreAdapter.default_adapter(
        adapter_id="ios_chat_memory_adapter_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
    )

    assert adapter.shell_adapter_only is True
    assert adapter.local_chat_memory_only is True
    assert adapter.stores_message_body is False
    assert adapter.stores_heavy_payload is False
    assert adapter.openim_truth is False
    assert adapter.core_chat_truth is False
    assert adapter.canonical_truth is False
    assert adapter.core_write_allowed is False
    assert adapter.direct_server_write_allowed is False
    assert adapter.network_allowed is False
    assert adapter.platform_api_calls_allowed is False
    assert adapter.sync_runtime_allowed is False
    assert adapter.store_contract.sync_policy_required is True


def test_ios_chat_memory_store_rejects_openim_truth() -> None:
    base = IOSChatMemoryStoreAdapter.default_adapter(
        adapter_id="ios_chat_memory_adapter_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
    )

    with pytest.raises(ValueError, match="openim_truth must be False"):
        IOSChatMemoryStoreAdapter(
            adapter_id="bad_ios_chat_memory_adapter",
            store_contract=base.store_contract,
            device_id=base.device_id,
            app_id=base.app_id,
            owner_identity_id=base.owner_identity_id,
            ios_bundle_id=base.ios_bundle_id,
            local_store_ref=base.local_store_ref,
            secure_store_ref=base.secure_store_ref,
            index_ref=base.index_ref,
            replay_state_ref=base.replay_state_ref,
            export_bridge_ref=base.export_bridge_ref,
            shell_adapter_only=True,
            local_chat_memory_only=True,
            stores_message_body=False,
            stores_heavy_payload=False,
            openim_truth=True,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
        )
