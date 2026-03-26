from __future__ import annotations

from MAKSIMAR_CORE_LIB.payload_routing_contract import (
    build_payload_routing_contract,
)


def test_payload_routing_contract_builds() -> None:
    """Payload routing contract should build successfully."""
    contract = build_payload_routing_contract()

    assert contract.total_rules == 3
    assert len(contract.rules) == 3


def test_payload_routing_contract_contains_expected_classes() -> None:
    """Payload routing contract should expose expected payload classes."""
    contract = build_payload_routing_contract()

    assert contract.rules[0].payload_class == "small_control"
    assert contract.rules[1].payload_class == "medium_contract"
    assert contract.rules[2].payload_class == "heavy_artifact"


def test_payload_routing_contract_enforces_reference_for_heavy_artifact() -> None:
    """Heavy artifact must be routed through data plane by reference."""
    contract = build_payload_routing_contract()

    heavy = contract.rules[2]

    assert heavy.route_target == "data_plane"
    assert heavy.artifact_reference_requirement == "required"
    assert heavy.owner_task_id_required is True
    assert heavy.artifact_size_declaration_required is True
    assert heavy.max_inline_size_kb == 0
