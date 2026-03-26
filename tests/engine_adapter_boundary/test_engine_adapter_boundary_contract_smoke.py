from __future__ import annotations

from MAKSIMAR_CORE_LIB.engine_adapter_boundary import (
    build_engine_adapter_boundary_contract,
)


def test_engine_adapter_boundary_contract_builds() -> None:
    """Engine adapter boundary contract should build successfully."""
    contract = build_engine_adapter_boundary_contract()

    assert contract.total_entries == 3
    assert contract.optics_linked_entries == 1
    assert contract.integration_linked_entries == 1
    assert contract.fallback_required_entries == 3
    assert contract.defined_entries == 3


def test_engine_adapter_boundary_contract_contains_expected_simulation_entry() -> None:
    """Engine adapter boundary should expose expected simulation entry."""
    contract = build_engine_adapter_boundary_contract()
    entry = contract.entries[0]

    assert entry.engine_adapter_id == "engineadapter_simulation_worker_001"
    assert entry.worker_kind == "simulation_worker"
    assert entry.contract_shape == "engine_neutral"
    assert entry.linked_optics_engine_id is None
    assert entry.linked_integration_entry_id is None


def test_engine_adapter_boundary_contract_contains_expected_optics_entry() -> None:
    """Engine adapter boundary should expose expected optics entry."""
    contract = build_engine_adapter_boundary_contract()
    entry = contract.entries[1]

    assert entry.engine_adapter_id == "engineadapter_optics_worker_001"
    assert entry.worker_kind == "optics_worker"
    assert entry.linked_optics_engine_id == "opticsengine_ar_glasses_projection_001"
    assert entry.linked_integration_entry_id is None


def test_engine_adapter_boundary_contract_contains_expected_display_entry() -> None:
    """Engine adapter boundary should expose expected display entry."""
    contract = build_engine_adapter_boundary_contract()
    entry = contract.entries[2]

    assert entry.engine_adapter_id == "engineadapter_display_transform_001"
    assert entry.worker_kind == "display_transform_runtime"
    assert entry.linked_optics_engine_id is None
    assert entry.linked_integration_entry_id == "wristdisplayint_ar_001"
