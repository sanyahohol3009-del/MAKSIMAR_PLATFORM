from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.distributed_workload_placement import (
    build_distributed_workload_placement_contract,
)
from MAKSIMAR_CORE_LIB.node_topology_runtime import (
    build_node_topology_runtime_contract,
)


LeaseRoutingEntryId = Literal[
    "leaseartifact_control_plane_001",
    "leaseartifact_heavy_execution_001",
    "leaseartifact_mobile_entry_001",
]

ArtifactClass = Literal[
    "control_contract_artifact",
    "heavy_execution_artifact",
    "mobile_request_artifact",
]

LeaseOwnerNodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

TargetNodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

RoutingMode = Literal[
    "local_authoritative_route",
    "cross_node_authoritative_route",
]

LeaseStatus = Literal[
    "leased",
]

ArtifactRoutingStatus = Literal[
    "routed",
]


_ENTRY_ID_PATTERN = re.compile(r"^leaseartifact_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_PLACEMENT_ID_PATTERN = re.compile(r"^placement_[a-z][a-z0-9_]*$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class DistributedLeaseArtifactRoutingEntry:
    """Canonical distributed lease / artifact routing entry."""

    lease_routing_entry_id: LeaseRoutingEntryId
    artifact_class: ArtifactClass
    lease_owner_node_id: LeaseOwnerNodeId
    target_node_id: TargetNodeId
    linked_placement_entry_id: str
    linked_topology_entry_id: str
    routing_mode: RoutingMode
    cross_node_transfer_required: bool
    approval_required_before_route: bool
    lease_status: LeaseStatus
    artifact_routing_status: ArtifactRoutingStatus
    explainable_required: bool
    production_path_allowed: bool
    description: str

    def __post_init__(self) -> None:
        """Validate distributed lease / artifact routing invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.lease_routing_entry_id):
            raise ValueError(
                f"Invalid lease_routing_entry_id: {self.lease_routing_entry_id}"
            )

        if not _NODE_ID_PATTERN.fullmatch(self.lease_owner_node_id):
            raise ValueError(f"Invalid lease_owner_node_id: {self.lease_owner_node_id}")

        if not _NODE_ID_PATTERN.fullmatch(self.target_node_id):
            raise ValueError(f"Invalid target_node_id: {self.target_node_id}")

        if not _PLACEMENT_ID_PATTERN.fullmatch(self.linked_placement_entry_id):
            raise ValueError(
                f"Invalid linked_placement_entry_id: {self.linked_placement_entry_id}"
            )

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_topology_entry_id):
            raise ValueError(
                f"Invalid linked_topology_entry_id: {self.linked_topology_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.lease_routing_entry_id}"
            )

        if self.lease_status != "leased":
            raise ValueError(
                f"lease_status must be leased: {self.lease_routing_entry_id}"
            )

        if self.artifact_routing_status != "routed":
            raise ValueError(
                f"artifact_routing_status must be routed: {self.lease_routing_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.lease_routing_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.lease_routing_entry_id}"
            )

        if self.lease_routing_entry_id == "leaseartifact_control_plane_001":
            if self.artifact_class != "control_contract_artifact":
                raise ValueError(
                    "leaseartifact_control_plane_001 must use control_contract_artifact"
                )
            if self.lease_owner_node_id != "dev_001":
                raise ValueError(
                    "leaseartifact_control_plane_001 must use dev_001 as lease owner"
                )
            if self.target_node_id != "dev_001":
                raise ValueError(
                    "leaseartifact_control_plane_001 must target dev_001"
                )
            if self.linked_placement_entry_id != "placement_control_plane_001":
                raise ValueError(
                    "leaseartifact_control_plane_001 must link placement_control_plane_001"
                )
            if self.linked_topology_entry_id != "nodetopology_dev_001":
                raise ValueError(
                    "leaseartifact_control_plane_001 must link nodetopology_dev_001"
                )
            if self.routing_mode != "local_authoritative_route":
                raise ValueError(
                    "leaseartifact_control_plane_001 must use local_authoritative_route"
                )
            if self.cross_node_transfer_required:
                raise ValueError(
                    "leaseartifact_control_plane_001 must not require cross-node transfer"
                )
            if self.approval_required_before_route:
                raise ValueError(
                    "leaseartifact_control_plane_001 must not require approval before route"
                )

        if self.lease_routing_entry_id == "leaseartifact_heavy_execution_001":
            if self.artifact_class != "heavy_execution_artifact":
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must use heavy_execution_artifact"
                )
            if self.lease_owner_node_id != "dev_001":
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must use dev_001 as lease owner"
                )
            if self.target_node_id != "home_001":
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must target home_001"
                )
            if self.linked_placement_entry_id != "placement_heavy_execution_001":
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must link placement_heavy_execution_001"
                )
            if self.linked_topology_entry_id != "nodetopology_home_001":
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must link nodetopology_home_001"
                )
            if self.routing_mode != "cross_node_authoritative_route":
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must use cross_node_authoritative_route"
                )
            if not self.cross_node_transfer_required:
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must require cross-node transfer"
                )
            if not self.approval_required_before_route:
                raise ValueError(
                    "leaseartifact_heavy_execution_001 must require approval before route"
                )

        if self.lease_routing_entry_id == "leaseartifact_mobile_entry_001":
            if self.artifact_class != "mobile_request_artifact":
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must use mobile_request_artifact"
                )
            if self.lease_owner_node_id != "mobile_001":
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must use mobile_001 as lease owner"
                )
            if self.target_node_id != "mobile_001":
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must target mobile_001"
                )
            if self.linked_placement_entry_id != "placement_mobile_entry_001":
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must link placement_mobile_entry_001"
                )
            if self.linked_topology_entry_id != "nodetopology_mobile_001":
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must link nodetopology_mobile_001"
                )
            if self.routing_mode != "local_authoritative_route":
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must use local_authoritative_route"
                )
            if self.cross_node_transfer_required:
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must not require cross-node transfer"
                )
            if self.approval_required_before_route:
                raise ValueError(
                    "leaseartifact_mobile_entry_001 must not require approval before route"
                )


@dataclass(frozen=True, slots=True)
class DistributedLeaseArtifactRoutingContract:
    """Unified distributed lease / artifact routing contract."""

    total_entries: int
    local_route_entries: int
    cross_node_route_entries: int
    approval_required_entries: int
    routed_entries: int
    entries: tuple[DistributedLeaseArtifactRoutingEntry, ...]

    def __post_init__(self) -> None:
        """Validate distributed lease / artifact routing contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        local_route_entries = sum(
            1 for entry in self.entries if entry.routing_mode == "local_authoritative_route"
        )
        cross_node_route_entries = sum(
            1 for entry in self.entries if entry.routing_mode == "cross_node_authoritative_route"
        )
        approval_required_entries = sum(
            1 for entry in self.entries if entry.approval_required_before_route
        )
        routed_entries = sum(
            1 for entry in self.entries if entry.artifact_routing_status == "routed"
        )

        if self.local_route_entries != local_route_entries:
            raise ValueError("local_route_entries must match computed count")

        if self.cross_node_route_entries != cross_node_route_entries:
            raise ValueError("cross_node_route_entries must match computed count")

        if self.approval_required_entries != approval_required_entries:
            raise ValueError("approval_required_entries must match computed count")

        if self.routed_entries != routed_entries:
            raise ValueError("routed_entries must match computed count")

        entry_ids = tuple(entry.lease_routing_entry_id for entry in self.entries)
        artifact_classes = tuple(entry.artifact_class for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate lease_routing_entry_id values detected")

        if len(set(artifact_classes)) != len(artifact_classes):
            raise ValueError("Duplicate artifact_class values detected")


def build_distributed_lease_artifact_routing_contract() -> DistributedLeaseArtifactRoutingContract:
    """Build canonical distributed lease / artifact routing contract."""
    placement_contract = build_distributed_workload_placement_contract()
    topology_contract = build_node_topology_runtime_contract()

    placement_ids = {entry.placement_entry_id for entry in placement_contract.entries}
    topology_ids = {entry.topology_entry_id for entry in topology_contract.entries}

    required_placement_ids = {
        "placement_control_plane_001",
        "placement_heavy_execution_001",
        "placement_mobile_entry_001",
    }
    required_topology_ids = {
        "nodetopology_dev_001",
        "nodetopology_home_001",
        "nodetopology_mobile_001",
    }

    missing_placement_ids = required_placement_ids - placement_ids
    if missing_placement_ids:
        raise ValueError(
            f"Missing placement ids: {sorted(missing_placement_ids)}"
        )

    missing_topology_ids = required_topology_ids - topology_ids
    if missing_topology_ids:
        raise ValueError(
            f"Missing topology ids: {sorted(missing_topology_ids)}"
        )

    entries = (
        DistributedLeaseArtifactRoutingEntry(
            lease_routing_entry_id="leaseartifact_control_plane_001",
            artifact_class="control_contract_artifact",
            lease_owner_node_id="dev_001",
            target_node_id="dev_001",
            linked_placement_entry_id="placement_control_plane_001",
            linked_topology_entry_id="nodetopology_dev_001",
            routing_mode="local_authoritative_route",
            cross_node_transfer_required=False,
            approval_required_before_route=False,
            lease_status="leased",
            artifact_routing_status="routed",
            explainable_required=True,
            production_path_allowed=True,
            description="Canonical lease-aware routing for control contract artifact.",
        ),
        DistributedLeaseArtifactRoutingEntry(
            lease_routing_entry_id="leaseartifact_heavy_execution_001",
            artifact_class="heavy_execution_artifact",
            lease_owner_node_id="dev_001",
            target_node_id="home_001",
            linked_placement_entry_id="placement_heavy_execution_001",
            linked_topology_entry_id="nodetopology_home_001",
            routing_mode="cross_node_authoritative_route",
            cross_node_transfer_required=True,
            approval_required_before_route=True,
            lease_status="leased",
            artifact_routing_status="routed",
            explainable_required=True,
            production_path_allowed=True,
            description="Canonical lease-aware routing for heavy execution artifact.",
        ),
        DistributedLeaseArtifactRoutingEntry(
            lease_routing_entry_id="leaseartifact_mobile_entry_001",
            artifact_class="mobile_request_artifact",
            lease_owner_node_id="mobile_001",
            target_node_id="mobile_001",
            linked_placement_entry_id="placement_mobile_entry_001",
            linked_topology_entry_id="nodetopology_mobile_001",
            routing_mode="local_authoritative_route",
            cross_node_transfer_required=False,
            approval_required_before_route=False,
            lease_status="leased",
            artifact_routing_status="routed",
            explainable_required=True,
            production_path_allowed=True,
            description="Canonical lease-aware routing for mobile request artifact.",
        ),
    )

    local_route_entries = sum(
        1 for entry in entries if entry.routing_mode == "local_authoritative_route"
    )
    cross_node_route_entries = sum(
        1 for entry in entries if entry.routing_mode == "cross_node_authoritative_route"
    )
    approval_required_entries = sum(
        1 for entry in entries if entry.approval_required_before_route
    )
    routed_entries = sum(
        1 for entry in entries if entry.artifact_routing_status == "routed"
    )

    return DistributedLeaseArtifactRoutingContract(
        total_entries=len(entries),
        local_route_entries=local_route_entries,
        cross_node_route_entries=cross_node_route_entries,
        approval_required_entries=approval_required_entries,
        routed_entries=routed_entries,
        entries=entries,
    )
