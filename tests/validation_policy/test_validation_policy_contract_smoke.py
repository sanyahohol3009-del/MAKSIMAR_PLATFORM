from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_policy_contract,
)


def test_validation_policy_contract_builds() -> None:
    """Validation policy contract should build successfully."""
    contract = build_validation_policy_contract()

    assert contract.total_rules == 12
    assert len(contract.rules) == 12


def test_validation_policy_contract_contains_expected_rule_ids() -> None:
    """Validation policy contract should expose expected rule ids."""
    contract = build_validation_policy_contract()

    rule_ids = {entry.rule_id for entry in contract.rules}

    assert "policy_chat_request_small_control" in rule_ids
    assert "policy_chat_request_medium_contract" in rule_ids
    assert "policy_simulation_request_heavy_artifact" in rule_ids
    assert "policy_robotics_action_heavy_artifact" in rule_ids
    assert "policy_automation_job_heavy_artifact" in rule_ids


def test_validation_policy_contract_preserves_expected_validation_defaults() -> None:
    """Validation policy contract should preserve strict validation defaults."""
    contract = build_validation_policy_contract()
    rules_by_id = {entry.rule_id: entry for entry in contract.rules}

    chat_small = rules_by_id["policy_chat_request_small_control"]
    sim_heavy = rules_by_id["policy_simulation_request_heavy_artifact"]
    robotics_heavy = rules_by_id["policy_robotics_action_heavy_artifact"]
    automation_heavy = rules_by_id["policy_automation_job_heavy_artifact"]

    assert chat_small.required_validation_tier == "L1_HEADER"
    assert chat_small.effective_risk_level == "low"
    assert chat_small.payload_reference_enforcement_required is False
    assert chat_small.deep_validation_required is False
    assert chat_small.execution_side_effects_possible is False

    assert sim_heavy.required_validation_tier == "L2_SCHEMA"
    assert sim_heavy.effective_risk_level == "high"
    assert sim_heavy.payload_reference_enforcement_required is True
    assert sim_heavy.deep_validation_required is True
    assert sim_heavy.execution_side_effects_possible is False

    assert robotics_heavy.required_validation_tier == "L3_DEEP"
    assert robotics_heavy.effective_risk_level == "critical"
    assert robotics_heavy.payload_reference_enforcement_required is True
    assert robotics_heavy.deep_validation_required is True
    assert robotics_heavy.execution_side_effects_possible is True

    assert automation_heavy.required_validation_tier == "L3_DEEP"
    assert automation_heavy.effective_risk_level == "high"
    assert automation_heavy.payload_reference_enforcement_required is True
    assert automation_heavy.deep_validation_required is True
    assert automation_heavy.execution_side_effects_possible is True
