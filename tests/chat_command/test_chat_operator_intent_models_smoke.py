import pytest

from MAKSIMAR_CORE_LIB.chat_command.chat_operator_intent_models import ChatOperatorIntentModel


def test_chat_operator_intent_model_smoke() -> None:
    model = ChatOperatorIntentModel(
        intent_id="intent_001",
        source_message_id="msg_001",
        source_surface="chat_dashboard",
        normalized_intent="show runtime status",
        intent_state="approval_required",
        risk_level="low",
        policy_review_required=True,
        operator_approval_required=True,
        control_plane_handoff_required=True,
        sandbox_required=True,
        direct_execution_allowed=False,
        runtime_mutation_allowed=False,
    )

    assert model.policy_review_required is True
    assert model.direct_execution_allowed is False


def test_chat_operator_intent_model_rejects_missing_approval() -> None:
    with pytest.raises(ValueError, match="operator_approval_required must be True"):
        ChatOperatorIntentModel(
            intent_id="intent_bad",
            source_message_id="msg_001",
            source_surface="chat_dashboard",
            normalized_intent="restart runtime",
            intent_state="approval_required",
            risk_level="medium",
            policy_review_required=True,
            operator_approval_required=False,
            control_plane_handoff_required=True,
            sandbox_required=True,
            direct_execution_allowed=False,
            runtime_mutation_allowed=False,
        )


def test_chat_operator_intent_model_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        ChatOperatorIntentModel(
            intent_id="intent_exec_bad",
            source_message_id="msg_001",
            source_surface="operator_button",
            normalized_intent="restart runtime",
            intent_state="approval_required",
            risk_level="high",
            policy_review_required=True,
            operator_approval_required=True,
            control_plane_handoff_required=True,
            sandbox_required=True,
            direct_execution_allowed=True,
            runtime_mutation_allowed=False,
        )
