import pytest

from MAKSIMAR_CORE_LIB.chat_command.offline_delivery_contract import OfflineDeliveryContract
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.offline_queue_runtime import (
    OfflineQueueEntry,
    OfflineQueueRuntime,
)


def test_offline_queue_runtime_smoke() -> None:
    queue = OfflineQueueRuntime()
    delivery = OfflineDeliveryContract(
        delivery_id="delivery_001",
        message_id="msg_001",
        target_identity_id="identity_family_001",
        target_device_id="android_device_001",
        delivery_state="queued_offline",
        retry_policy="bounded",
        max_retry_count=3,
        server_sync_required=True,
        external_network_access_allowed=False,
        direct_mobile_api_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    entry = queue.enqueue_delivery(delivery)

    assert entry.queue_state == "queued"
    assert queue.get_entry("delivery_001") == entry


def test_offline_queue_runtime_rejects_direct_mobile_api() -> None:
    with pytest.raises(ValueError, match="direct_mobile_api_execution_allowed must be False"):
        OfflineQueueEntry(
            delivery_id="delivery_bad",
            message_id="msg_001",
            target_device_id="android_device_001",
            queue_state="queued",
            wake_device_allowed=False,
            external_network_access_allowed=False,
            direct_mobile_api_execution_allowed=True,
        )


def test_offline_queue_runtime_marks_delivered_reference_only() -> None:
    queue = OfflineQueueRuntime()
    queue.enqueue_delivery(
        OfflineDeliveryContract(
            delivery_id="delivery_002",
            message_id="msg_002",
            target_identity_id="identity_family_001",
            target_device_id="ios_device_001",
            delivery_state="queued_offline",
            retry_policy="bounded",
            max_retry_count=2,
            server_sync_required=True,
            external_network_access_allowed=False,
            direct_mobile_api_execution_allowed=False,
            runtime_mutation_allowed=False,
        )
    )

    delivered = queue.mark_delivered_reference("delivery_002")

    assert delivered.queue_state == "delivered_reference"
    assert delivered.external_network_access_allowed is False
