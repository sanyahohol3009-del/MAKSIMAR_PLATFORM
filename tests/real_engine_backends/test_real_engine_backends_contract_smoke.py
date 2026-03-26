from __future__ import annotations

from MAKSIMAR_CORE_LIB.real_engine_backends import (
    build_real_engine_backends_contract,
)


def test_real_engine_backends_contract_builds() -> None:
    """Real engine backends contract should build successfully."""
    contract = build_real_engine_backends_contract()

    assert contract.total_entries == 3
    assert contract.native_runtime_entries == 1
    assert contract.gpu_runtime_entries == 1
    assert contract.fallback_class_entries == 1
    assert contract.active_entries == 3


def test_real_engine_backends_contract_contains_expected_simulation_entry() -> None:
    """Real engine backends should expose expected simulation backend."""
    contract = build_real_engine_backends_contract()
    entry = contract.entries[0]

    assert entry.real_backend_entry_id == "realbackend_simulation_native_001"
    assert entry.linked_engine_capability_id == "enginecap_simulation_001"
    assert entry.linked_backend_policy_id == "backendpolicy_simulation_001"
    assert entry.backend_runtime_kind == "native_runtime"
    assert entry.selected_backend_slot == "native_backend_slot"


def test_real_engine_backends_contract_contains_expected_optics_entry() -> None:
    """Real engine backends should expose expected optics backend."""
    contract = build_real_engine_backends_contract()
    entry = contract.entries[1]

    assert entry.real_backend_entry_id == "realbackend_optics_gpu_001"
    assert entry.linked_engine_capability_id == "enginecap_optics_001"
    assert entry.linked_backend_policy_id == "backendpolicy_optics_001"
    assert entry.backend_runtime_kind == "gpu_runtime"
    assert entry.selected_backend_slot == "gpu_backend_slot"


def test_real_engine_backends_contract_contains_expected_display_entry() -> None:
    """Real engine backends should expose expected display backend."""
    contract = build_real_engine_backends_contract()
    entry = contract.entries[2]

    assert entry.real_backend_entry_id == "realbackend_display_python_001"
    assert entry.linked_engine_capability_id == "enginecap_display_transform_001"
    assert entry.linked_backend_policy_id == "backendpolicy_display_transform_001"
    assert entry.backend_runtime_kind == "python_runtime"
    assert entry.selected_backend_slot == "python_backend_slot"
