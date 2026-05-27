import pytest

from ANDROID_SHELL.chat_client.chat_message_store import (
    AndroidChatMessageStore,
    AndroidChatMessageStoreEntry,
)


def test_android_chat_message_store_smoke() -> None:
    store = AndroidChatMessageStore()
    entry = AndroidChatMessageStoreEntry(
        local_message_id="local_msg_001",
        room_id="room_operator_001",
        sender_identity_id="identity_owner_001",
        text_preview="Покажи статус",
        message_state="queued_local",
        encrypted_at_rest=True,
        plaintext_persistence_allowed=False,
        canonical_truth_write_allowed=False,
        external_network_access_allowed=False,
    )

    store.add_entry(entry)

    assert store.get_entry("local_msg_001") == entry
    assert store.list_entries() == (entry,)


def test_android_chat_message_store_rejects_plaintext_persistence() -> None:
    with pytest.raises(ValueError, match="plaintext_persistence_allowed must be False"):
        AndroidChatMessageStoreEntry(
            local_message_id="local_msg_bad",
            room_id="room_operator_001",
            sender_identity_id="identity_owner_001",
            text_preview="secret",
            message_state="queued_local",
            encrypted_at_rest=True,
            plaintext_persistence_allowed=True,
            canonical_truth_write_allowed=False,
            external_network_access_allowed=False,
        )
