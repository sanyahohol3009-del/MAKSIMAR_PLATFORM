import pytest

from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.chat_session_registry import (
    ChatSessionRecord,
    ChatSessionRegistry,
)


def test_chat_session_registry_smoke() -> None:
    registry = ChatSessionRegistry()
    record = ChatSessionRecord(
        session_id="session_001",
        room_id="room_operator_001",
        participant_identity_ids=("identity_owner_001", "identity_jarvis_001"),
        session_state="active",
        command_execution_allowed=False,
        external_network_access_allowed=False,
        canonical_write_allowed=False,
    )

    registry.register_session(record)

    assert registry.get_session("session_001") == record
    assert registry.list_sessions() == (record,)


def test_chat_session_registry_rejects_command_execution() -> None:
    with pytest.raises(ValueError, match="command_execution_allowed must be False"):
        ChatSessionRecord(
            session_id="session_bad",
            room_id="room_operator_001",
            participant_identity_ids=("identity_owner_001",),
            session_state="active",
            command_execution_allowed=True,
            external_network_access_allowed=False,
            canonical_write_allowed=False,
        )


def test_chat_session_registry_closes_session_without_execution() -> None:
    registry = ChatSessionRegistry()
    registry.register_session(
        ChatSessionRecord(
            session_id="session_002",
            room_id="room_operator_001",
            participant_identity_ids=("identity_owner_001",),
            session_state="active",
            command_execution_allowed=False,
            external_network_access_allowed=False,
            canonical_write_allowed=False,
        )
    )

    closed = registry.close_session("session_002")

    assert closed.session_state == "closed"
    assert closed.command_execution_allowed is False
