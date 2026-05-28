import pytest

from IOS_SHELL.memory_adapter.ios_chat_memory_export_bridge import IOSChatMemoryExportBridge
from IOS_SHELL.memory_adapter.ios_chat_memory_index import IOSChatMemoryIndexAdapter
from IOS_SHELL.memory_adapter.ios_chat_memory_store import IOSChatMemoryStoreAdapter


_RECORD_REF = "chat-memory://ios_device_001/records/chat-memory-record-001"


def _store() -> IOSChatMemoryStoreAdapter:
    return IOSChatMemoryStoreAdapter.default_adapter(
        adapter_id="ios_chat_memory_adapter_001",
        device_id="ios_device_001",
        app_id="maksimar_mobile",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
    )


def _index() -> IOSChatMemoryIndexAdapter:
    return IOSChatMemoryIndexAdapter.default_index(
        index_adapter_id="ios_chat_memory_index_001",
        device_id="ios_device_001",
        owner_identity_id="owner_001",
        ios_bundle_id="de.maksimar.mobile",
        indexed_record_refs=(_RECORD_REF,),
        audit_ref="audit://ios_chat_memory_index_001",
    )


def test_ios_chat_memory_export_bridge_is_read_only_reference_export() -> None:
    bridge = IOSChatMemoryExportBridge.from_store_and_index(
        bridge_id="ios_chat_memory_export_bridge_001",
        store_adapter=_store(),
        index_adapter=_index(),
        exported_record_refs=(_RECORD_REF,),
    )

    assert bridge.read_only is True
    assert bridge.reference_only_export is True
    assert bridge.includes_message_body is False
    assert bridge.includes_heavy_payload is False
    assert bridge.local_chat_memory_only is True
    assert bridge.openim_truth is False
    assert bridge.core_chat_truth is False
    assert bridge.canonical_truth is False
    assert bridge.core_write_allowed is False
    assert bridge.direct_server_write_allowed is False
    assert bridge.network_allowed is False
    assert bridge.platform_api_calls_allowed is False
    assert bridge.sync_runtime_allowed is False
    assert bridge.mutation_allowed is False


def test_ios_chat_memory_export_bridge_rejects_message_body_export() -> None:
    store = _store()
    index = _index()

    with pytest.raises(ValueError, match="includes_message_body must be False"):
        IOSChatMemoryExportBridge(
            bridge_id="bad_ios_chat_memory_export_bridge",
            store_adapter=store,
            index_adapter=index,
            device_id=store.device_id,
            app_id=store.app_id,
            owner_identity_id=store.owner_identity_id,
            ios_bundle_id=store.ios_bundle_id,
            export_scope="ios_local_chat_memory_reference_export",
            exported_record_refs=(_RECORD_REF,),
            export_manifest_ref="ref://bad_ios_chat_memory_export_bridge/manifest",
            audit_ref="audit://bad_ios_chat_memory_export_bridge",
            read_only=True,
            reference_only_export=True,
            includes_message_body=True,
            includes_heavy_payload=False,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
            mutation_allowed=False,
        )
