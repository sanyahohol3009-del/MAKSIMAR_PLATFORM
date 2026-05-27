import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_message_contract import ChatMessageContract


def test_chat_message_contract_smoke() -> None:
    message = ChatMessageContract(
        message_id="msg_001",
        room_id="room_operator_001",
        sender_identity_id="identity_owner_001",
        message_kind="human_text",
        text_payload="Покажи статус системы",
        message_state="accepted",
        created_at_utc="2026-05-27T20:00:00Z",
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert message.message_kind == "human_text"
    assert message.direct_execution_allowed is False
    assert message.runtime_mutation_allowed is False


def test_chat_message_rejects_runtime_mutation() -> None:
    with pytest.raises(ValueError, match="runtime_mutation_allowed must be False"):
        ChatMessageContract(
            message_id="msg_bad",
            room_id="room_operator_001",
            sender_identity_id="identity_owner_001",
            message_kind="human_text",
            text_payload="mutate runtime",
            message_state="accepted",
            created_at_utc="2026-05-27T20:00:00Z",
            direct_execution_allowed=False,
            runtime_mutation_allowed=True,
        )


def test_command_intent_message_is_not_delivered_as_execution() -> None:
    with pytest.raises(ValueError, match="command_intent messages must not be delivered"):
        ChatMessageContract(
            message_id="msg_cmd_001",
            room_id="room_operator_001",
            sender_identity_id="identity_owner_001",
            message_kind="command_intent",
            text_payload="restart service",
            message_state="delivered",
            created_at_utc="2026-05-27T20:00:00Z",
            direct_execution_allowed=False,
            runtime_mutation_allowed=False,
        )
