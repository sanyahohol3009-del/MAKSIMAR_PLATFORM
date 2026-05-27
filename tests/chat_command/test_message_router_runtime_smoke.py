from MAKSIMAR_CORE_LIB.chat_command.chat_message_contract import ChatMessageContract
from MAKSIMAR_SERVER.CHAT_COMMAND_RUNTIME.message_router_runtime import MessageRouterRuntime


def test_message_router_runtime_routes_normal_message() -> None:
    router = MessageRouterRuntime()
    message = ChatMessageContract(
        message_id="msg_001",
        room_id="room_operator_001",
        sender_identity_id="identity_owner_001",
        message_kind="human_text",
        text_payload="Покажи статус",
        message_state="accepted",
        created_at_utc="2026-05-27T20:00:00Z",
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    decision = router.route_message(message)

    assert decision.route_target == "message_reference_store"
    assert decision.command_review_required is False
    assert decision.direct_execution_allowed is False


def test_message_router_runtime_routes_command_intent_to_review() -> None:
    router = MessageRouterRuntime()
    message = ChatMessageContract(
        message_id="msg_cmd_001",
        room_id="room_operator_001",
        sender_identity_id="identity_owner_001",
        message_kind="command_intent",
        text_payload="restart runtime",
        message_state="accepted",
        created_at_utc="2026-05-27T20:00:00Z",
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    decision = router.route_message(message)

    assert decision.route_target == "command_review_queue"
    assert decision.command_review_required is True
    assert decision.runtime_command_execution_allowed is False
