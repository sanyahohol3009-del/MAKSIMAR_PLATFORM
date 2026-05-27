import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_session_read_model import ChatSessionReadModel


def test_chat_session_read_model_smoke() -> None:
    model = ChatSessionReadModel(
        read_model_id="chat_session_rm_001",
        session_id="session_001",
        room_id="room_operator_001",
        participant_count=2,
        session_state="active",
        unread_count=1,
        pending_outbound_count=0,
        dashboard_read_only=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
        canonical_truth_write_allowed=False,
    )

    assert model.session_state == "active"
    assert model.dashboard_read_only is True


def test_chat_session_read_model_rejects_zero_participants() -> None:
    with pytest.raises(ValueError, match="participant_count must be greater than zero"):
        ChatSessionReadModel(
            read_model_id="chat_session_rm_bad",
            session_id="session_001",
            room_id="room_operator_001",
            participant_count=0,
            session_state="active",
            unread_count=0,
            pending_outbound_count=0,
            dashboard_read_only=True,
            direct_execution_allowed=False,
            runtime_mutation_allowed=False,
            canonical_truth_write_allowed=False,
        )
