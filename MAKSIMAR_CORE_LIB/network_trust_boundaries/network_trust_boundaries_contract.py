from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.distributed_lease_artifact_routing import (
    build_distributed_lease_artifact_routing_contract,
)
from MAKSIMAR_CORE_LIB.distributed_workload_placement import (
    build_distributed_workload_placement_contract,
)
from MAKSIMAR_CORE_LIB.node_topology_runtime import (
    build_node_topology_runtime_contract,
)


TrustBoundaryEntryId = Literal[
    "trustboundary_dev_local_001",
    "trustboundary_dev_home_001",
    "trustboundary_mobile_local_001",
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

TrustZoneClass = Literal[
    "local_same_zone",
    "cross_zone_restricted",
]

BoundaryRiskClass = Literal[
    "low",
    "elevated",
]

BoundaryRequirement = Literal[
    "local_only",
    "approval_and_restricted_route",
]

BoundaryModelStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^trustboundary_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")
_ROUTE_ID_PATTERN = re.compile(r"^leaseartifact_[a-z][a-z0-9_]*$")
_PLACEMENT_ID_PATTERN = re.compile(r"^placement_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class NetworkTrustBoundaryEntry:
    """Canonical network / trust boundary entry."""

    trust_boundary_entry_id: TrustBoundaryEntryId
    source_node_id: SourceNodeId
    target_node_id: TargetNodeId
    linked_source_topology_id: str
    linked_target_topology_id: str
    linked_route_entry_id: str
    linked_placement_entry_id: str
    trust_zone_class: TrustZoneClass
    boundary_risk_class: BoundaryRiskClass
    boundary_requirement: BoundaryRequirement
    cross_node_allowed: bool
    explainable_required: bool
    production_path_allowed: bool
    boundary_model_status: BoundaryModelStatus
    description: str

    def __post_init__(self) -> None:
        """Validate network / trust boundary invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.trust_boundary_entry_id):
            raise ValueError(
                f"Invalid trust_boundary_entry_id: {self.trust_boundary_entry_id}"
            )

        if not _NODE_ID_PATTERN.fullmatch(self.source_node_id):
            raise ValueError(f"Invalid source_node_id: {self.source_node_id}")

        if not _NODE_ID_PATTERN.fullmatch(self.target_node_id):
            raise ValueError(f"Invalid target_node_id: {self.target_node_id}")

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_source_topology_id):
            raise ValueError(
                f"Invalid linked_source_topology_id: {self.linked_source_topology_id}"
            )

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_target_topology_id):
            raise ValueError(
                f"Invalid linked_target_topology_id: {self.linked_target_topology_id}"
            )

        if not _ROUTE_ID_PATTERN.fullmatch(self.linked_route_entry_id):
            raise ValueError(
                f"Invalid linked_route_entry_id: {self.linked_route_entry_id}"
            )

        if not _PLACEMENT_ID_PATTERN.fullmatch(self.linked_placement_entry_id):
            raise ValueError(
                f"Invalid linked_placement_entry_id: {self.linked_placement_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.trust_boundary_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.trust_boundary_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.trust_boundary_entry_id}"
            )

        if self.boundary_model_status != "defined":
            raise ValueError(
                f"boundary_model_status must be defined: {self.trust_boundary_entry_id}"
            )

        if self.trust_boundary_entry_id == "trustboundary_dev_local_001":
            if self.source_node_id != "dev_001" or self.target_node_id != "dev_001":
                raise ValueError("trustboundary_dev_local_001 must be dev_001 -> dev_001")
            if self.linked_source_topology_id != "nodetopology_dev_001":
                raise ValueError(
                    "trustboundary_dev_local_001 must link nodetopology_dev_001 as source"
                )
            if self.linked_target_topology_id != "nodetopology_dev_001":
                raise ValueError(
                    "trustboundary_dev_local_001 must link nodetopology_dev_001 as target"
                )
            if self.linked_route_entry_id != "leaseartifact_control_plane_001":
                raise ValueError(
                    "trustboundary_dev_local_001 must link leaseartifact_control_plane_001"
                )
            if self.linked_placement_entry_id != "placement_control_plane_001":
                raise ValueError(
                    "trustboundary_dev_local_001 must link placement_control_plane_001"
                )
            if self.trust_zone_class != "local_same_zone":
                raise ValueError(
                    "trustboundary_dev_local_001 must use local_same_zone"
                )
            if self.boundary_risk_class != "low":
                raise ValueError("trustboundary_dev_local_001 must use low risk")
            if self.boundary_requirement != "local_only":
                raise ValueError(
                    "trustboundary_dev_local_001 must use local_only"
                )
            if not self.cross_node_allowed:
                raise ValueError(
                    "trustboundary_dev_local_001 must keep canonical local route allowed"
                )

        if self.trust_boundary_entry_id == "trustboundary_dev_home_001":
            if self.source_node_id != "dev_001" or self.target_node_id != "home_001":
                raise ValueError("trustboundary_dev_home_001 must be dev_001 -> home_001")
            if self.linked_source_topology_id != "nodetopology_dev_001":
                raise ValueError(
                    "trustboundary_dev_home_001 must link nodetopology_dev_001 as source"
                )
            if self.linked_target_topology_id != "nodetopology_home_001":
                raise ValueError(
                    "trustboundary_dev_home_001 must link nodetopology_home_001 as target"
                )
            if self.linked_route_entry_id != "leaseartifact_heavy_execution_001":
                raise ValueError(
                    "trustboundary_dev_home_001 must link leaseartifact_heavy_execution_001"
                )
            if self.linked_placement_entry_id != "placement_heavy_execution_001":
                raise ValueError(
                    "trustboundary_dev_home_001 must link placement_heavy_execution_001"
                )
            if self.trust_zone_class != "cross_zone_restricted":
                raise ValueError(
                    "trustboundary_dev_home_001 must use cross_zone_restricted"
                )
            if self.boundary_risk_class != "elevated":
                raise ValueError("trustboundary_dev_home_001 must use elevated risk")
            if self.boundary_requirement != "approval_and_restricted_route":
                raise ValueError(
                    "trustboundary_dev_home_001 must use approval_and_restricted_route"
                )
            if not self.cross_node_allowed:
                raise ValueError(
                    "trustboundary_dev_home_001 must allow cross-node route under restriction"
                )

        if self.trust_boundary_entry_id == "trustboundary_mobile_local_001":
            if self.source_node_id != "mobile_001" or self.target_node_id != "mobile_001":
                raise ValueError(
                    "trustboundary_mobile_local_001 must be mobile_001 -> mobile_001"
                )
            if self.linked_source_topology_id != "nodetopology_mobile_001":
                raise ValueError(
                    "trustboundary_mobile_local_001 must link nodetopology_mobile_001 as source"
                )
            if self.linked_target_topology_id != "nodetopology_mobile_001":
                raise ValueError(
                    "trustboundary_mobile_local_001 must link nodetopology_mobile_001 as target"
                )
            if self.linked_route_entry_id != "leaseartifact_mobile_entry_001":
                raise ValueError(
                    "trustboundary_mobile_local_001 must link leaseartifact_mobile_entry_001"
                )
            if self.linked_placement_entry_id != "placement_mobile_entry_001":
                raise ValueError(
                    "trustboundary_mobile_local_001 must link placement_mobile_entry_001"
                )
            if self.trust_zone_class != "local_same_zone":
                raise ValueError(
                    "trustboundary_mobile_local_001 must use local_same_zone"
                )
            if self.boundary_risk_class != "low":
                raise ValueError("trustboundary_mobile_local_001 must use low risk")
            if self.boundary_requirement != "local_only":
                raise ValueError(
                    "trustboundary_mobile_local_001 must use local_only"
                )
            if not self.cross_node_allowed:
                raise ValueError(
                    "trustboundary_mobile_local_001 must keep canonical local route allowed"
                )


@dataclass(frozen=True, slots=True)
class NetworkTrustBoundariesContract:
    """Unified network / trust boundaries contract."""

    total_entries: int
    local_zone_entries: int
    restricted_cross_zone_entries: int
    elevated_risk_entries: int
    defined_entries: int
    entries: tuple[NetworkTrustBoundaryEntry, ...]

    def __post_init__(self) -> None:
        """Validate network / trust boundaries contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        local_zone_entries = sum(
            1 for entry in self.entries if entry.trust_zone_class == "local_same_zone"
        )
        restricted_cross_zone_entries = sum(
            1
            for entry in self.entries
            if entry.trust_zone_class == "cross_zone_restricted"
        )
        elevated_risk_entries = sum(
            1 for entry in self.entries if entry.boundary_risk_class == "elevated"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.boundary_model_status == "defined"
        )

        if self.local_zone_entries != local_zone_entries:
            raise ValueError("local_zone_entries must match computed count")

        if self.restricted_cross_zone_entries != restricted_cross_zone_entries:
            raise ValueError(
                "restricted_cross_zone_entries must match computed count"
            )

        if self.elevated_risk_entries != elevated_risk_entries:
            raise ValueError("elevated_risk_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.trust_boundary_entry_id for entry in self.entries)
        route_ids = tuple(entry.linked_route_entry_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate trust_boundary_entry_id values detected")

        if len(set(route_ids)) != len(route_ids):
            raise ValueError("Duplicate linked_route_entry_id values detected")


def build_network_trust_boundaries_contract() -> NetworkTrustBoundariesContract:
    """Build canonical network / trust boundaries contract."""
    topology_contract = build_node_topology_runtime_contract()
    placement_contract = build_distributed_workload_placement_contract()
    lease_contract = build_distributed_lease_artifact_routing_contract()

    topology_ids = {entry.topology_entry_id for entry in topology_contract.entries}
    placement_ids = {entry.placement_entry_id for entry in placement_contract.entries}
    lease_ids = {entry.lease_routing_entry_id for entry in lease_contract.entries}

    required_topology_ids = {
        "nodetopology_dev_001",
        "nodetopology_home_001",
        "nodetopology_mobile_001",
    }
    required_placement_ids = {
        "placement_control_plane_001",
        "placement_heavy_execution_001",
        "placement_mobile_entry_001",
    }
    required_lease_ids = {
        "leaseartifact_control_plane_001",
        "leaseartifact_heavy_execution_001",
        "leaseartifact_mobile_entry_001",
    }

    missing_topology_ids = required_topology_ids - topology_ids
    if missing_topology_ids:
        raise ValueError(
            f"Missing topology ids: {sorted(missing_topology_ids)}"
        )

    missing_placement_ids = required_placement_ids - placement_ids
    if missing_placement_ids:
        raise ValueError(
            f"Missing placement ids: {sorted(missing_placement_ids)}"
        )

    missing_lease_ids = required_lease_ids - lease_ids
    if missing_lease_ids:
        raise ValueError(f"Missing lease ids: {sorted(missing_lease_ids)}")

    entries = (
        NetworkTrustBoundaryEntry(
            trust_boundary_entry_id="trustboundary_dev_local_001",
            source_node_id="dev_001",
            target_node_id="dev_001",
            linked_source_topology_id="nodetopology_dev_001",
            linked_target_topology_id="nodetopology_dev_001",
            linked_route_entry_id="leaseartifact_control_plane_001",
            linked_placement_entry_id="placement_control_plane_001",
            trust_zone_class="local_same_zone",
            boundary_risk_class="low",
            boundary_requirement="local_only",
            cross_node_allowed=True,
            explainable_required=True,
            production_path_allowed=True,
            boundary_model_status="defined",
            description="Canonical trust boundary for DEV local control-plane route.",
        ),
        NetworkTrustBoundaryEntry(
            trust_boundary_entry_id="trustboundary_dev_home_001",
            source_node_id="dev_001",
            target_node_id="home_001",
            linked_source_topology_id="nodetopology_dev_001",
            linked_target_topology_id="nodetopology_home_001",
            linked_route_entry_id="leaseartifact_heavy_execution_001",
            linked_placement_entry_id="placement_heavy_execution_001",
            trust_zone_class="cross_zone_restricted",
            boundary_risk_class="elevated",
            boundary_requirement="approval_and_restricted_route",
            cross_node_allowed=True,
            explainable_required=True,
            production_path_allowed=True,
            boundary_model_status="defined",
            description="Canonical restricted trust boundary for DEV to HOME heavy route.",
        ),
        NetworkTrustBoundaryEntry(
            trust_boundary_entry_id="trustboundary_mobile_local_001",
            source_node_id="mobile_001",
            target_node_id="mobile_001",
            linked_source_topology_id="nodetopology_mobile_001",
            linked_target_topology_id="nodetopology_mobile_001",
            linked_route_entry_id="leaseartifact_mobile_entry_001",
            linked_placement_entry_id="placement_mobile_entry_001",
            trust_zone_class="local_same_zone",
            boundary_risk_class="low",
            boundary_requirement="local_only",
            cross_node_allowed=True,
            explainable_required=True,
            production_path_allowed=True,
            boundary_model_status="defined",
            description="Canonical trust boundary for MOBILE local request route.",
        ),
    )

    local_zone_entries = sum(
        1 for entry in entries if entry.trust_zone_class == "local_same_zone"
    )
    restricted_cross_zone_entries = sum(
        1 for entry in entries if entry.trust_zone_class == "cross_zone_restricted"
    )
    elevated_risk_entries = sum(
        1 for entry in entries if entry.boundary_risk_class == "elevated"
    )
    defined_entries = sum(
        1 for entry in entries if entry.boundary_model_status == "defined"
    )

    return NetworkTrustBoundariesContract(
        total_entries=len(entries),
        local_zone_entries=local_zone_entries,
        restricted_cross_zone_entries=restricted_cross_zone_entries,
        elevated_risk_entries=elevated_risk_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
