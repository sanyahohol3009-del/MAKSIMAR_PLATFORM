from __future__ import annotations

from MAKSIMAR_CORE_LIB.end_to_end_orchestration_runtime import (
    build_end_to_end_orchestration_runtime_contract,
)


def test_end_to_end_orchestration_runtime_contract_builds() -> None:
    """End-to-end orchestration runtime contract should build successfully."""
    contract = build_end_to_end_orchestration_runtime_contract()

    assert contract.total_entries == 3
    assert contract.backend_required_entries == 2
    assert contract.local_flow_entries == 2
    assert contract.restricted_flow_entries == 1
    assert contract.active_entries == 3


def test_end_to_end_orchestration_runtime_contract_contains_expected_control_entry() -> None:
    """End-to-end orchestration should expose expected control entry."""
    contract = build_end_to_end_orchestration_runtime_contract()
    entry = contract.entries[0]

    assert entry.orchestration_entry_id == "orchestration_control_plane_001"
    assert entry.workload_class == "control_plane_workload"
    assert entry.linked_node_agent_id == "nodeagent_dev_001"
    assert entry.linked_real_backend_id is None
    assert entry.orchestration_flow_class == "local_control_flow"


def test_end_to_end_orchestration_runtime_contract_contains_expected_heavy_entry() -> None:
    """End-to-end orchestration should expose expected heavy entry."""
    contract = build_end_to_end_orchestration_runtime_contract()
    entry = contract.entries[1]

    assert entry.orchestration_entry_id == "orchestration_heavy_execution_001"
    assert entry.workload_class == "heavy_execution_workload"
    assert entry.linked_node_agent_id == "nodeagent_home_001"
    assert entry.linked_real_backend_id == "realbackend_simulation_native_001"
    assert entry.orchestration_flow_class == "restricted_execution_flow"


def test_end_to_end_orchestration_runtime_contract_contains_expected_mobile_entry() -> None:
    """End-to-end orchestration should expose expected mobile entry."""
    contract = build_end_to_end_orchestration_runtime_contract()
    entry = contract.entries[2]

    assert entry.orchestration_entry_id == "orchestration_mobile_entry_001"
    assert entry.workload_class == "mobile_entry_workload"
    assert entry.linked_node_agent_id == "nodeagent_mobile_001"
    assert entry.linked_real_backend_id == "realbackend_display_python_001"
    assert entry.orchestration_flow_class == "local_mobile_flow"
