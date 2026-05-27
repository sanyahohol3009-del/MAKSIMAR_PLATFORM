import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_system_read_model import ChatSystemReadModel


def test_chat_system_read_model_smoke() -> None:
    model = ChatSystemReadModel(
        read_model_id="chat_system_rm_001",
        system_state="online_reference",
        active_session_count=2,
        queued_message_count=3,
        blocked_message_count=0,
        file_transfer_count=1,
        dashboard_read_only=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
        canonical_truth_write_allowed=False,
    )

    assert model.dashboard_read_only is True
    assert model.direct_execution_allowed is False


def test_chat_system_read_model_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        ChatSystemReadModel(
            read_model_id="chat_system_rm_bad",
            system_state="online_reference",
            active_session_count=0,
            queued_message_count=0,
            blocked_message_count=0,
            file_transfer_count=0,
            dashboard_read_only=True,
            direct_execution_allowed=True,
            runtime_mutation_allowed=False,
            canonical_truth_write_allowed=False,
        )
