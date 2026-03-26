from __future__ import annotations

from MAKSIMAR_CORE_LIB.persistent_storage_migrations import (
    build_persistent_storage_migrations_contract,
)


def test_persistent_storage_migrations_contract_builds() -> None:
    """Persistent storage migrations contract should build successfully."""
    contract = build_persistent_storage_migrations_contract()

    assert contract.total_entries == 3
    assert contract.local_authority_entries == 2
    assert contract.restricted_remote_authority_entries == 1
    assert contract.rollback_required_entries == 3
    assert contract.defined_entries == 3


def test_persistent_storage_migrations_contract_contains_expected_dev_entry() -> None:
    """Persistent storage migrations should expose expected DEV entry."""
    contract = build_persistent_storage_migrations_contract()
    entry = contract.entries[0]

    assert entry.persistent_storage_entry_id == "storage_dev_metadata_001"
    assert entry.storage_class == "metadata_store"
    assert entry.linked_node_agent_id == "nodeagent_dev_001"
    assert entry.storage_authority_mode == "local_authority"
    assert entry.migration_mode == "schema_migration_required"


def test_persistent_storage_migrations_contract_contains_expected_home_entry() -> None:
    """Persistent storage migrations should expose expected HOME entry."""
    contract = build_persistent_storage_migrations_contract()
    entry = contract.entries[1]

    assert entry.persistent_storage_entry_id == "storage_home_artifacts_001"
    assert entry.storage_class == "artifact_store"
    assert entry.linked_node_agent_id == "nodeagent_home_001"
    assert entry.storage_authority_mode == "restricted_remote_authority"
    assert entry.migration_mode == "artifact_migration_required"


def test_persistent_storage_migrations_contract_contains_expected_mobile_entry() -> None:
    """Persistent storage migrations should expose expected MOBILE entry."""
    contract = build_persistent_storage_migrations_contract()
    entry = contract.entries[2]

    assert entry.persistent_storage_entry_id == "storage_mobile_local_state_001"
    assert entry.storage_class == "local_proxy_store"
    assert entry.linked_node_agent_id == "nodeagent_mobile_001"
    assert entry.storage_authority_mode == "local_authority"
    assert entry.migration_mode == "local_state_migration_required"
