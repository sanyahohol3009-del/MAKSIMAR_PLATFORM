from shared_mobile_core.chat_memory import ChatMemoryRecordContract


def test_chat_memory_record_contract_is_local_reference_only() -> None:
    record = ChatMemoryRecordContract.local_message_reference(
        record_id="chat-memory-record-1",
        chat_id="chat-1",
        conversation_id="conversation-1",
        message_id="message-1",
        device_id="device-1",
        owner_identity_id="owner-1",
        participant_identity_refs=("identity://owner-1", "identity://peer-1"),
        message_ref="chat-memory://device-1/messages/message-1",
        created_at="2026-05-28T10:00:00Z",
        updated_at="2026-05-28T10:01:00Z",
        retention_policy_id="chat-retention-1",
        encryption_policy_id="chat-encryption-1",
        audit_ref="audit://chat-memory-record-1",
    )

    assert record.local_chat_memory_only is True
    assert record.openim_truth is False
    assert record.core_chat_truth is False
    assert record.canonical_truth is False
    assert record.core_write_allowed is False
    assert record.direct_server_write_allowed is False
    assert record.sync_requires_policy is True
    assert record.offline_replay_eligible is True
