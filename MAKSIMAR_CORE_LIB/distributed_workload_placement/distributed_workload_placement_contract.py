from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.multi_node_health_registry import (
    build_multi_node_health_registry_contract,
)
from MAKSIMAR_CORE_LIB.node_topology_runtime import (
    build_node_topology_runtime_contract,
)


PlacementEntryId = Literal[
    "placement_control_plane_001",
    "placement_heavy_execution_001",
    "placement_mobile_entry_001",
]

WorkloadClass = Literal[
    "control_plane_workload",
    "heavy_execution_workload",
    "mobile_entry_workload",
]

TargetNodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

PlacementReason = Literal[
    "control_plane_on_dev",
    "heavy_execution_on_home",
    "mobile_entry_on_mobile",
]

PlacementStatus = Literal[
    "placed",
]


_ENTRY_ID_PATTERN = re.compile(r"^placement_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")
_HEALTH_ID_PATTERN = re.compile(r"^nodehealth_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class DistributedWorkloadPlacementEntry:
    """Canonical distributed workload placement entry."""

    placement_entry_id: PlacementEntryId
    workload_class: WorkloadClass
    target_node_id: TargetNodeId
    linked_topology_entry_id: str
    linked_health_entry_id: str
    heavy_execution_required: bool
    control_plane_required: bool
    mobile_proxy_required: bool
    placement_reason: PlacementReason
    explainable_required: bool
    production_path_allowed: bool
    placement_status: PlacementStatus
    description: str

    def __post_init__(self) -> None:
        """Validate distributed workload placement invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.placement_entry_id):
            raise ValueError(f"Invalid placement_entry_id: {self.placement_entry_id}")

        if not _NODE_ID_PATTERN.fullmatch(self.target_node_id):
            raise ValueError(f"Invalid target_node_id: {self.target_node_id}")

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_topology_entry_id):
            raise ValueError(
                f"Invalid linked_topology_entry_id: {self.linked_topology_entry_id}"
            )

        if not _HEALTH_ID_PATTERN.fullmatch(self.linked_health_entry_id):
            raise ValueError(
                f"Invalid linked_health_entry_id: {self.linked_health_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.placement_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.placement_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.placement_entry_id}"
            )

        if self.placement_status != "placed":
            raise ValueError(
                f"placement_status must be placed: {self.placement_entry_id}"
            )

        if self.placement_entry_id == "placement_control_plane_001":
            if self.workload_class != "control_plane_workload":
                raise ValueError(
                    "placement_control_plane_001 must use control_plane_workload"
                )
            if self.target_node_id != "dev_001":
                raise ValueError(
                    "placement_control_plane_001 must target dev_001"
                )
            if self.linked_topology_entry_id != "nodetopology_dev_001":
                raise ValueError(
                    "placement_control_plane_001 must link nodetopology_dev_001"
                )
            if self.linked_health_entry_id != "nodehealth_dev_001":
                raise ValueError(
                    "placement_control_plane_001 must link nodehealth_dev_001"
                )
            if self.heavy_execution_required:
                raise ValueError(
                    "placement_control_plane_001 must not require heavy_execution"
                )
            if not self.control_plane_required:
                raise ValueError(
                    "placement_control_plane_001 must require control_plane"
                )
            if self.mobile_proxy_required:
                raise ValueError(
                    "placement_control_plane_001 must not require mobile_proxy"
                )
            if self.placement_reason != "control_plane_on_dev":
                raise ValueError(
                    "placement_control_plane_001 must use control_plane_on_dev"
                )

        if self.placement_entry_id == "placement_heavy_execution_001":
            if self.workload_class != "heavy_execution_workload":
                raise ValueError(
                    "placement_heavy_execution_001 must use heavy_execution_workload"
                )
            if self.target_node_id != "home_001":
                raise ValueError(
                    "placement_heavy_execution_001 must target home_001"
                )
            if self.linked_topology_entry_id != "nodetopology_home_001":
                raise ValueError(
                    "placement_heavy_execution_001 must link nodetopology_home_001"
                )
            if self.linked_health_entry_id != "nodehealth_home_001":
                raise ValueError(
                    "placement_heavy_execution_001 must link nodehealth_home_001"
                )
            if not self.heavy_execution_required:
                raise ValueError(
                    "placement_heavy_execution_001 must require heavy_execution"
                )
            if self.control_plane_required:
                raise ValueError(
                    "placement_heavy_execution_001 must not require control_plane"
                )
            if self.mobile_proxy_required:
                raise ValueError(
                    "placement_heavy_execution_001 must not require mobile_proxy"
                )
            if self.placement_reason != "heavy_execution_on_home":
                raise ValueError(
                    "placement_heavy_execution_001 must use heavy_execution_on_home"
                )

        if self.placement_entry_id == "placement_mobile_entry_001":
            if self.workload_class != "mobile_entry_workload":
                raise ValueError(
                    "placement_mobile_entry_001 must use mobile_entry_workload"
                )
            if self.target_node_id != "mobile_001":
                raise ValueError(
                    "placement_mobile_entry_001 must target mobile_001"
                )
            if self.linked_topology_entry_id != "nodetopology_mobile_001":
                raise ValueError(
                    "placement_mobile_entry_001 must link nodetopology_mobile_001"
                )
            if self.linked_health_entry_id != "nodehealth_mobile_001":
                raise ValueError(
                    "placement_mobile_entry_001 must link nodehealth_mobile_001"
                )
            if self.heavy_execution_required:
                raise ValueError(
                    "placement_mobile_entry_001 must not require heavy_execution"
                )
            if self.control_plane_required:
                raise ValueError(
                    "placement_mobile_entry_001 must not require control_plane"
                )
            if not self.mobile_proxy_required:
                raise ValueError(
                    "placement_mobile_entry_001 must require mobile_proxy"
                )
            if self.placement_reason != "mobile_entry_on_mobile":
                raise ValueError(
                    "placement_mobile_entry_001 must use mobile_entry_on_mobile"
                )


@dataclass(frozen=True, slots=True)
class DistributedWorkloadPlacementContract:
    """Unified distributed workload placement contract."""

    total_entries: int
    heavy_execution_entries: int
    control_plane_entries: int
    mobile_proxy_entries: int
    placed_entries: int
    entries: tuple[DistributedWorkloadPlacementEntry, ...]

    def __post_init__(self) -> None:
        """Validate distributed workload placement contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        heavy_execution_entries = sum(
            1 for entry in self.entries if entry.heavy_execution_required
        )
        control_plane_entries = sum(
            1 for entry in self.entries if entry.control_plane_required
        )
        mobile_proxy_entries = sum(
            1 for entry in self.entries if entry.mobile_proxy_required
        )
        placed_entries = sum(
            1 for entry in self.entries if entry.placement_status == "placed"
        )

        if self.heavy_execution_entries != heavy_execution_entries:
            raise ValueError("heavy_execution_entries must match computed count")

        if self.control_plane_entries != control_plane_entries:
            raise ValueError("control_plane_entries must match computed count")

        if self.mobile_proxy_entries != mobile_proxy_entries:
            raise ValueError("mobile_proxy_entries must match computed count")

        if self.placed_entries != placed_entries:
            raise ValueError("placed_entries must match computed count")

        entry_ids = tuple(entry.placement_entry_id for entry in self.entries)
        workloads = tuple(entry.workload_class for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate placement_entry_id values detected")

        if len(set(workloads)) != len(workloads):
            raise ValueError("Duplicate workload_class values detected")


def build_distributed_workload_placement_contract() -> DistributedWorkloadPlacementContract:
    """Build canonical distributed workload placement contract."""
    topology_contract = build_node_topology_runtime_contract()
    health_contract = build_multi_node_health_registry_contract()

    topology_ids = {entry.topology_entry_id for entry in topology_contract.entries}
    health_ids = {entry.health_registry_entry_id for entry in health_contract.entries}

    required_topology_ids = {
        "nodetopology_dev_001",
        "nodetopology_home_001",
        "nodetopology_mobile_001",
    }
    required_health_ids = {
        "nodehealth_dev_001",
        "nodehealth_home_001",
        "nodehealth_mobile_001",
    }

    missing_topology_ids = required_topology_ids - topology_ids
    if missing_topology_ids:
        raise ValueError(
            f"Missing topology ids: {sorted(missing_topology_ids)}"
        )

    missing_health_ids = required_health_ids - health_ids
    if missing_health_ids:
        raise ValueError(
            f"Missing health ids: {sorted(missing_health_ids)}"
        )

    entries = (
        DistributedWorkloadPlacementEntry(
            placement_entry_id="placement_control_plane_001",
            workload_class="control_plane_workload",
            target_node_id="dev_001",
            linked_topology_entry_id="nodetopology_dev_001",
            linked_health_entry_id="nodehealth_dev_001",
            heavy_execution_required=False,
            control_plane_required=True,
            mobile_proxy_required=False,
            placement_reason="control_plane_on_dev",
            explainable_required=True,
            production_path_allowed=True,
            placement_status="placed",
            description="Canonical workload placement for control plane workload.",
        ),
        DistributedWorkloadPlacementEntry(
            placement_entry_id="placement_heavy_execution_001",
            workload_class="heavy_execution_workload",
            target_node_id="home_001",
            linked_topology_entry_id="nodetopology_home_001",
            linked_health_entry_id="nodehealth_home_001",
            heavy_execution_required=True,
            control_plane_required=False,
            mobile_proxy_required=False,
            placement_reason="heavy_execution_on_home",
            explainable_required=True,
            production_path_allowed=True,
            placement_status="placed",
            description="Canonical workload placement for heavy execution workload.",
        ),
        DistributedWorkloadPlacementEntry(
            placement_entry_id="placement_mobile_entry_001",
            workload_class="mobile_entry_workload",
            target_node_id="mobile_001",
            linked_topology_entry_id="nodetopology_mobile_001",
            linked_health_entry_id="nodehealth_mobile_001",
            heavy_execution_required=False,
            control_plane_required=False,
            mobile_proxy_required=True,
            placement_reason="mobile_entry_on_mobile",
            explainable_required=True,
            production_path_allowed=True,
            placement_status="placed",
            description="Canonical workload placement for mobile entry workload.",
        ),
    )

    heavy_execution_entries = sum(
        1 for entry in entries if entry.heavy_execution_required
    )
    control_plane_entries = sum(
        1 for entry in entries if entry.control_plane_required
    )
    mobile_proxy_entries = sum(
        1 for entry in entries if entry.mobile_proxy_required
    )
    placed_entries = sum(
        1 for entry in entries if entry.placement_status == "placed"
    )

    return DistributedWorkloadPlacementContract(
        total_entries=len(entries),
        heavy_execution_entries=heavy_execution_entries,
        control_plane_entries=control_plane_entries,
        mobile_proxy_entries=mobile_proxy_entries,
        placed_entries=placed_entries,
        entries=entries,
    )
