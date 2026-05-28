import pytest

from IOS_SHELL.memory_adapter.ios_chat_memory_index import IOSChatMemoryIndexAdapter


_RECORD_REF = "chat-memory://ios_device_001/records/chat-memory-record-001"


def test_ios_chat_memory_index_stores_references_only() -> None:
    adapter = IOSChatMemoryIndexAdapter.default_index(
        index_adapter_id="ios_chat_memory_index_001",
        device_id="ios_device_001",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
        indexed_record_refs=(_RECORD_REF,),
        audit_ref="audit://ios_chat_memory_index_001",
    )

    assert adapter.supports_offline_search is True
    assert adapter.stores_message_body is False
    assert adapter.stores_heavy_payload is False
    assert adapter.local_chat_memory_only is True
    assert adapter.openim_truth is False
    assert adapter.core_chat_truth is False
    assert adapter.canonical_truth is False
    assert adapter.core_write_allowed is False
    assert adapter.direct_server_write_allowed is False
    assert adapter.network_allowed is False
    assert adapter.platform_api_calls_allowed is False
    assert adapter.sync_runtime_allowed is False


def test_ios_chat_memory_index_rejects_message_body_storage() -> None:
    base = IOSChatMemoryIndexAdapter.default_index(
        index_adapter_id="ios_chat_memory_index_001",
        device_id="ios_device_001",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
        indexed_record_refs=(_RECORD_REF,),
        audit_ref="audit://ios_chat_memory_index_001",
    )

    with pytest.raises(ValueError, match="stores_message_body must be False"):
        IOSChatMemoryIndexAdapter(
            index_adapter_id="bad_ios_chat_memory_index",
            index_contract=base.index_contract,
            device_id=base.device_id,
            owner_identity_id=base.owner_identity_id,
            ios_bundle_id=base.ios_bundle_id,
            indexed_record_refs=base.indexed_record_refs,
            index_storage_ref=base.index_storage_ref,
            index_rebuild_policy_ref=base.index_rebuild_policy_ref,
            supports_offline_search=True,
            stores_message_body=True,
            stores_heavy_payload=False,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
        )
