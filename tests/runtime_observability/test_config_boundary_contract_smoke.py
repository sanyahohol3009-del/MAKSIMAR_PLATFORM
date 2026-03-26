from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_typed_config_boundary_contract,
)


def test_typed_config_boundary_contract_builds() -> None:
    """Typed config boundary contract should build successfully."""
    contract = build_typed_config_boundary_contract()

    assert contract.total_entries == 5
    assert len(contract.entries) == 5


def test_typed_config_boundary_contains_runtime_and_feature_flags() -> None:
    """Typed config boundary should include runtime and feature_flag scopes."""
    contract = build_typed_config_boundary_contract()

    scopes = {entry.scope for entry in contract.entries}

    assert "runtime" in scopes
    assert "feature_flag" in scopes
    assert "environment" in scopes
