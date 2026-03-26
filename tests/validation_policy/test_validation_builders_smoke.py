from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_error_entry,
    build_validation_plan,
)


def test_validation_plan_builder_builds_chat_small_control() -> None:
    """Validation plan builder should resolve chat_request + small_control."""
    plan = build_validation_plan(
        task_class="chat_request",
        payload_class="small_control",
    )

    assert plan.rule_id == "policy_chat_request_small_control"
    assert plan.required_validation_tier == "L1_HEADER"
    assert plan.effective_risk_level == "low"
    assert plan.header_validation_required is True
    assert plan.schema_validation_required is False
    assert plan.deep_validation_required is False
    assert plan.payload_reference_enforcement_required is False
    assert plan.execution_side_effects_possible is False


def test_validation_plan_builder_builds_robotics_heavy_artifact() -> None:
    """Validation plan builder should resolve robotics_action + heavy_artifact."""
    plan = build_validation_plan(
        task_class="robotics_action",
        payload_class="heavy_artifact",
    )

    assert plan.rule_id == "policy_robotics_action_heavy_artifact"
    assert plan.required_validation_tier == "L3_DEEP"
    assert plan.effective_risk_level == "critical"
    assert plan.header_validation_required is True
    assert plan.schema_validation_required is True
    assert plan.deep_validation_required is True
    assert plan.payload_reference_enforcement_required is True
    assert plan.execution_side_effects_possible is True


def test_validation_error_builder_builds_policy_error_entry() -> None:
    """Validation error builder should resolve canonical error entry."""
    error = build_validation_error_entry(
        error_code="policy_rule_not_found",
    )

    assert error.error_code == "policy_rule_not_found"
    assert error.category == "policy"
    assert error.severity == "critical"
    assert error.retryable is False
    assert error.terminal is True
