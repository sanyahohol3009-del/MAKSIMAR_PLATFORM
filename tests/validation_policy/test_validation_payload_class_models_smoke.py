from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_payload_class_contract,
)


def test_validation_payload_class_contract_builds() -> None:
    """Validation payload class contract should build successfully."""
    contract = build_validation_payload_class_contract()

    assert contract.total_payload_classes == 3
    assert len(contract.payload_classes) == 3


def test_validation_payload_class_contract_contains_expected_payload_classes() -> None:
    """Validation payload class contract should expose expected payload classes."""
    contract = build_validation_payload_class_contract()

    assert contract.payload_classes[0].payload_class == "small_control"
    assert contract.payload_classes[1].payload_class == "medium_contract"
    assert contract.payload_classes[2].payload_class == "heavy_artifact"


def test_validation_payload_class_contract_preserves_progressive_validation_rules() -> None:
    """Validation payload classes should preserve expected validation defaults."""
    contract = build_validation_payload_class_contract()

    small = contract.payload_classes[0]
    medium = contract.payload_classes[1]
    heavy = contract.payload_classes[2]

    assert small.minimum_validation_tier == "L1_HEADER"
    assert small.inline_payload_allowed is True
    assert small.payload_reference_required is False
    assert small.deep_validation_required_for_default_flow is False

    assert medium.minimum_validation_tier == "L2_SCHEMA"
    assert medium.inline_payload_allowed is True
    assert medium.payload_reference_required is False
    assert medium.deep_validation_required_for_default_flow is False

    assert heavy.minimum_validation_tier == "L2_SCHEMA"
    assert heavy.inline_payload_allowed is False
    assert heavy.payload_reference_required is True
    assert heavy.deep_validation_required_for_default_flow is True
