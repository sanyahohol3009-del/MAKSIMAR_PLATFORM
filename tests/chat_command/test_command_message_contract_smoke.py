import pytest

from MAKSIMAR_CORE_LIB.chat_command.command_message_contract import CommandMessageContract


def test_command_message_contract_smoke() -> None:
    command = CommandMessageContract(
        command_message_id="cmd_msg_001",
        source_message_id="msg_001",
        source_room_id="room_operator_001",
        source_identity_id="identity_owner_001",
        command_intent_kind="operator_request",
        normalized_intent="show_system_status",
        risk_level="low",
        control_plane_handoff_required=True,
        operator_approval_required=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert command.control_plane_handoff_required is True
    assert command.operator_approval_required is True
    assert command.direct_execution_allowed is False


def test_command_message_requires_control_plane_handoff() -> None:
    with pytest.raises(ValueError, match="control_plane_handoff_required must be True"):
        CommandMessageContract(
            command_message_id="cmd_msg_002",
            source_message_id="msg_001",
            source_room_id="room_operator_001",
            source_identity_id="identity_owner_001",
            command_intent_kind="operator_request",
            normalized_intent="show_system_status",
            risk_level="low",
            control_plane_handoff_required=False,
            operator_approval_required=True,
            direct_execution_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_command_message_never_executes_directly() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        CommandMessageContract(
            command_message_id="cmd_msg_003",
            source_message_id="msg_001",
            source_room_id="room_operator_001",
            source_identity_id="identity_owner_001",
            command_intent_kind="operator_request",
            normalized_intent="restart_runtime",
            risk_level="high",
            control_plane_handoff_required=True,
            operator_approval_required=True,
            direct_execution_allowed=True,
            runtime_mutation_allowed=False,
        )
