from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_task_class_contract,
)


def test_validation_task_class_contract_builds() -> None:
    """Validation task class contract should build successfully."""
    contract = build_validation_task_class_contract()

    assert contract.total_task_classes == 6
    assert len(contract.task_classes) == 6


def test_validation_task_class_contract_contains_expected_task_classes() -> None:
    """Validation task class contract should expose expected task classes."""
    contract = build_validation_task_class_contract()

    assert contract.task_classes[0].task_class == "chat_request"
    assert contract.task_classes[1].task_class == "simulation_request"
    assert contract.task_classes[2].task_class == "robotics_action"
    assert contract.task_classes[3].task_class == "media_job"
    assert contract.task_classes[4].task_class == "evaluation_job"
    assert contract.task_classes[5].task_class == "automation_job"


def test_validation_task_class_contract_preserves_progressive_risk_and_validation() -> None:
    """Validation task classes should preserve expected risk and validation defaults."""
    contract = build_validation_task_class_contract()

    chat = contract.task_classes[0]
    robotics = contract.task_classes[2]
    automation = contract.task_classes[5]

    assert chat.default_validation_tier == "L1_HEADER"
    assert chat.risk_level == "low"
    assert chat.execution_side_effects_possible is False

    assert robotics.default_validation_tier == "L3_DEEP"
    assert robotics.risk_level == "critical"
    assert robotics.deep_validation_default_required is True
    assert robotics.execution_side_effects_possible is True

    assert automation.default_validation_tier == "L3_DEEP"
    assert automation.risk_level == "high"
    assert automation.deep_validation_default_required is True
    assert automation.execution_side_effects_possible is True
