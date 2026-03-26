from __future__ import annotations

from MAKSIMAR_CORE_LIB.backend_selection_policy import (
    build_backend_selection_policy_contract,
)


def test_backend_selection_policy_contract_builds() -> None:
    """Backend selection policy contract should build successfully."""
    contract = build_backend_selection_policy_contract()

    assert contract.total_entries == 3
    assert contract.gpu_selected_entries == 1
    assert contract.native_selected_entries == 1
    assert contract.fallback_path_entries == 1
    assert contract.defined_entries == 3


def test_backend_selection_policy_contract_contains_expected_simulation_entry() -> None:
    """Backend selection policy should expose expected simulation entry."""
    contract = build_backend_selection_policy_contract()
    entry = contract.entries[0]

    assert entry.backend_policy_id == "backendpolicy_simulation_001"
    assert entry.linked_engine_capability_id == "enginecap_simulation_001"
    assert entry.selected_backend_slot == "native_backend_slot"
    assert entry.latency_sensitivity == "bounded_realtime"
    assert entry.degraded_mode == "normal_path"


def test_backend_selection_policy_contract_contains_expected_optics_entry() -> None:
    """Backend selection policy should expose expected optics entry."""
    contract = build_backend_selection_policy_contract()
    entry = contract.entries[1]

    assert entry.backend_policy_id == "backendpolicy_optics_001"
    assert entry.linked_engine_capability_id == "enginecap_optics_001"
    assert entry.selected_backend_slot == "gpu_backend_slot"
    assert entry.latency_sensitivity == "interactive"
    assert entry.degraded_mode == "normal_path"


def test_backend_selection_policy_contract_contains_expected_display_entry() -> None:
    """Backend selection policy should expose expected display entry."""
    contract = build_backend_selection_policy_contract()
    entry = contract.entries[2]

    assert entry.backend_policy_id == "backendpolicy_display_transform_001"
    assert entry.linked_engine_capability_id == "enginecap_display_transform_001"
    assert entry.selected_backend_slot == "python_backend_slot"
    assert entry.latency_sensitivity == "interactive"
    assert entry.degraded_mode == "fallback_path"
