from __future__ import annotations

from MAKSIMAR_CORE_LIB.payload_policy_models import (
    build_payload_class_contract,
)


def test_payload_class_contract_builds() -> None:
    """Payload class contract should build successfully."""
    contract = build_payload_class_contract()

    assert contract.total_classes == 3
    assert len(contract.classes) == 3


def test_payload_class_contract_contains_expected_classes() -> None:
    """Payload class contract should expose expected payload classes."""
    contract = build_payload_class_contract()

    assert contract.classes[0].payload_class == "small_control"
    assert contract.classes[1].payload_class == "medium_contract"
    assert contract.classes[2].payload_class == "heavy_artifact"


def test_payload_class_contract_enforces_heavy_artifact_reference() -> None:
    """Heavy artifact payload should require reference-based routing."""
    contract = build_payload_class_contract()

    heavy = contract.classes[2]

    assert heavy.routing_direction == "data_plane"
    assert heavy.embedding_policy == "reference_required"
    assert heavy.max_inline_size_kb == 0
