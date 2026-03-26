from __future__ import annotations

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_error_contract,
)


def test_validation_error_contract_builds() -> None:
    """Validation error contract should build successfully."""
    contract = build_validation_error_contract()

    assert contract.total_errors == 6
    assert len(contract.errors) == 6


def test_validation_error_contract_contains_expected_error_codes() -> None:
    """Validation error contract should expose expected validation error codes."""
    contract = build_validation_error_contract()

    error_codes = {entry.error_code for entry in contract.errors}

    assert "invalid_header" in error_codes
    assert "invalid_schema" in error_codes
    assert "forbidden_payload_embedding" in error_codes
    assert "missing_payload_reference" in error_codes
    assert "deep_validation_failed" in error_codes
    assert "policy_rule_not_found" in error_codes


def test_validation_error_contract_preserves_expected_severity_and_terminality() -> None:
    """Validation errors should preserve expected severity and terminal semantics."""
    contract = build_validation_error_contract()
    errors_by_code = {entry.error_code: entry for entry in contract.errors}

    invalid_header = errors_by_code["invalid_header"]
    invalid_schema = errors_by_code["invalid_schema"]
    deep_validation_failed = errors_by_code["deep_validation_failed"]
    policy_rule_not_found = errors_by_code["policy_rule_not_found"]

    assert invalid_header.category == "header"
    assert invalid_header.severity == "medium"
    assert invalid_header.retryable is False
    assert invalid_header.terminal is True

    assert invalid_schema.category == "schema"
    assert invalid_schema.severity == "high"
    assert invalid_schema.retryable is False
    assert invalid_schema.terminal is True

    assert deep_validation_failed.category == "deep_validation"
    assert deep_validation_failed.severity == "critical"
    assert deep_validation_failed.retryable is False
    assert deep_validation_failed.terminal is True

    assert policy_rule_not_found.category == "policy"
    assert policy_rule_not_found.severity == "critical"
    assert policy_rule_not_found.retryable is False
    assert policy_rule_not_found.terminal is True
