import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_to_command_handoff_contract import ChatToCommandHandoffContract


def test_chat_to_command_handoff_contract_smoke() -> None:
    handoff = ChatToCommandHandoffContract(
        handoff_id="handoff_001",
        source_message_id="msg_001",
        source_room_id="room_operator_001",
        source_identity_id="identity_owner_001",
        source_channel="chat_message",
        normalized_intent="show_system_status",
        control_plane_target="proposal_engine",
        handoff_state="policy_review_required",
        policy_review_required=True,
        operator_approval_required=True,
        sandbox_required=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
        external_adapter_execution_allowed=False,
    )

    assert handoff.policy_review_required is True
    assert handoff.operator_approval_required is True
    assert handoff.direct_execution_allowed is False


def test_chat_to_command_handoff_requires_policy_review() -> None:
    with pytest.raises(ValueError, match="policy_review_required must be True"):
        ChatToCommandHandoffContract(
            handoff_id="handoff_bad",
            source_message_id="msg_001",
            source_room_id="room_operator_001",
            source_identity_id="identity_owner_001",
            source_channel="chat_message",
            normalized_intent="restart_runtime",
            control_plane_target="proposal_engine",
            handoff_state="policy_review_required",
            policy_review_required=False,
            operator_approval_required=True,
            sandbox_required=True,
            direct_execution_allowed=False,
            runtime_mutation_allowed=False,
            external_adapter_execution_allowed=False,
        )


def test_chat_to_command_handoff_never_executes_directly() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        ChatToCommandHandoffContract(
            handoff_id="handoff_exec",
            source_message_id="msg_001",
            source_room_id="room_operator_001",
            source_identity_id="identity_owner_001",
            source_channel="chat_message",
            normalized_intent="restart_runtime",
            control_plane_target="proposal_engine",
            handoff_state="policy_review_required",
            policy_review_required=True,
            operator_approval_required=True,
            sandbox_required=True,
            direct_execution_allowed=True,
            runtime_mutation_allowed=False,
            external_adapter_execution_allowed=False,
        )
