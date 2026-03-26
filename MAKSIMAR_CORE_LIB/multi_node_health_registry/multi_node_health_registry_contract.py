from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_runtime_split import (
    build_node_runtime_split_contract,
)
from MAKSIMAR_CORE_LIB.node_topology_runtime import (
    build_node_topology_runtime_contract,
)


HealthRegistryEntryId = Literal[
    "nodehealth_dev_001",
    "nodehealth_home_001",
    "nodehealth_mobile_001",
]

NodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

HealthClass = Literal[
    "healthy_control",
    "healthy_compute",
    "healthy_mobile_proxy",
]

RuntimeState = Literal[
    "normal",
    "throttled",
]

RoutingRelevance = Literal[
    "control_plane_routing",
    "heavy_execution_routing",
    "mobile_entry_routing",
]

HealthRegistryStatus = Literal[
    "registered",
]


_ENTRY_ID_PATTERN = re.compile(r"^nodehealth_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class MultiNodeHealthRegistryEntry:
    """Canonical multi-node health registry entry."""

    health_registry_entry_id: HealthRegistryEntryId
    node_id: NodeId
    linked_topology_entry_id: str
    health_class: HealthClass
    runtime_state: RuntimeState
    health_score: int
    worker_capacity_available: bool
    routing_relevance: RoutingRelevance
    degraded_flag_active: bool
    explainable_required: bool
    production_path_allowed: bool
    registry_status: HealthRegistryStatus
    description: str

    def __post_init__(self) -> None:
        """Validate multi-node health registry invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.health_registry_entry_id):
            raise ValueError(
                f"Invalid health_registry_entry_id: {self.health_registry_entry_id}"
            )

        if not _NODE_ID_PATTERN.fullmatch(self.node_id):
            raise ValueError(f"Invalid node_id: {self.node_id}")

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_topology_entry_id):
            raise ValueError(
                f"Invalid linked_topology_entry_id: {self.linked_topology_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.health_registry_entry_id}"
            )

        if not 0 <= self.health_score <= 100:
            raise ValueError(
                f"health_score must be within 0..100: {self.health_registry_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.health_registry_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.health_registry_entry_id}"
            )

        if self.registry_status != "registered":
            raise ValueError(
                f"registry_status must be registered: {self.health_registry_entry_id}"
            )

        if self.health_registry_entry_id == "nodehealth_dev_001":
            if self.node_id != "dev_001":
                raise ValueError("nodehealth_dev_001 must use dev_001")
            if self.linked_topology_entry_id != "nodetopology_dev_001":
                raise ValueError(
                    "nodehealth_dev_001 must link nodetopology_dev_001"
                )
            if self.health_class != "healthy_control":
                raise ValueError(
                    "nodehealth_dev_001 must use healthy_control"
                )
            if self.runtime_state != "normal":
                raise ValueError("nodehealth_dev_001 must use runtime_state=normal")
            if self.health_score != 96:
                raise ValueError("nodehealth_dev_001 must use health_score=96")
            if not self.worker_capacity_available:
                raise ValueError(
                    "nodehealth_dev_001 must have worker_capacity_available=True"
                )
            if self.routing_relevance != "control_plane_routing":
                raise ValueError(
                    "nodehealth_dev_001 must use control_plane_routing"
                )
            if self.degraded_flag_active:
                raise ValueError(
                    "nodehealth_dev_001 must not have degraded_flag_active"
                )

        if self.health_registry_entry_id == "nodehealth_home_001":
            if self.node_id != "home_001":
                raise ValueError("nodehealth_home_001 must use home_001")
            if self.linked_topology_entry_id != "nodetopology_home_001":
                raise ValueError(
                    "nodehealth_home_001 must link nodetopology_home_001"
                )
            if self.health_class != "healthy_compute":
                raise ValueError(
                    "nodehealth_home_001 must use healthy_compute"
                )
            if self.runtime_state != "throttled":
                raise ValueError("nodehealth_home_001 must use runtime_state=throttled")
            if self.health_score != 82:
                raise ValueError("nodehealth_home_001 must use health_score=82")
            if not self.worker_capacity_available:
                raise ValueError(
                    "nodehealth_home_001 must have worker_capacity_available=True"
                )
            if self.routing_relevance != "heavy_execution_routing":
                raise ValueError(
                    "nodehealth_home_001 must use heavy_execution_routing"
                )
            if not self.degraded_flag_active:
                raise ValueError(
                    "nodehealth_home_001 must have degraded_flag_active=True"
                )

        if self.health_registry_entry_id == "nodehealth_mobile_001":
            if self.node_id != "mobile_001":
                raise ValueError("nodehealth_mobile_001 must use mobile_001")
            if self.linked_topology_entry_id != "nodetopology_mobile_001":
                raise ValueError(
                    "nodehealth_mobile_001 must link nodetopology_mobile_001"
                )
            if self.health_class != "healthy_mobile_proxy":
                raise ValueError(
                    "nodehealth_mobile_001 must use healthy_mobile_proxy"
                )
            if self.runtime_state != "normal":
                raise ValueError("nodehealth_mobile_001 must use runtime_state=normal")
            if self.health_score != 91:
                raise ValueError("nodehealth_mobile_001 must use health_score=91")
            if not self.worker_capacity_available:
                raise ValueError(
                    "nodehealth_mobile_001 must have worker_capacity_available=True"
                )
            if self.routing_relevance != "mobile_entry_routing":
                raise ValueError(
                    "nodehealth_mobile_001 must use mobile_entry_routing"
                )
            if self.degraded_flag_active:
                raise ValueError(
                    "nodehealth_mobile_001 must not have degraded_flag_active"
                )


@dataclass(frozen=True, slots=True)
class MultiNodeHealthRegistryContract:
    """Unified multi-node health registry contract."""

    total_entries: int
    normal_runtime_entries: int
    throttled_runtime_entries: int
    degraded_active_entries: int
    registered_entries: int
    entries: tuple[MultiNodeHealthRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate multi-node health registry contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        normal_runtime_entries = sum(
            1 for entry in self.entries if entry.runtime_state == "normal"
        )
        throttled_runtime_entries = sum(
            1 for entry in self.entries if entry.runtime_state == "throttled"
        )
        degraded_active_entries = sum(
            1 for entry in self.entries if entry.degraded_flag_active
        )
        registered_entries = sum(
            1 for entry in self.entries if entry.registry_status == "registered"
        )

        if self.normal_runtime_entries != normal_runtime_entries:
            raise ValueError("normal_runtime_entries must match computed count")

        if self.throttled_runtime_entries != throttled_runtime_entries:
            raise ValueError("throttled_runtime_entries must match computed count")

        if self.degraded_active_entries != degraded_active_entries:
            raise ValueError("degraded_active_entries must match computed count")

        if self.registered_entries != registered_entries:
            raise ValueError("registered_entries must match computed count")

        entry_ids = tuple(entry.health_registry_entry_id for entry in self.entries)
        node_ids = tuple(entry.node_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate health_registry_entry_id values detected")

        if len(set(node_ids)) != len(node_ids):
            raise ValueError("Duplicate node_id values detected")


def build_multi_node_health_registry_contract() -> MultiNodeHealthRegistryContract:
    """Build canonical multi-node health registry contract."""
    node_split = build_node_runtime_split_contract()
    topology_contract = build_node_topology_runtime_contract()

    node_ids = {entry.node_id for entry in node_split.entries}
    topology_ids = {entry.topology_entry_id for entry in topology_contract.entries}

    required_node_ids = {"dev_001", "home_001", "mobile_001"}
    required_topology_ids = {
        "nodetopology_dev_001",
        "nodetopology_home_001",
        "nodetopology_mobile_001",
    }

    missing_node_ids = required_node_ids - node_ids
    if missing_node_ids:
        raise ValueError(f"Missing node ids: {sorted(missing_node_ids)}")

    missing_topology_ids = required_topology_ids - topology_ids
    if missing_topology_ids:
        raise ValueError(
            f"Missing topology ids: {sorted(missing_topology_ids)}"
        )

    entries = (
        MultiNodeHealthRegistryEntry(
            health_registry_entry_id="nodehealth_dev_001",
            node_id="dev_001",
            linked_topology_entry_id="nodetopology_dev_001",
            health_class="healthy_control",
            runtime_state="normal",
            health_score=96,
            worker_capacity_available=True,
            routing_relevance="control_plane_routing",
            degraded_flag_active=False,
            explainable_required=True,
            production_path_allowed=True,
            registry_status="registered",
            description="Canonical health registry entry for DEV node.",
        ),
        MultiNodeHealthRegistryEntry(
            health_registry_entry_id="nodehealth_home_001",
            node_id="home_001",
            linked_topology_entry_id="nodetopology_home_001",
            health_class="healthy_compute",
            runtime_state="throttled",
            health_score=82,
            worker_capacity_available=True,
            routing_relevance="heavy_execution_routing",
            degraded_flag_active=True,
            explainable_required=True,
            production_path_allowed=True,
            registry_status="registered",
            description="Canonical health registry entry for HOME node.",
        ),
        MultiNodeHealthRegistryEntry(
            health_registry_entry_id="nodehealth_mobile_001",
            node_id="mobile_001",
            linked_topology_entry_id="nodetopology_mobile_001",
            health_class="healthy_mobile_proxy",
            runtime_state="normal",
            health_score=91,
            worker_capacity_available=True,
            routing_relevance="mobile_entry_routing",
            degraded_flag_active=False,
            explainable_required=True,
            production_path_allowed=True,
            registry_status="registered",
            description="Canonical health registry entry for MOBILE node.",
        ),
    )

    normal_runtime_entries = sum(
        1 for entry in entries if entry.runtime_state == "normal"
    )
    throttled_runtime_entries = sum(
        1 for entry in entries if entry.runtime_state == "throttled"
    )
    degraded_active_entries = sum(
        1 for entry in entries if entry.degraded_flag_active
    )
    registered_entries = sum(
        1 for entry in entries if entry.registry_status == "registered"
    )

    return MultiNodeHealthRegistryContract(
        total_entries=len(entries),
        normal_runtime_entries=normal_runtime_entries,
        throttled_runtime_entries=throttled_runtime_entries,
        degraded_active_entries=degraded_active_entries,
        registered_entries=registered_entries,
        entries=entries,
    )
