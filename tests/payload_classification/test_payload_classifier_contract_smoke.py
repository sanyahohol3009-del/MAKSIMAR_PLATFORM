from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.payload_classification import (
    build_server_payload_classification_contract,
)


def test_server_payload_classification_contract_builds() -> None:
    """Server-side payload classification contract should build successfully."""
    contract = build_server_payload_classification_contract()

    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_server_payload_classification_detects_expected_classes() -> None:
    """Server-side payload classification should detect expected payload classes."""
    contract = build_server_payload_classification_contract()

    assert contract.entries[0].detected_payload_class == "small_control"
    assert contract.entries[1].detected_payload_class == "medium_contract"
    assert contract.entries[2].detected_payload_class == "heavy_artifact"


def test_server_payload_classification_routes_heavy_artifact_to_data_plane() -> None:
    """Server-side payload classification should route heavy artifact to data plane."""
    contract = build_server_payload_classification_contract()

    heavy = contract.entries[2]

    assert heavy.route_target == "data_plane"
    assert heavy.inline_allowed is False
    assert heavy.valid is True
    assert heavy.classification_reason == "payload_policy_valid"
