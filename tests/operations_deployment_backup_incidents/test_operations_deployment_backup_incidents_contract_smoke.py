from __future__ import annotations

from MAKSIMAR_CORE_LIB.operations_deployment_backup_incidents import (
    build_operations_deployment_backup_incidents_contract,
)


def test_operations_deployment_backup_incidents_contract_builds() -> None:
    """Operations / deployment / backup / incidents contract should build successfully."""
    contract = build_operations_deployment_backup_incidents_contract()

    assert contract.total_entries == 3
    assert contract.deployment_domain_entries == 1
    assert contract.backup_incident_domain_entries == 1
    assert contract.mobile_operations_domain_entries == 1
    assert contract.defined_entries == 3


def test_operations_deployment_backup_incidents_contract_contains_expected_dev_entry() -> None:
    """Operations contract should expose expected DEV entry."""
    contract = build_operations_deployment_backup_incidents_contract()
    entry = contract.entries[0]

    assert entry.ops_entry_id == "ops_dev_control_001"
    assert entry.ops_domain == "deployment_domain"
    assert entry.linked_node_agent_id == "nodeagent_dev_001"
    assert entry.backup_mode == "metadata_backup_restore_ready"


def test_operations_deployment_backup_incidents_contract_contains_expected_home_entry() -> None:
    """Operations contract should expose expected HOME entry."""
    contract = build_operations_deployment_backup_incidents_contract()
    entry = contract.entries[1]

    assert entry.ops_entry_id == "ops_home_execution_001"
    assert entry.ops_domain == "backup_incident_domain"
    assert entry.linked_node_agent_id == "nodeagent_home_001"
    assert entry.backup_mode == "artifact_backup_restore_ready"


def test_operations_deployment_backup_incidents_contract_contains_expected_mobile_entry() -> None:
    """Operations contract should expose expected MOBILE entry."""
    contract = build_operations_deployment_backup_incidents_contract()
    entry = contract.entries[2]

    assert entry.ops_entry_id == "ops_mobile_proxy_001"
    assert entry.ops_domain == "mobile_operations_domain"
    assert entry.linked_node_agent_id == "nodeagent_mobile_001"
    assert entry.backup_mode == "local_state_backup_restore_ready"
