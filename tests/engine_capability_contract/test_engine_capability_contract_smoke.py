from __future__ import annotations

from MAKSIMAR_CORE_LIB.engine_capability_contract import (
    build_engine_capability_contract,
)


def test_engine_capability_contract_builds() -> None:
    """Engine capability contract should build successfully."""
    contract = build_engine_capability_contract()

    assert contract.total_entries == 3
    assert contract.hybrid_runtime_entries == 2
    assert contract.interactive_latency_entries == 2
    assert contract.fallback_available_entries == 3
    assert contract.defined_entries == 3


def test_engine_capability_contract_contains_expected_simulation_entry() -> None:
    """Engine capability contract should expose expected simulation entry."""
    contract = build_engine_capability_contract()
    entry = contract.entries[0]

    assert entry.engine_capability_id == "enginecap_simulation_001"
    assert entry.linked_engine_adapter_id == "engineadapter_simulation_worker_001"
    assert entry.engine_kind == "simulation_engine"
    assert entry.language_runtime == "hybrid"
    assert entry.supported_workloads == ("simulation_workload",)
    assert entry.latency_profile == "bounded_realtime"


def test_engine_capability_contract_contains_expected_optics_entry() -> None:
    """Engine capability contract should expose expected optics entry."""
    contract = build_engine_capability_contract()
    entry = contract.entries[1]

    assert entry.engine_capability_id == "enginecap_optics_001"
    assert entry.linked_engine_adapter_id == "engineadapter_optics_worker_001"
    assert entry.engine_kind == "optics_engine"
    assert entry.language_runtime == "hybrid"
    assert entry.supported_workloads == ("optics_workload",)
    assert entry.latency_profile == "interactive"


def test_engine_capability_contract_contains_expected_display_entry() -> None:
    """Engine capability contract should expose expected display entry."""
    contract = build_engine_capability_contract()
    entry = contract.entries[2]

    assert entry.engine_capability_id == "enginecap_display_transform_001"
    assert entry.linked_engine_adapter_id == "engineadapter_display_transform_001"
    assert entry.engine_kind == "display_transform_engine"
    assert entry.language_runtime == "python"
    assert entry.supported_workloads == ("display_transform_workload",)
    assert entry.latency_profile == "interactive"
