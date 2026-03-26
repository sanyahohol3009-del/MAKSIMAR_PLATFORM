from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.full_test_suite import (
    build_full_test_suite_contract,
)
from MAKSIMAR_CORE_LIB.persistent_storage_migrations import (
    build_persistent_storage_migrations_contract,
)
from MAKSIMAR_CORE_LIB.real_node_agents import (
    build_real_node_agents_contract,
)
from MAKSIMAR_CORE_LIB.secure_sync_update_transport import (
    build_secure_sync_update_transport_contract,
)


OpsEntryId = Literal[
    "ops_dev_control_001",
    "ops_home_execution_001",
    "ops_mobile_proxy_001",
]

OpsDomain = Literal[
    "deployment_domain",
    "backup_incident_domain",
    "mobile_operations_domain",
]

DeploymentMode = Literal[
    "local_control_deploy",
    "restricted_execution_deploy",
    "local_mobile_deploy",
]

BackupMode = Literal[
    "metadata_backup_restore_ready",
    "artifact_backup_restore_ready",
    "local_state_backup_restore_ready",
]

IncidentMode = Literal[
    "control_incident_ready",
    "execution_incident_ready",
    "mobile_incident_ready",
]

OpsStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^ops_[a-z][a-z0-9_]*$")
_AGENT_ID_PATTERN = re.compile(r"^nodeagent_[a-z][a-z0-9_]*$")
_STORAGE_ID_PATTERN = re.compile(r"^storage_[a-z][a-z0-9_]*$")
_TRANSPORT_ID_PATTERN = re.compile(r"^transport_[a-z][a-z0-9_]*$")
_TEST_ID_PATTERN = re.compile(r"^fulltest_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class OperationsDeploymentBackupIncidentsEntry:
    """Canonical operations / deployment / backup / incidents entry."""

    ops_entry_id: OpsEntryId
    ops_domain: OpsDomain
    linked_node_agent_id: str
    linked_storage_entry_id: str
    linked_transport_entry_id: str
    linked_full_test_entry_id: str
    deployment_mode: DeploymentMode
    backup_mode: BackupMode
    incident_mode: IncidentMode
    restore_ready_required: bool
    incident_snapshot_required: bool
    explainable_required: bool
    production_path_allowed: bool
    ops_status: OpsStatus
    description: str

    def __post_init__(self) -> None:
        """Validate operations / deployment / backup / incidents invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.ops_entry_id):
            raise ValueError(f"Invalid ops_entry_id: {self.ops_entry_id}")

        if not _AGENT_ID_PATTERN.fullmatch(self.linked_node_agent_id):
            raise ValueError(
                f"Invalid linked_node_agent_id: {self.linked_node_agent_id}"
            )

        if not _STORAGE_ID_PATTERN.fullmatch(self.linked_storage_entry_id):
            raise ValueError(
                f"Invalid linked_storage_entry_id: {self.linked_storage_entry_id}"
            )

        if not _TRANSPORT_ID_PATTERN.fullmatch(self.linked_transport_entry_id):
            raise ValueError(
                f"Invalid linked_transport_entry_id: {self.linked_transport_entry_id}"
            )

        if not _TEST_ID_PATTERN.fullmatch(self.linked_full_test_entry_id):
            raise ValueError(
                f"Invalid linked_full_test_entry_id: {self.linked_full_test_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.ops_entry_id}")

        if not self.restore_ready_required:
            raise ValueError(
                f"restore_ready_required must be True: {self.ops_entry_id}"
            )

        if not self.incident_snapshot_required:
            raise ValueError(
                f"incident_snapshot_required must be True: {self.ops_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.ops_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.ops_entry_id}"
            )

        if self.ops_status != "defined":
            raise ValueError(f"ops_status must be defined: {self.ops_entry_id}")

        if self.ops_entry_id == "ops_dev_control_001":
            if self.ops_domain != "deployment_domain":
                raise ValueError("ops_dev_control_001 must use deployment_domain")
            if self.linked_node_agent_id != "nodeagent_dev_001":
                raise ValueError("ops_dev_control_001 must link nodeagent_dev_001")
            if self.linked_storage_entry_id != "storage_dev_metadata_001":
                raise ValueError("ops_dev_control_001 must link storage_dev_metadata_001")
            if self.linked_transport_entry_id != "transport_dev_local_001":
                raise ValueError("ops_dev_control_001 must link transport_dev_local_001")
            if self.linked_full_test_entry_id != "fulltest_orchestration_001":
                raise ValueError("ops_dev_control_001 must link fulltest_orchestration_001")
            if self.deployment_mode != "local_control_deploy":
                raise ValueError("ops_dev_control_001 must use local_control_deploy")
            if self.backup_mode != "metadata_backup_restore_ready":
                raise ValueError(
                    "ops_dev_control_001 must use metadata_backup_restore_ready"
                )
            if self.incident_mode != "control_incident_ready":
                raise ValueError("ops_dev_control_001 must use control_incident_ready")

        if self.ops_entry_id == "ops_home_execution_001":
            if self.ops_domain != "backup_incident_domain":
                raise ValueError("ops_home_execution_001 must use backup_incident_domain")
            if self.linked_node_agent_id != "nodeagent_home_001":
                raise ValueError("ops_home_execution_001 must link nodeagent_home_001")
            if self.linked_storage_entry_id != "storage_home_artifacts_001":
                raise ValueError("ops_home_execution_001 must link storage_home_artifacts_001")
            if self.linked_transport_entry_id != "transport_dev_home_001":
                raise ValueError("ops_home_execution_001 must link transport_dev_home_001")
            if self.linked_full_test_entry_id != "fulltest_orchestration_001":
                raise ValueError("ops_home_execution_001 must link fulltest_orchestration_001")
            if self.deployment_mode != "restricted_execution_deploy":
                raise ValueError(
                    "ops_home_execution_001 must use restricted_execution_deploy"
                )
            if self.backup_mode != "artifact_backup_restore_ready":
                raise ValueError(
                    "ops_home_execution_001 must use artifact_backup_restore_ready"
                )
            if self.incident_mode != "execution_incident_ready":
                raise ValueError(
                    "ops_home_execution_001 must use execution_incident_ready"
                )

        if self.ops_entry_id == "ops_mobile_proxy_001":
            if self.ops_domain != "mobile_operations_domain":
                raise ValueError("ops_mobile_proxy_001 must use mobile_operations_domain")
            if self.linked_node_agent_id != "nodeagent_mobile_001":
                raise ValueError("ops_mobile_proxy_001 must link nodeagent_mobile_001")
            if self.linked_storage_entry_id != "storage_mobile_local_state_001":
                raise ValueError(
                    "ops_mobile_proxy_001 must link storage_mobile_local_state_001"
                )
            if self.linked_transport_entry_id != "transport_mobile_local_001":
                raise ValueError("ops_mobile_proxy_001 must link transport_mobile_local_001")
            if self.linked_full_test_entry_id != "fulltest_clients_voice_001":
                raise ValueError("ops_mobile_proxy_001 must link fulltest_clients_voice_001")
            if self.deployment_mode != "local_mobile_deploy":
                raise ValueError("ops_mobile_proxy_001 must use local_mobile_deploy")
            if self.backup_mode != "local_state_backup_restore_ready":
                raise ValueError(
                    "ops_mobile_proxy_001 must use local_state_backup_restore_ready"
                )
            if self.incident_mode != "mobile_incident_ready":
                raise ValueError("ops_mobile_proxy_001 must use mobile_incident_ready")


@dataclass(frozen=True, slots=True)
class OperationsDeploymentBackupIncidentsContract:
    """Unified operations / deployment / backup / incidents contract."""

    total_entries: int
    deployment_domain_entries: int
    backup_incident_domain_entries: int
    mobile_operations_domain_entries: int
    defined_entries: int
    entries: tuple[OperationsDeploymentBackupIncidentsEntry, ...]

    def __post_init__(self) -> None:
        """Validate operations / deployment / backup / incidents contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        deployment_domain_entries = sum(
            1 for entry in self.entries if entry.ops_domain == "deployment_domain"
        )
        backup_incident_domain_entries = sum(
            1 for entry in self.entries if entry.ops_domain == "backup_incident_domain"
        )
        mobile_operations_domain_entries = sum(
            1 for entry in self.entries if entry.ops_domain == "mobile_operations_domain"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.ops_status == "defined"
        )

        if self.deployment_domain_entries != deployment_domain_entries:
            raise ValueError("deployment_domain_entries must match computed count")

        if self.backup_incident_domain_entries != backup_incident_domain_entries:
            raise ValueError(
                "backup_incident_domain_entries must match computed count"
            )

        if self.mobile_operations_domain_entries != mobile_operations_domain_entries:
            raise ValueError(
                "mobile_operations_domain_entries must match computed count"
            )

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.ops_entry_id for entry in self.entries)
        domains = tuple(entry.ops_domain for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate ops_entry_id values detected")

        if len(set(domains)) != len(domains):
            raise ValueError("Duplicate ops_domain values detected")


def build_operations_deployment_backup_incidents_contract() -> OperationsDeploymentBackupIncidentsContract:
    """Build canonical operations / deployment / backup / incidents contract."""
    node_agents = build_real_node_agents_contract()
    storage = build_persistent_storage_migrations_contract()
    transport = build_secure_sync_update_transport_contract()
    full_tests = build_full_test_suite_contract()

    node_agent_ids = {entry.real_node_agent_entry_id for entry in node_agents.entries}
    storage_ids = {entry.persistent_storage_entry_id for entry in storage.entries}
    transport_ids = {entry.secure_transport_entry_id for entry in transport.entries}
    full_test_ids = {entry.full_test_entry_id for entry in full_tests.entries}

    required_node_agent_ids = {
        "nodeagent_dev_001",
        "nodeagent_home_001",
        "nodeagent_mobile_001",
    }
    required_storage_ids = {
        "storage_dev_metadata_001",
        "storage_home_artifacts_001",
        "storage_mobile_local_state_001",
    }
    required_transport_ids = {
        "transport_dev_local_001",
        "transport_dev_home_001",
        "transport_mobile_local_001",
    }
    required_full_test_ids = {
        "fulltest_orchestration_001",
        "fulltest_clients_voice_001",
    }

    for label, required, actual in (
        ("node agent ids", required_node_agent_ids, node_agent_ids),
        ("storage ids", required_storage_ids, storage_ids),
        ("transport ids", required_transport_ids, transport_ids),
        ("full test ids", required_full_test_ids, full_test_ids),
    ):
        missing = required - actual
        if missing:
            raise ValueError(f"Missing {label}: {sorted(missing)}")

    entries = (
        OperationsDeploymentBackupIncidentsEntry(
            ops_entry_id="ops_dev_control_001",
            ops_domain="deployment_domain",
            linked_node_agent_id="nodeagent_dev_001",
            linked_storage_entry_id="storage_dev_metadata_001",
            linked_transport_entry_id="transport_dev_local_001",
            linked_full_test_entry_id="fulltest_orchestration_001",
            deployment_mode="local_control_deploy",
            backup_mode="metadata_backup_restore_ready",
            incident_mode="control_incident_ready",
            restore_ready_required=True,
            incident_snapshot_required=True,
            explainable_required=True,
            production_path_allowed=True,
            ops_status="defined",
            description="Canonical operations entry for DEV control deployment path.",
        ),
        OperationsDeploymentBackupIncidentsEntry(
            ops_entry_id="ops_home_execution_001",
            ops_domain="backup_incident_domain",
            linked_node_agent_id="nodeagent_home_001",
            linked_storage_entry_id="storage_home_artifacts_001",
            linked_transport_entry_id="transport_dev_home_001",
            linked_full_test_entry_id="fulltest_orchestration_001",
            deployment_mode="restricted_execution_deploy",
            backup_mode="artifact_backup_restore_ready",
            incident_mode="execution_incident_ready",
            restore_ready_required=True,
            incident_snapshot_required=True,
            explainable_required=True,
            production_path_allowed=True,
            ops_status="defined",
            description="Canonical operations entry for HOME execution backup/incident path.",
        ),
        OperationsDeploymentBackupIncidentsEntry(
            ops_entry_id="ops_mobile_proxy_001",
            ops_domain="mobile_operations_domain",
            linked_node_agent_id="nodeagent_mobile_001",
            linked_storage_entry_id="storage_mobile_local_state_001",
            linked_transport_entry_id="transport_mobile_local_001",
            linked_full_test_entry_id="fulltest_clients_voice_001",
            deployment_mode="local_mobile_deploy",
            backup_mode="local_state_backup_restore_ready",
            incident_mode="mobile_incident_ready",
            restore_ready_required=True,
            incident_snapshot_required=True,
            explainable_required=True,
            production_path_allowed=True,
            ops_status="defined",
            description="Canonical operations entry for MOBILE proxy deployment path.",
        ),
    )

    deployment_domain_entries = sum(
        1 for entry in entries if entry.ops_domain == "deployment_domain"
    )
    backup_incident_domain_entries = sum(
        1 for entry in entries if entry.ops_domain == "backup_incident_domain"
    )
    mobile_operations_domain_entries = sum(
        1 for entry in entries if entry.ops_domain == "mobile_operations_domain"
    )
    defined_entries = sum(
        1 for entry in entries if entry.ops_status == "defined"
    )

    return OperationsDeploymentBackupIncidentsContract(
        total_entries=len(entries),
        deployment_domain_entries=deployment_domain_entries,
        backup_incident_domain_entries=backup_incident_domain_entries,
        mobile_operations_domain_entries=mobile_operations_domain_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
