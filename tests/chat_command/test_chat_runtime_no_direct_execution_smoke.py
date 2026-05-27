from MAKSIMAR_CORE_LIB.chat_command.chat_message_contract import ChatMessageContract
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.chat_session_registry import ChatSessionRecord
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.message_router_runtime import MessageRouterRuntime


def test_chat_runtime_no_direct_execution_smoke() -> None:
    session = ChatSessionRecord(
        session_id="session_no_exec",
        room_id="room_operator_001",
        participant_identity_ids=("identity_owner_001", "identity_jarvis_001"),
        session_state="active",
        command_execution_allowed=False,
        external_network_access_allowed=False,
        canonical_write_allowed=False,
    )
    message = ChatMessageContract(
        message_id="msg_no_exec",
        room_id="room_operator_001",
        sender_identity_id="identity_owner_001",
        message_kind="command_intent",
        text_payload="restart runtime",
        message_state="accepted",
        created_at_utc="2026-05-27T20:00:00Z",
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )
    decision = MessageRouterRuntime().route_message(message)

    assert session.command_execution_allowed is False
    assert session.external_network_access_allowed is False
    assert decision.route_target == "command_review_queue"
    assert decision.direct_execution_allowed is False
    assert decision.runtime_command_execution_allowed is False
