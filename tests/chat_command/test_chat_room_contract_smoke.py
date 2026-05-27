import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_room_contract import ChatRoomContract


def test_chat_room_contract_smoke() -> None:
    room = ChatRoomContract(
        room_id="room_operator_001",
        room_kind="operator",
        room_mode="private",
        participant_identity_ids=("identity_owner_001", "identity_jarvis_001"),
        command_intents_allowed=True,
        direct_execution_allowed=False,
    )

    assert room.room_id == "room_operator_001"
    assert room.command_intents_allowed is True
    assert room.direct_execution_allowed is False


def test_chat_room_rejects_duplicate_participants() -> None:
    with pytest.raises(ValueError, match="must not contain duplicates"):
        ChatRoomContract(
            room_id="room_bad",
            room_kind="operator",
            room_mode="private",
            participant_identity_ids=("identity_owner_001", "identity_owner_001"),
            command_intents_allowed=True,
            direct_execution_allowed=False,
        )


def test_external_adapter_room_cannot_allow_command_intents() -> None:
    with pytest.raises(ValueError, match="external adapter rooms must not allow command intents"):
        ChatRoomContract(
            room_id="room_openim_bridge",
            room_kind="adapter_bridge",
            room_mode="read_only_bridge",
            participant_identity_ids=("identity_openim_adapter",),
            command_intents_allowed=True,
            direct_execution_allowed=False,
            external_adapter_room=True,
        )
