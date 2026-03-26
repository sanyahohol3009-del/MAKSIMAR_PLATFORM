from __future__ import annotations

from MAKSIMAR_CORE_LIB.payload_policy_hardening import (
    build_payload_policy_hardening_contract,
)


def test_payload_policy_hardening_contract_builds() -> None:
    """Payload policy hardening contract should build successfully."""
    contract = build_payload_policy_hardening_contract()

    assert contract.total_entries == 3
    assert contract.control_plane_entries == 2
    assert contract.data_plane_entries == 1
    assert contract.deep_validation_entries == 1
    assert contract.hardened_entries == 3


def test_payload_policy_hardening_contract_contains_expected_small_control_entry() -> None:
    """Payload policy hardening should expose expected small_control entry."""
    contract = build_payload_policy_hardening_contract()
    entry = contract.entries[0]

    assert entry.payload_class == "small_control"
    assert entry.route_target == "control_plane"
    assert entry.inline_payload_allowed is True
    assert entry.artifact_reference_requirement == "forbidden"
    assert entry.minimum_validation_tier == "L1_HEADER"
    assert entry.deep_validation_required_for_default_flow is False
    assert entry.control_plane_allowed is True
    assert entry.data_plane_required is False


def test_payload_policy_hardening_contract_contains_expected_medium_contract_entry() -> None:
    """Payload policy hardening should expose expected medium_contract entry."""
    contract = build_payload_policy_hardening_contract()
    entry = contract.entries[1]

    assert entry.payload_class == "medium_contract"
    assert entry.route_target == "control_plane"
    assert entry.inline_payload_allowed is True
    assert entry.artifact_reference_requirement == "optional"
    assert entry.minimum_validation_tier == "L2_SCHEMA"
    assert entry.deep_validation_required_for_default_flow is False
    assert entry.control_plane_allowed is True
    assert entry.data_plane_required is False


def test_payload_policy_hardening_contract_contains_expected_heavy_artifact_entry() -> None:
    """Payload policy hardening should expose expected heavy_artifact entry."""
    contract = build_payload_policy_hardening_contract()
    entry = contract.entries[2]

    assert entry.payload_class == "heavy_artifact"
    assert entry.route_target == "data_plane"
    assert entry.inline_payload_allowed is False
    assert entry.artifact_reference_requirement == "required"
    assert entry.minimum_validation_tier == "L2_SCHEMA"
    assert entry.deep_validation_required_for_default_flow is True
    assert entry.control_plane_allowed is False
    assert entry.data_plane_required is True


def test_payload_policy_hardening_contract_preserves_hardened_status() -> None:
    """Payload policy hardening should preserve hardened split validity."""
    contract = build_payload_policy_hardening_contract()

    for entry in contract.entries:
        assert entry.split_valid is True
        assert entry.policy_status == "hardened"
