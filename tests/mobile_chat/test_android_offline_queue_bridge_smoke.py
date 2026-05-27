import pytest

from ANDROID_SHELL.chat_client.offline_queue_bridge import (
    AndroidOfflineQueueBridge,
    AndroidOfflineQueueBridgeEntry,
)


def test_android_offline_queue_bridge_smoke() -> None:
    queue = AndroidOfflineQueueBridge()
    entry = AndroidOfflineQueueBridgeEntry(
        delivery_id="delivery_001",
        message_id="msg_001",
        target_room_id="room_family_001",
        queue_state="queued_local",
        bounded_retry_required=True,
        wake_lock_allowed=False,
        direct_mobile_api_execution_allowed=False,
        external_network_access_allowed=False,
    )

    queue.enqueue(entry)
    updated = queue.mark_waiting_for_server("delivery_001")

    assert updated.queue_state == "waiting_for_server"
    assert updated.wake_lock_allowed is False
    assert updated.external_network_access_allowed is False


def test_android_offline_queue_bridge_rejects_wake_lock() -> None:
    with pytest.raises(ValueError, match="wake_lock_allowed must be False"):
        AndroidOfflineQueueBridgeEntry(
            delivery_id="delivery_bad",
            message_id="msg_001",
            target_room_id="room_family_001",
            queue_state="queued_local",
            bounded_retry_required=True,
            wake_lock_allowed=True,
            direct_mobile_api_execution_allowed=False,
            external_network_access_allowed=False,
        )
