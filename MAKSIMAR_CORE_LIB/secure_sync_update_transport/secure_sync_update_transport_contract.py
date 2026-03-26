from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.distributed_lease_artifact_routing import (
    build_distributed_lease_artifact_routing_contract,
)
from MAKSIMAR_CORE_LIB.network_trust_boundaries import (
    build_network_trust_boundaries_contract,
)
from MAKSIMAR_CORE_LIB.node_topology_runtime import (
    build_node_topology_runtime_contract,
)


SecureTransportEntryId = Literal[
    "transport_dev_local_001",
    "transport_dev_home_001",
    "transport_mobile_local_001",
]

TransportClass = Literal[
    "local_control_transport",
    "restricted_update_transport",
    "local_mobile_transport",
]

SourceNodeId = Literal[
    "dev_001",
    "mobile_001",
]

TargetNodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

TransportMode = Literal[
    "local_same_node_transport",
    "restricted_cross_node_transport",
]

ApprovalMode = Literal[
    "no_extra_approval",
    "approval_required",
]

EncryptionMode = Literal[
    "local_process_boundary",
    "restricted_encrypted_transport",
]

TransportStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^transport_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_ROUTE_ID_PATTERN = re.compile(r"^leaseartifact_[a-z][a-z0-9_]*$")
_BOUNDARY_ID_PATTERN = re.compile(r"^trustboundary_[a-z][a-z0-9_]*$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class SecureSyncUpdateTransportEntry:
    """Canonical secure sync / update transport entry."""

    secure_transport_entry_id: SecureTransportEntryId
    transport_class: TransportClass
    source_node_id: SourceNodeId
    target_node_id: TargetNodeId
    linked_route_entry_id: str
    linked_boundary_entry_id: str
    linked_target_topology_id: str
    transport_mode: TransportMode
    approval_mode: ApprovalMode
    encryption_mode: EncryptionMode
    cross_node_transfer_allowed: bool
    sync_allowed: bool
    update_allowed: bool
    explainable_required: bool
    production_path_allowed: bool
    transport_status: TransportStatus
    description: str

    def __post_init__(self) -> None:
        """Validate secure sync / update transport invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.secure_transport_entry_id):
            raise ValueError(
                f"Invalid secure_transport_entry_id: {self.secure_transport_entry_id}"
            )

        if not _NODE_ID_PATTERN.fullmatch(self.source_node_id):
            raise ValueError(f"Invalid source_node_id: {self.source_node_id}")

        if not _NODE_ID_PATTERN.fullmatch(self.target_node_id):
            raise ValueError(f"Invalid target_node_id: {self.target_node_id}")

        if not _ROUTE_ID_PATTERN.fullmatch(self.linked_route_entry_id):
            raise ValueError(
                f"Invalid linked_route_entry_id: {self.linked_route_entry_id}"
            )

        if not _BOUNDARY_ID_PATTERN.fullmatch(self.linked_boundary_entry_id):
            raise ValueError(
                f"Invalid linked_boundary_entry_id: {self.linked_boundary_entry_id}"
            )

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_target_topology_id):
            raise ValueError(
                f"Invalid linked_target_topology_id: {self.linked_target_topology_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.secure_transport_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.secure_transport_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.secure_transport_entry_id}"
            )

        if self.transport_status != "defined":
            raise ValueError(
                f"transport_status must be defined: {self.secure_transport_entry_id}"
            )

        if self.secure_transport_entry_id == "transport_dev_local_001":
            if self.transport_class != "local_control_transport":
                raise ValueError(
                    "transport_dev_local_001 must use local_control_transport"
                )
            if self.source_node_id != "dev_001" or self.target_node_id != "dev_001":
                raise ValueError("transport_dev_local_001 must be dev_001 -> dev_001")
            if self.linked_route_entry_id != "leaseartifact_control_plane_001":
                raise ValueError(
                    "transport_dev_local_001 must link leaseartifact_control_plane_001"
                )
            if self.linked_boundary_entry_id != "trustboundary_dev_local_001":
                raise ValueError(
                    "transport_dev_local_001 must link trustboundary_dev_local_001"
                )
            if self.linked_target_topology_id != "nodetopology_dev_001":
                raise ValueError(
                    "transport_dev_local_001 must link nodetopology_dev_001"
                )
            if self.transport_mode != "local_same_node_transport":
                raise ValueError(
                    "transport_dev_local_001 must use local_same_node_transport"
                )
            if self.approval_mode != "no_extra_approval":
                raise ValueError(
                    "transport_dev_local_001 must use no_extra_approval"
                )
            if self.encryption_mode != "local_process_boundary":
                raise ValueError(
                    "transport_dev_local_001 must use local_process_boundary"
                )
            if self.cross_node_transfer_allowed:
                raise ValueError(
                    "transport_dev_local_001 must not allow cross-node transfer"
                )
            if not self.sync_allowed:
                raise ValueError("transport_dev_local_001 must allow sync")
            if not self.update_allowed:
                raise ValueError("transport_dev_local_001 must allow update")

        if self.secure_transport_entry_id == "transport_dev_home_001":
            if self.transport_class != "restricted_update_transport":
                raise ValueError(
                    "transport_dev_home_001 must use restricted_update_transport"
                )
            if self.source_node_id != "dev_001" or self.target_node_id != "home_001":
                raise ValueError("transport_dev_home_001 must be dev_001 -> home_001")
            if self.linked_route_entry_id != "leaseartifact_heavy_execution_001":
                raise ValueError(
                    "transport_dev_home_001 must link leaseartifact_heavy_execution_001"
                )
            if self.linked_boundary_entry_id != "trustboundary_dev_home_001":
                raise ValueError(
                    "transport_dev_home_001 must link trustboundary_dev_home_001"
                )
            if self.linked_target_topology_id != "nodetopology_home_001":
                raise ValueError(
                    "transport_dev_home_001 must link nodetopology_home_001"
                )
            if self.transport_mode != "restricted_cross_node_transport":
                raise ValueError(
                    "transport_dev_home_001 must use restricted_cross_node_transport"
                )
            if self.approval_mode != "approval_required":
                raise ValueError(
                    "transport_dev_home_001 must use approval_required"
                )
            if self.encryption_mode != "restricted_encrypted_transport":
                raise ValueError(
                    "transport_dev_home_001 must use restricted_encrypted_transport"
                )
            if not self.cross_node_transfer_allowed:
                raise ValueError(
                    "transport_dev_home_001 must allow restricted cross-node transfer"
                )
            if self.sync_allowed:
                raise ValueError("transport_dev_home_001 must not allow free sync")
            if not self.update_allowed:
                raise ValueError("transport_dev_home_001 must allow restricted update")

        if self.secure_transport_entry_id == "transport_mobile_local_001":
            if self.transport_class != "local_mobile_transport":
                raise ValueError(
                    "transport_mobile_local_001 must use local_mobile_transport"
                )
            if self.source_node_id != "mobile_001" or self.target_node_id != "mobile_001":
                raise ValueError(
                    "transport_mobile_local_001 must be mobile_001 -> mobile_001"
                )
            if self.linked_route_entry_id != "leaseartifact_mobile_entry_001":
                raise ValueError(
                    "transport_mobile_local_001 must link leaseartifact_mobile_entry_001"
                )
            if self.linked_boundary_entry_id != "trustboundary_mobile_local_001":
                raise ValueError(
                    "transport_mobile_local_001 must link trustboundary_mobile_local_001"
                )
            if self.linked_target_topology_id != "nodetopology_mobile_001":
                raise ValueError(
                    "transport_mobile_local_001 must link nodetopology_mobile_001"
                )
            if self.transport_mode != "local_same_node_transport":
                raise ValueError(
                    "transport_mobile_local_001 must use local_same_node_transport"
                )
            if self.approval_mode != "no_extra_approval":
                raise ValueError(
                    "transport_mobile_local_001 must use no_extra_approval"
                )
            if self.encryption_mode != "local_process_boundary":
                raise ValueError(
                    "transport_mobile_local_001 must use local_process_boundary"
                )
            if self.cross_node_transfer_allowed:
                raise ValueError(
                    "transport_mobile_local_001 must not allow cross-node transfer"
                )
            if not self.sync_allowed:
                raise ValueError("transport_mobile_local_001 must allow local sync")
            if not self.update_allowed:
                raise ValueError("transport_mobile_local_001 must allow local update")


@dataclass(frozen=True, slots=True)
class SecureSyncUpdateTransportContract:
    """Unified secure sync / update transport contract."""

    total_entries: int
    local_transport_entries: int
    restricted_cross_node_entries: int
    approval_required_entries: int
    defined_entries: int
    entries: tuple[SecureSyncUpdateTransportEntry, ...]

    def __post_init__(self) -> None:
        """Validate secure sync / update transport contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        local_transport_entries = sum(
            1 for entry in self.entries if entry.transport_mode == "local_same_node_transport"
        )
        restricted_cross_node_entries = sum(
            1 for entry in self.entries if entry.transport_mode == "restricted_cross_node_transport"
        )
        approval_required_entries = sum(
            1 for entry in self.entries if entry.approval_mode == "approval_required"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.transport_status == "defined"
        )

        if self.local_transport_entries != local_transport_entries:
            raise ValueError("local_transport_entries must match computed count")

        if self.restricted_cross_node_entries != restricted_cross_node_entries:
            raise ValueError(
                "restricted_cross_node_entries must match computed count"
            )

        if self.approval_required_entries != approval_required_entries:
            raise ValueError("approval_required_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.secure_transport_entry_id for entry in self.entries)
        route_ids = tuple(entry.linked_route_entry_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate secure_transport_entry_id values detected")

        if len(set(route_ids)) != len(route_ids):
            raise ValueError("Duplicate linked_route_entry_id values detected")


def build_secure_sync_update_transport_contract() -> SecureSyncUpdateTransportContract:
    """Build canonical secure sync / update transport contract."""
    topology_contract = build_node_topology_runtime_contract()
    lease_contract = build_distributed_lease_artifact_routing_contract()
    boundary_contract = build_network_trust_boundaries_contract()

    topology_ids = {entry.topology_entry_id for entry in topology_contract.entries}
    lease_ids = {entry.lease_routing_entry_id for entry in lease_contract.entries}
    boundary_ids = {entry.trust_boundary_entry_id for entry in boundary_contract.entries}

    required_topology_ids = {
        "nodetopology_dev_001",
        "nodetopology_home_001",
        "nodetopology_mobile_001",
    }
    required_lease_ids = {
        "leaseartifact_control_plane_001",
        "leaseartifact_heavy_execution_001",
        "leaseartifact_mobile_entry_001",
    }
    required_boundary_ids = {
        "trustboundary_dev_local_001",
        "trustboundary_dev_home_001",
        "trustboundary_mobile_local_001",
    }

    missing_topology_ids = required_topology_ids - topology_ids
    if missing_topology_ids:
        raise ValueError(
            f"Missing topology ids: {sorted(missing_topology_ids)}"
        )

    missing_lease_ids = required_lease_ids - lease_ids
    if missing_lease_ids:
        raise ValueError(f"Missing lease ids: {sorted(missing_lease_ids)}")

    missing_boundary_ids = required_boundary_ids - boundary_ids
    if missing_boundary_ids:
        raise ValueError(
            f"Missing boundary ids: {sorted(missing_boundary_ids)}"
        )

    entries = (
        SecureSyncUpdateTransportEntry(
            secure_transport_entry_id="transport_dev_local_001",
            transport_class="local_control_transport",
            source_node_id="dev_001",
            target_node_id="dev_001",
            linked_route_entry_id="leaseartifact_control_plane_001",
            linked_boundary_entry_id="trustboundary_dev_local_001",
            linked_target_topology_id="nodetopology_dev_001",
            transport_mode="local_same_node_transport",
            approval_mode="no_extra_approval",
            encryption_mode="local_process_boundary",
            cross_node_transfer_allowed=False,
            sync_allowed=True,
            update_allowed=True,
            explainable_required=True,
            production_path_allowed=True,
            transport_status="defined",
            description="Canonical secure local transport for DEV control-plane artifacts.",
        ),
        SecureSyncUpdateTransportEntry(
            secure_transport_entry_id="transport_dev_home_001",
            transport_class="restricted_update_transport",
            source_node_id="dev_001",
            target_node_id="home_001",
            linked_route_entry_id="leaseartifact_heavy_execution_001",
            linked_boundary_entry_id="trustboundary_dev_home_001",
            linked_target_topology_id="nodetopology_home_001",
            transport_mode="restricted_cross_node_transport",
            approval_mode="approval_required",
            encryption_mode="restricted_encrypted_transport",
            cross_node_transfer_allowed=True,
            sync_allowed=False,
            update_allowed=True,
            explainable_required=True,
            production_path_allowed=True,
            transport_status="defined",
            description="Canonical restricted encrypted transport for DEV→HOME update path.",
        ),
        SecureSyncUpdateTransportEntry(
            secure_transport_entry_id="transport_mobile_local_001",
            transport_class="local_mobile_transport",
            source_node_id="mobile_001",
            target_node_id="mobile_001",
            linked_route_entry_id="leaseartifact_mobile_entry_001",
            linked_boundary_entry_id="trustboundary_mobile_local_001",
            linked_target_topology_id="nodetopology_mobile_001",
            transport_mode="local_same_node_transport",
            approval_mode="no_extra_approval",
            encryption_mode="local_process_boundary",
            cross_node_transfer_allowed=False,
            sync_allowed=True,
            update_allowed=True,
            explainable_required=True,
            production_path_allowed=True,
            transport_status="defined",
            description="Canonical secure local transport for MOBILE request artifacts.",
        ),
    )

    local_transport_entries = sum(
        1 for entry in entries if entry.transport_mode == "local_same_node_transport"
    )
    restricted_cross_node_entries = sum(
        1 for entry in entries if entry.transport_mode == "restricted_cross_node_transport"
    )
    approval_required_entries = sum(
        1 for entry in entries if entry.approval_mode == "approval_required"
    )
    defined_entries = sum(
        1 for entry in entries if entry.transport_status == "defined"
    )

    return SecureSyncUpdateTransportContract(
        total_entries=len(entries),
        local_transport_entries=local_transport_entries,
        restricted_cross_node_entries=restricted_cross_node_entries,
        approval_required_entries=approval_required_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
