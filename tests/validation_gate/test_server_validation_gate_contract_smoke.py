from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate import (
    build_server_validation_gate_contract,
)


def test_server_validation_gate_contract_builds() -> None:
    """Server validation gate contract should build successfully."""
    contract = build_server_validation_gate_contract()

    assert contract.total_entries == 4
    assert contract.passed_entries == 3
    assert contract.rejected_entries == 1


def test_server_validation_gate_contract_contains_expected_validation_paths() -> None:
    """Server validation gate contract should expose expected validation paths."""
    contract = build_server_validation_gate_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    third = contract.entries[2]

    assert first.request_id == "val_req_001"
    assert first.resolved_validation_tier == "L1_HEADER"
    assert first.l1_header_passed is True
    assert first.l2_schema_passed is False
    assert first.l3_deep_passed is False
    assert first.final_status == "passed"

    assert second.request_id == "val_req_002"
    assert second.resolved_validation_tier == "L2_SCHEMA"
    assert second.l1_header_passed is True
    assert second.l2_schema_passed is True
    assert second.l3_deep_passed is True
    assert second.final_status == "passed"

    assert third.request_id == "val_req_003"
    assert third.resolved_validation_tier == "L3_DEEP"
    assert third.l1_header_passed is True
    assert third.l2_schema_passed is True
    assert third.l3_deep_passed is True
    assert third.final_status == "passed"


def test_server_validation_gate_contract_rejects_failed_deep_validation() -> None:
    """Server validation gate contract should reject failed deep validation path."""
    contract = build_server_validation_gate_contract()

    last = contract.entries[-1]

    assert last.request_id == "val_req_004"
    assert last.resolved_validation_tier == "L3_DEEP"
    assert last.l1_header_passed is True
    assert last.l2_schema_passed is True
    assert last.l3_deep_passed is False
    assert last.final_status == "rejected"
    assert last.blocking_error_code == "deep_validation_failed"
