from shared_mobile_core.chat_memory import ChatMemoryIndexContract


def test_chat_memory_index_contract_stores_references_only() -> None:
    index = ChatMemoryIndexContract.local_chat_index(
        index_id="chat-index-1",
        device_id="device-1",
        owner_identity_id="owner-1",
        indexed_record_refs=("chat-memory://device-1/records/chat-memory-record-1",),
        audit_ref="audit://chat-index-1",
    )

    assert index.supports_offline_search is True
    assert index.stores_message_body is False
    assert index.stores_heavy_payload is False
    assert index.local_chat_memory_only is True
    assert index.openim_truth is False
    assert index.core_chat_truth is False
    assert index.canonical_truth is False
    assert index.rebuild_requires_policy is True
