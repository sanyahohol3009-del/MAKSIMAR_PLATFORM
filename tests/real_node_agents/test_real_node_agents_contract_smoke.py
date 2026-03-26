from __future__ import annotations

from MAKSIMAR_CORE_LIB.real_node_agents import (
    build_real_node_agents_contract,
)


def test_real_node_agents_contract_builds() -> None:
    """Real node agents contract should build successfully."""
    contract = build_real_node_agents_contract()

    assert contract.total_entries == 3
    assert contract.control_agent_entries == 1
    assert contract.execution_agent_entries == 1
    assert contract.mobile_proxy_agent_entries == 1
    assert contract.active_entries == 3


def test_real_node_agents_contract_contains_expected_dev_entry() -> None:
    """Real node agents should expose expected DEV entry."""
    contract = build_real_node_agents_contract()
    entry = contract.entries[0]

    assert entry.real_node_agent_entry_id == "nodeagent_dev_001"
    assert entry.node_id == "dev_001"
    assert entry.node_agent_class == "control_agent"
    assert entry.agent_runtime_mode == "control_runtime"
    assert entry.linked_transport_entry_id == "transport_dev_local_001"


def test_real_node_agents_contract_contains_expected_home_entry() -> None:
    """Real node agents should expose expected HOME entry."""
    contract = build_real_node_agents_contract()
    entry = contract.entries[1]

    assert entry.real_node_agent_entry_id == "nodeagent_home_001"
    assert entry.node_id == "home_001"
    assert entry.node_agent_class == "execution_agent"
    assert entry.agent_runtime_mode == "execution_runtime"
    assert entry.linked_real_backend_entry_id == "realbackend_simulation_native_001"


def test_real_node_agents_contract_contains_expected_mobile_entry() -> None:
    """Real node agents should expose expected MOBILE entry."""
    contract = build_real_node_agents_contract()
    entry = contract.entries[2]

    assert entry.real_node_agent_entry_id == "nodeagent_mobile_001"
    assert entry.node_id == "mobile_001"
    assert entry.node_agent_class == "mobile_proxy_agent"
    assert entry.agent_runtime_mode == "proxy_runtime"
    assert entry.linked_real_backend_entry_id == "realbackend_display_python_001"
