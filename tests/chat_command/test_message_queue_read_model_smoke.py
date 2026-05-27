import pytest

from MAKSIMAR_CORE_LIB.chat_command.message_queue_read_model import MessageQueueReadModel


def test_message_queue_read_model_smoke() -> None:
    model = MessageQueueReadModel(
        read_model_id="message_queue_rm_001",
        queue_state="active",
        queued_count=4,
        waiting_for_sync_count=1,
        blocked_count=0,
        oldest_message_age_seconds=12,
        dashboard_read_only=True,
        direct_delivery_allowed=False,
        external_network_access_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert model.queued_count == 4
    assert model.direct_delivery_allowed is False


def test_message_queue_read_model_rejects_external_network() -> None:
    with pytest.raises(ValueError, match="external_network_access_allowed must be False"):
        MessageQueueReadModel(
            read_model_id="message_queue_rm_bad",
            queue_state="active",
            queued_count=1,
            waiting_for_sync_count=0,
            blocked_count=0,
            oldest_message_age_seconds=0,
            dashboard_read_only=True,
            direct_delivery_allowed=False,
            external_network_access_allowed=True,
            runtime_mutation_allowed=False,
        )
