from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.real_node_agents import (
    build_real_node_agents_contract,
)
from MAKSIMAR_CORE_LIB.secure_sync_update_transport import (
    build_secure_sync_update_transport_contract,
)


PersistentStorageEntryId = Literal[
    "storage_dev_metadata_001",
    "storage_home_artifacts_001",
    "storage_mobile_local_state_001",
]

StorageClass = Literal[
    "metadata_store",
    "artifact_store",
    "local_proxy_store",
]

StorageAuthorityMode = Literal[
    "local_authority",
    "restricted_remote_authority",
]

MigrationMode = Literal[
    "schema_migration_required",
    "artifact_migration_required",
    "local_state_migration_required",
]

MigrationStatus = Literal[
    "migration_ready",
]

PersistenceStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^storage_[a-z][a-z0-9_]*$")
_NODE_AGENT_ID_PATTERN = re.compile(r"^nodeagent_[a-z][a-z0-9_]*$")
_TRANSPORT_ID_PATTERN = re.compile(r"^transport_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class PersistentStorageMigrationEntry:
    """Canonical persistent storage / migrations entry."""

    persistent_storage_entry_id: PersistentStorageEntryId
    storage_class: StorageClass
    linked_node_agent_id: str
    linked_transport_entry_id: str
    storage_authority_mode: StorageAuthorityMode
    migration_mode: MigrationMode
    persistent_write_allowed: bool
    runtime_state_separated: bool
    migration_manifest_required: bool
    rollback_required: bool
    explainable_required: bool
    production_path_allowed: bool
    migration_status: MigrationStatus
    persistence_status: PersistenceStatus
    description: str

    def __post_init__(self) -> None:
        """Validate persistent storage / migrations invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.persistent_storage_entry_id):
            raise ValueError(
                f"Invalid persistent_storage_entry_id: {self.persistent_storage_entry_id}"
            )

        if not _NODE_AGENT_ID_PATTERN.fullmatch(self.linked_node_agent_id):
            raise ValueError(
                f"Invalid linked_node_agent_id: {self.linked_node_agent_id}"
            )

        if not _TRANSPORT_ID_PATTERN.fullmatch(self.linked_transport_entry_id):
            raise ValueError(
                f"Invalid linked_transport_entry_id: {self.linked_transport_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.persistent_storage_entry_id}"
            )

        if not self.persistent_write_allowed:
            raise ValueError(
                f"persistent_write_allowed must be True: {self.persistent_storage_entry_id}"
            )

        if not self.runtime_state_separated:
            raise ValueError(
                f"runtime_state_separated must be True: {self.persistent_storage_entry_id}"
            )

        if not self.migration_manifest_required:
            raise ValueError(
                f"migration_manifest_required must be True: {self.persistent_storage_entry_id}"
            )

        if not self.rollback_required:
            raise ValueError(
                f"rollback_required must be True: {self.persistent_storage_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.persistent_storage_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.persistent_storage_entry_id}"
            )

        if self.migration_status != "migration_ready":
            raise ValueError(
                f"migration_status must be migration_ready: {self.persistent_storage_entry_id}"
            )

        if self.persistence_status != "defined":
            raise ValueError(
                f"persistence_status must be defined: {self.persistent_storage_entry_id}"
            )

        if self.persistent_storage_entry_id == "storage_dev_metadata_001":
            if self.storage_class != "metadata_store":
                raise ValueError(
                    "storage_dev_metadata_001 must use metadata_store"
                )
            if self.linked_node_agent_id != "nodeagent_dev_001":
                raise ValueError(
                    "storage_dev_metadata_001 must link nodeagent_dev_001"
                )
            if self.linked_transport_entry_id != "transport_dev_local_001":
                raise ValueError(
                    "storage_dev_metadata_001 must link transport_dev_local_001"
                )
            if self.storage_authority_mode != "local_authority":
                raise ValueError(
                    "storage_dev_metadata_001 must use local_authority"
                )
            if self.migration_mode != "schema_migration_required":
                raise ValueError(
                    "storage_dev_metadata_001 must use schema_migration_required"
                )

        if self.persistent_storage_entry_id == "storage_home_artifacts_001":
            if self.storage_class != "artifact_store":
                raise ValueError(
                    "storage_home_artifacts_001 must use artifact_store"
                )
            if self.linked_node_agent_id != "nodeagent_home_001":
                raise ValueError(
                    "storage_home_artifacts_001 must link nodeagent_home_001"
                )
            if self.linked_transport_entry_id != "transport_dev_home_001":
                raise ValueError(
                    "storage_home_artifacts_001 must link transport_dev_home_001"
                )
            if self.storage_authority_mode != "restricted_remote_authority":
                raise ValueError(
                    "storage_home_artifacts_001 must use restricted_remote_authority"
                )
            if self.migration_mode != "artifact_migration_required":
                raise ValueError(
                    "storage_home_artifacts_001 must use artifact_migration_required"
                )

        if self.persistent_storage_entry_id == "storage_mobile_local_state_001":
            if self.storage_class != "local_proxy_store":
                raise ValueError(
                    "storage_mobile_local_state_001 must use local_proxy_store"
                )
            if self.linked_node_agent_id != "nodeagent_mobile_001":
                raise ValueError(
                    "storage_mobile_local_state_001 must link nodeagent_mobile_001"
                )
            if self.linked_transport_entry_id != "transport_mobile_local_001":
                raise ValueError(
                    "storage_mobile_local_state_001 must link transport_mobile_local_001"
                )
            if self.storage_authority_mode != "local_authority":
                raise ValueError(
                    "storage_mobile_local_state_001 must use local_authority"
                )
            if self.migration_mode != "local_state_migration_required":
                raise ValueError(
                    "storage_mobile_local_state_001 must use local_state_migration_required"
                )


@dataclass(frozen=True, slots=True)
class PersistentStorageMigrationsContract:
    """Unified persistent storage / migrations contract."""

    total_entries: int
    local_authority_entries: int
    restricted_remote_authority_entries: int
    rollback_required_entries: int
    defined_entries: int
    entries: tuple[PersistentStorageMigrationEntry, ...]

    def __post_init__(self) -> None:
        """Validate persistent storage / migrations contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        local_authority_entries = sum(
            1 for entry in self.entries if entry.storage_authority_mode == "local_authority"
        )
        restricted_remote_authority_entries = sum(
            1
            for entry in self.entries
            if entry.storage_authority_mode == "restricted_remote_authority"
        )
        rollback_required_entries = sum(
            1 for entry in self.entries if entry.rollback_required
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.persistence_status == "defined"
        )

        if self.local_authority_entries != local_authority_entries:
            raise ValueError("local_authority_entries must match computed count")

        if self.restricted_remote_authority_entries != restricted_remote_authority_entries:
            raise ValueError(
                "restricted_remote_authority_entries must match computed count"
            )

        if self.rollback_required_entries != rollback_required_entries:
            raise ValueError("rollback_required_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.persistent_storage_entry_id for entry in self.entries)
        storage_classes = tuple(entry.storage_class for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate persistent_storage_entry_id values detected")

        if len(set(storage_classes)) != len(storage_classes):
            raise ValueError("Duplicate storage_class values detected")


def build_persistent_storage_migrations_contract() -> PersistentStorageMigrationsContract:
    """Build canonical persistent storage / migrations contract."""
    node_agent_contract = build_real_node_agents_contract()
    transport_contract = build_secure_sync_update_transport_contract()

    node_agent_ids = {entry.real_node_agent_entry_id for entry in node_agent_contract.entries}
    transport_ids = {entry.secure_transport_entry_id for entry in transport_contract.entries}

    required_node_agent_ids = {
        "nodeagent_dev_001",
        "nodeagent_home_001",
        "nodeagent_mobile_001",
    }
    required_transport_ids = {
        "transport_dev_local_001",
        "transport_dev_home_001",
        "transport_mobile_local_001",
    }

    missing_node_agent_ids = required_node_agent_ids - node_agent_ids
    if missing_node_agent_ids:
        raise ValueError(
            f"Missing node agent ids: {sorted(missing_node_agent_ids)}"
        )

    missing_transport_ids = required_transport_ids - transport_ids
    if missing_transport_ids:
        raise ValueError(
            f"Missing transport ids: {sorted(missing_transport_ids)}"
        )

    entries = (
        PersistentStorageMigrationEntry(
            persistent_storage_entry_id="storage_dev_metadata_001",
            storage_class="metadata_store",
            linked_node_agent_id="nodeagent_dev_001",
            linked_transport_entry_id="transport_dev_local_001",
            storage_authority_mode="local_authority",
            migration_mode="schema_migration_required",
            persistent_write_allowed=True,
            runtime_state_separated=True,
            migration_manifest_required=True,
            rollback_required=True,
            explainable_required=True,
            production_path_allowed=True,
            migration_status="migration_ready",
            persistence_status="defined",
            description="Canonical persistent storage entry for DEV metadata store.",
        ),
        PersistentStorageMigrationEntry(
            persistent_storage_entry_id="storage_home_artifacts_001",
            storage_class="artifact_store",
            linked_node_agent_id="nodeagent_home_001",
            linked_transport_entry_id="transport_dev_home_001",
            storage_authority_mode="restricted_remote_authority",
            migration_mode="artifact_migration_required",
            persistent_write_allowed=True,
            runtime_state_separated=True,
            migration_manifest_required=True,
            rollback_required=True,
            explainable_required=True,
            production_path_allowed=True,
            migration_status="migration_ready",
            persistence_status="defined",
            description="Canonical persistent storage entry for HOME artifact store.",
        ),
        PersistentStorageMigrationEntry(
            persistent_storage_entry_id="storage_mobile_local_state_001",
            storage_class="local_proxy_store",
            linked_node_agent_id="nodeagent_mobile_001",
            linked_transport_entry_id="transport_mobile_local_001",
            storage_authority_mode="local_authority",
            migration_mode="local_state_migration_required",
            persistent_write_allowed=True,
            runtime_state_separated=True,
            migration_manifest_required=True,
            rollback_required=True,
            explainable_required=True,
            production_path_allowed=True,
            migration_status="migration_ready",
            persistence_status="defined",
            description="Canonical persistent storage entry for MOBILE local proxy store.",
        ),
    )

    local_authority_entries = sum(
        1 for entry in entries if entry.storage_authority_mode == "local_authority"
    )
    restricted_remote_authority_entries = sum(
        1
        for entry in entries
        if entry.storage_authority_mode == "restricted_remote_authority"
    )
    rollback_required_entries = sum(
        1 for entry in entries if entry.rollback_required
    )
    defined_entries = sum(
        1 for entry in entries if entry.persistence_status == "defined"
    )

    return PersistentStorageMigrationsContract(
        total_entries=len(entries),
        local_authority_entries=local_authority_entries,
        restricted_remote_authority_entries=restricted_remote_authority_entries,
        rollback_required_entries=rollback_required_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
