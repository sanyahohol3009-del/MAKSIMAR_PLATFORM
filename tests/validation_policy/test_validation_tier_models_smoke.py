from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_tier_contract,
)


def test_validation_tier_contract_builds() -> None:
    """Validation tier contract should build successfully."""
    contract = build_validation_tier_contract()

    assert contract.total_tiers == 3
    assert len(contract.tiers) == 3


def test_validation_tier_contract_contains_expected_tiers() -> None:
    """Validation tier contract should expose expected validation tiers."""
    contract = build_validation_tier_contract()

    assert contract.tiers[0].tier_id == "L1_HEADER"
    assert contract.tiers[1].tier_id == "L2_SCHEMA"
    assert contract.tiers[2].tier_id == "L3_DEEP"


def test_validation_tier_contract_preserves_progressive_validation_semantics() -> None:
    """Validation tiers should progress monotonically from header to deep validation."""
    contract = build_validation_tier_contract()

    l1 = contract.tiers[0]
    l2 = contract.tiers[1]
    l3 = contract.tiers[2]

    assert l1.header_validation_required is True
    assert l1.schema_validation_required is False
    assert l1.deep_validation_required is False
    assert l1.payload_reference_enforcement_required is False

    assert l2.header_validation_required is True
    assert l2.schema_validation_required is True
    assert l2.deep_validation_required is False
    assert l2.payload_reference_enforcement_required is True

    assert l3.header_validation_required is True
    assert l3.schema_validation_required is True
    assert l3.deep_validation_required is True
    assert l3.payload_reference_enforcement_required is True
