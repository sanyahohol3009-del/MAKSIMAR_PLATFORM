from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy_completion import (
    build_validation_policy_completion_contract,
)


def test_validation_policy_completion_contract_builds() -> None:
    """Validation policy completion contract should build successfully."""
    contract = build_validation_policy_completion_contract()

    assert contract.total_entries == 3
    assert contract.deep_validation_entries == 1
    assert contract.payload_reference_entries == 1
    assert contract.completed_entries == 3


def test_validation_policy_completion_contract_contains_expected_chat_entry() -> None:
    """Validation policy completion should expose expected chat entry."""
    contract = build_validation_policy_completion_contract()
    entry = contract.entries[0]

    assert entry.task_class == "chat_request"
    assert entry.payload_class == "small_control"
    assert entry.required_validation_tier == "L1_HEADER"
    assert entry.effective_risk_level == "low"
    assert entry.policy_rule_id == "policy_chat_request_small_control"
    assert entry.deep_validation_required is False
    assert entry.payload_reference_required is False
    assert entry.error_code_on_failure == "invalid_header"


def test_validation_policy_completion_contract_contains_expected_simulation_entry() -> None:
    """Validation policy completion should expose expected simulation entry."""
    contract = build_validation_policy_completion_contract()
    entry = contract.entries[1]

    assert entry.task_class == "simulation_request"
    assert entry.payload_class == "medium_contract"
    assert entry.required_validation_tier == "L2_SCHEMA"
    assert entry.effective_risk_level == "medium"
    assert entry.policy_rule_id == "policy_simulation_request_medium_contract"
    assert entry.deep_validation_required is False
    assert entry.payload_reference_required is False
    assert entry.error_code_on_failure == "invalid_schema"


def test_validation_policy_completion_contract_contains_expected_robotics_entry() -> None:
    """Validation policy completion should expose expected robotics entry."""
    contract = build_validation_policy_completion_contract()
    entry = contract.entries[2]

    assert entry.task_class == "robotics_action"
    assert entry.payload_class == "heavy_artifact"
    assert entry.required_validation_tier == "L3_DEEP"
    assert entry.effective_risk_level == "critical"
    assert entry.policy_rule_id == "policy_robotics_action_heavy_artifact"
    assert entry.deep_validation_required is True
    assert entry.payload_reference_required is True
    assert entry.error_code_on_failure == "deep_validation_failed"


def test_validation_policy_completion_contract_preserves_completed_status() -> None:
    """Validation policy completion should preserve completed status."""
    contract = build_validation_policy_completion_contract()

    for entry in contract.entries:
        assert entry.completion_valid is True
        assert entry.completion_status == "completed"
