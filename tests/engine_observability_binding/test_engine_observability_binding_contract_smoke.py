from __future__ import annotations

from MAKSIMAR_CORE_LIB.engine_observability_binding import (
    build_engine_observability_binding_contract,
)


def test_engine_observability_binding_contract_builds() -> None:
    """Engine observability binding contract should build successfully."""
    contract = build_engine_observability_binding_contract()

    assert contract.total_entries == 3
    assert contract.gpu_selected_entries == 1
    assert contract.fallback_active_entries == 1
    assert contract.interactive_latency_entries == 2
    assert contract.defined_entries == 3


def test_engine_observability_binding_contract_contains_expected_simulation_entry() -> None:
    """Engine observability binding should expose expected simulation entry."""
    contract = build_engine_observability_binding_contract()
    entry = contract.entries[0]

    assert entry.observability_entry_id == "engineobs_simulation_001"
    assert entry.linked_backend_policy_id == "backendpolicy_simulation_001"
    assert entry.selected_backend_slot == "native_backend_slot"
    assert entry.latency_path_class == "bounded_realtime_path"
    assert entry.fallback_active is False
    assert entry.mismatch_condition == "none"


def test_engine_observability_binding_contract_contains_expected_optics_entry() -> None:
    """Engine observability binding should expose expected optics entry."""
    contract = build_engine_observability_binding_contract()
    entry = contract.entries[1]

    assert entry.observability_entry_id == "engineobs_optics_001"
    assert entry.linked_backend_policy_id == "backendpolicy_optics_001"
    assert entry.selected_backend_slot == "gpu_backend_slot"
    assert entry.latency_path_class == "interactive_path"
    assert entry.fallback_active is False
    assert entry.mismatch_condition == "none"


def test_engine_observability_binding_contract_contains_expected_display_entry() -> None:
    """Engine observability binding should expose expected display entry."""
    contract = build_engine_observability_binding_contract()
    entry = contract.entries[2]

    assert entry.observability_entry_id == "engineobs_display_transform_001"
    assert entry.linked_backend_policy_id == "backendpolicy_display_transform_001"
    assert entry.selected_backend_slot == "python_backend_slot"
    assert entry.latency_path_class == "fallback_interactive_path"
    assert entry.fallback_active is True
    assert entry.mismatch_condition == "fallback_active"
