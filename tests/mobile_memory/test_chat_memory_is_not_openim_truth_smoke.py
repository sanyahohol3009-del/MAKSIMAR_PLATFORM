import pytest

from shared_mobile_core.chat_memory import ChatMemoryIndexContract, ChatMemoryRecordContract


def _valid_record_kwargs() -> dict:
    return {
        "record_id": "chat-memory-record-1",
        "chat_id": "chat-1",
        "conversation_id": "conversation-1",
        "message_id": "message-1",
        "device_id": "device-1",
        "owner_identity_id": "owner-1",
        "participant_identity_refs": ("identity://owner-1", "identity://peer-1"),
        "message_ref": "chat-memory://device-1/messages/message-1",
        "created_at": "2026-05-28T10:00:00Z",
        "updated_at": "2026-05-28T10:01:00Z",
        "schema_version": "chat_memory_record.v1",
        "privacy_classification": "conversation_private",
        "retention_policy_id": "chat-retention-1",
        "encryption_policy_id": "chat-encryption-1",
        "sync_eligible": True,
        "sync_requires_policy": True,
        "offline_replay_eligible": True,
        "audit_ref": "audit://chat-memory-record-1",
        "local_chat_memory_only": True,
        "openim_truth": False,
        "core_chat_truth": False,
        "canonical_truth": False,
        "core_write_allowed": False,
        "direct_server_write_allowed": False,
    }


def test_chat_memory_record_rejects_truth_claims() -> None:
    for field_name in ("openim_truth", "core_chat_truth", "canonical_truth"):
        kwargs = _valid_record_kwargs()
        kwargs[field_name] = True

        with pytest.raises(ValueError):
            ChatMemoryRecordContract(**kwargs)


def test_chat_memory_record_rejects_inline_message_body() -> None:
    kwargs = _valid_record_kwargs()
    kwargs["message_ref"] = "inline:hello from a full message body"

    with pytest.raises(ValueError):
        ChatMemoryRecordContract(**kwargs)


def test_chat_memory_index_rejects_message_body_or_payload_storage() -> None:
    with pytest.raises(ValueError):
        ChatMemoryIndexContract(
            index_id="chat-index-1",
            device_id="device-1",
            owner_identity_id="owner-1",
            indexed_record_refs=("chat-memory://device-1/records/chat-memory-record-1",),
            index_scope="local_mobile_chat_memory",
            supports_offline_search=True,
            stores_message_body=True,
            stores_heavy_payload=False,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            rebuild_requires_policy=True,
            audit_ref="audit://chat-index-1",
        )

    with pytest.raises(ValueError):
        ChatMemoryIndexContract(
            index_id="chat-index-2",
            device_id="device-1",
            owner_identity_id="owner-1",
            indexed_record_refs=("chat-memory://device-1/records/chat-memory-record-2",),
            index_scope="local_mobile_chat_memory",
            supports_offline_search=True,
            stores_message_body=False,
            stores_heavy_payload=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            rebuild_requires_policy=True,
            audit_ref="audit://chat-index-2",
        )
