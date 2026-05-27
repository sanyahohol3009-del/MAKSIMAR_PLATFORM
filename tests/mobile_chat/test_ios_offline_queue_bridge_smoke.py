import pytest

from IOS_SHELL.chat_client.offline_queue_bridge import (
    IOSOfflineQueueBridge,
    IOSOfflineQueueBridgeEntry,
)


def test_ios_offline_queue_bridge_smoke() -> None:
    queue = IOSOfflineQueueBridge()
    entry = IOSOfflineQueueBridgeEntry(
        delivery_id="delivery_001",
        message_id="msg_001",
        target_room_id="room_family_001",
        queue_state="queued_local",
        bounded_retry_required=True,
        background_task_allowed=False,
        direct_mobile_api_execution_allowed=False,
        external_network_access_allowed=False,
    )

    queue.enqueue(entry)
    updated = queue.mark_waiting_for_server("delivery_001")

    assert updated.queue_state == "waiting_for_server"
    assert updated.background_task_allowed is False
    assert updated.external_network_access_allowed is False


def test_ios_offline_queue_bridge_rejects_background_task() -> None:
    with pytest.raises(ValueError, match="background_task_allowed must be False"):
        IOSOfflineQueueBridgeEntry(
            delivery_id="delivery_bad",
            message_id="msg_001",
            target_room_id="room_family_001",
            queue_state="queued_local",
            bounded_retry_required=True,
            background_task_allowed=True,
            direct_mobile_api_execution_allowed=False,
            external_network_access_allowed=False,
        )
