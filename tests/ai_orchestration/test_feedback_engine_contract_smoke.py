from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.feedback_engine_contract import (
    FeedbackEngineContract,
    build_default_feedback_engine_contract,
)


def test_default_feedback_engine_contract_is_read_model_input_only() -> None:
    contract = build_default_feedback_engine_contract()

    assert contract.feedback_id == "feedback_engine_contract_v1"
    assert contract.feedback_read_model_input_only is True
    assert contract.feedback_ready is True
    assert contract.autonomous_learning_mutation_allowed is False
    assert contract.runtime_model_update_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.dashboard_safe is True
    assert contract.read_only is True


def test_feedback_engine_contract_rejects_autonomous_learning_mutation() -> None:
    with pytest.raises(ValueError, match="autonomous_learning_mutation_allowed"):
        FeedbackEngineContract(
            feedback_id="bad",
            feedback_source="operator",
            feedback_reference="ref",
            feedback_read_model_input_only=True,
            feedback_ready=True,
            autonomous_learning_mutation_allowed=True,
            runtime_model_update_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_feedback_engine_contract_rejects_runtime_model_update() -> None:
    with pytest.raises(ValueError, match="runtime_model_update_allowed"):
        FeedbackEngineContract(
            feedback_id="bad",
            feedback_source="operator",
            feedback_reference="ref",
            feedback_read_model_input_only=True,
            feedback_ready=True,
            autonomous_learning_mutation_allowed=False,
            runtime_model_update_allowed=True,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
