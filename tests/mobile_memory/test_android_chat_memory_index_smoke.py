import pytest

from ANDROID_SHELL.memory_adapter.android_chat_memory_index import AndroidChatMemoryIndexAdapter


_RECORD_REFS = ("chat-memory://android_device_001/records/message_001",)


def test_android_chat_memory_index_stores_references_only() -> None:
    index = AndroidChatMemoryIndexAdapter.default_index(
        adapter_id="android_chat_index_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
        indexed_record_refs=_RECORD_REFS,
    )

    assert index.supports_offline_search is True
    assert index.stores_message_body is False
    assert index.stores_heavy_payload is False
    assert index.shell_adapter_only is True
    assert index.local_chat_memory_only is True
    assert index.openim_truth is False
    assert index.core_chat_truth is False
    assert index.canonical_truth is False
    assert index.mutation_allowed is False
    assert index.network_allowed is False


def test_android_chat_memory_index_rejects_message_body_storage() -> None:
    base = AndroidChatMemoryIndexAdapter.default_index(
        adapter_id="android_chat_index_001",
        device_id="android_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        android_package_name="de.maksimar.mobile",
        indexed_record_refs=_RECORD_REFS,
    )

    with pytest.raises(ValueError, match="stores_message_body must be False"):
        AndroidChatMemoryIndexAdapter(
            adapter_id="bad_index",
            index_contract=base.index_contract,
            device_id=base.device_id,
            app_id=base.app_id,
            owner_identity_id=base.owner_identity_id,
            android_package_name=base.android_package_name,
            local_index_ref=base.local_index_ref,
            indexed_record_refs=base.indexed_record_refs,
            supports_offline_search=True,
            stores_message_body=True,
            stores_heavy_payload=False,
            shell_adapter_only=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            mutation_allowed=False,
            network_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )
