from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.node_runtime_split import (
    build_node_runtime_split_contract,
)
from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


TopologyEntryId = Literal[
    "nodetopology_dev_001",
    "nodetopology_home_001",
    "nodetopology_mobile_001",
]

NodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

NodeRole = Literal[
    "DEV_NODE",
    "HOME_NODE",
    "MOBILE_NODE",
]

TopologyClass = Literal[
    "development_topology",
    "home_compute_topology",
    "mobile_access_topology",
]

RuntimeConnectivityMode = Literal[
    "orchestration_and_validation",
    "heavy_compute_execution",
    "mobile_entry_and_proxy",
]

TopologyRuntimeStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_WRIST_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class NodeTopologyRuntimeEntry:
    """Canonical node topology runtime entry."""

    topology_entry_id: TopologyEntryId
    node_id: NodeId
    node_role: NodeRole
    topology_class: TopologyClass
    runtime_connectivity_mode: RuntimeConnectivityMode
    heavy_execution_allowed: bool
    control_plane_allowed: bool
    mobile_proxy_allowed: bool
    wrist_terminal_linked: bool
    linked_wrist_terminal_id: str | None
    production_path_allowed: bool
    topology_runtime_status: TopologyRuntimeStatus
    description: str

    def __post_init__(self) -> None:
        """Validate node topology runtime invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.topology_entry_id):
            raise ValueError(f"Invalid topology_entry_id: {self.topology_entry_id}")

        if not _NODE_ID_PATTERN.fullmatch(self.node_id):
            raise ValueError(f"Invalid node_id: {self.node_id}")

        if self.linked_wrist_terminal_id is not None:
            if not _WRIST_ID_PATTERN.fullmatch(self.linked_wrist_terminal_id):
                raise ValueError(
                    f"Invalid linked_wrist_terminal_id: {self.linked_wrist_terminal_id}"
                )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.topology_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.topology_entry_id}"
            )

        if self.topology_runtime_status != "defined":
            raise ValueError(
                f"topology_runtime_status must be defined: {self.topology_entry_id}"
            )

        if self.topology_entry_id == "nodetopology_dev_001":
            if self.node_id != "dev_001":
                raise ValueError("nodetopology_dev_001 must use dev_001")
            if self.node_role != "DEV_NODE":
                raise ValueError("nodetopology_dev_001 must use DEV_NODE")
            if self.topology_class != "development_topology":
                raise ValueError(
                    "nodetopology_dev_001 must use development_topology"
                )
            if self.runtime_connectivity_mode != "orchestration_and_validation":
                raise ValueError(
                    "nodetopology_dev_001 must use orchestration_and_validation"
                )
            if self.heavy_execution_allowed:
                raise ValueError(
                    "nodetopology_dev_001 must not allow heavy_execution"
                )
            if not self.control_plane_allowed:
                raise ValueError(
                    "nodetopology_dev_001 must allow control_plane"
                )
            if self.mobile_proxy_allowed:
                raise ValueError(
                    "nodetopology_dev_001 must not allow mobile_proxy"
                )
            if self.wrist_terminal_linked:
                raise ValueError(
                    "nodetopology_dev_001 must not link wrist terminal"
                )
            if self.linked_wrist_terminal_id is not None:
                raise ValueError(
                    "nodetopology_dev_001 must not have linked wrist terminal id"
                )

        if self.topology_entry_id == "nodetopology_home_001":
            if self.node_id != "home_001":
                raise ValueError("nodetopology_home_001 must use home_001")
            if self.node_role != "HOME_NODE":
                raise ValueError("nodetopology_home_001 must use HOME_NODE")
            if self.topology_class != "home_compute_topology":
                raise ValueError(
                    "nodetopology_home_001 must use home_compute_topology"
                )
            if self.runtime_connectivity_mode != "heavy_compute_execution":
                raise ValueError(
                    "nodetopology_home_001 must use heavy_compute_execution"
                )
            if not self.heavy_execution_allowed:
                raise ValueError(
                    "nodetopology_home_001 must allow heavy_execution"
                )
            if self.control_plane_allowed:
                raise ValueError(
                    "nodetopology_home_001 must not allow control_plane canonically"
                )
            if self.mobile_proxy_allowed:
                raise ValueError(
                    "nodetopology_home_001 must not allow mobile_proxy"
                )
            if self.wrist_terminal_linked:
                raise ValueError(
                    "nodetopology_home_001 must not link wrist terminal"
                )
            if self.linked_wrist_terminal_id is not None:
                raise ValueError(
                    "nodetopology_home_001 must not have linked wrist terminal id"
                )

        if self.topology_entry_id == "nodetopology_mobile_001":
            if self.node_id != "mobile_001":
                raise ValueError("nodetopology_mobile_001 must use mobile_001")
            if self.node_role != "MOBILE_NODE":
                raise ValueError("nodetopology_mobile_001 must use MOBILE_NODE")
            if self.topology_class != "mobile_access_topology":
                raise ValueError(
                    "nodetopology_mobile_001 must use mobile_access_topology"
                )
            if self.runtime_connectivity_mode != "mobile_entry_and_proxy":
                raise ValueError(
                    "nodetopology_mobile_001 must use mobile_entry_and_proxy"
                )
            if self.heavy_execution_allowed:
                raise ValueError(
                    "nodetopology_mobile_001 must not allow heavy_execution"
                )
            if self.control_plane_allowed:
                raise ValueError(
                    "nodetopology_mobile_001 must not allow control_plane"
                )
            if not self.mobile_proxy_allowed:
                raise ValueError(
                    "nodetopology_mobile_001 must allow mobile_proxy"
                )
            if not self.wrist_terminal_linked:
                raise ValueError(
                    "nodetopology_mobile_001 must link wrist terminal"
                )
            if self.linked_wrist_terminal_id != "wrist_terminal_core_001":
                raise ValueError(
                    "nodetopology_mobile_001 must link wrist_terminal_core_001"
                )


@dataclass(frozen=True, slots=True)
class NodeTopologyRuntimeContract:
    """Unified node topology runtime contract."""

    total_entries: int
    heavy_execution_entries: int
    control_plane_entries: int
    mobile_proxy_entries: int
    wrist_linked_entries: int
    defined_entries: int
    entries: tuple[NodeTopologyRuntimeEntry, ...]

    def __post_init__(self) -> None:
        """Validate node topology runtime contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        heavy_execution_entries = sum(
            1 for entry in self.entries if entry.heavy_execution_allowed
        )
        control_plane_entries = sum(
            1 for entry in self.entries if entry.control_plane_allowed
        )
        mobile_proxy_entries = sum(
            1 for entry in self.entries if entry.mobile_proxy_allowed
        )
        wrist_linked_entries = sum(
            1 for entry in self.entries if entry.wrist_terminal_linked
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.topology_runtime_status == "defined"
        )

        if self.heavy_execution_entries != heavy_execution_entries:
            raise ValueError("heavy_execution_entries must match computed count")

        if self.control_plane_entries != control_plane_entries:
            raise ValueError("control_plane_entries must match computed count")

        if self.mobile_proxy_entries != mobile_proxy_entries:
            raise ValueError("mobile_proxy_entries must match computed count")

        if self.wrist_linked_entries != wrist_linked_entries:
            raise ValueError("wrist_linked_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.topology_entry_id for entry in self.entries)
        node_ids = tuple(entry.node_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate topology_entry_id values detected")

        if len(set(node_ids)) != len(node_ids):
            raise ValueError("Duplicate node_id values detected")


def build_node_topology_runtime_contract() -> NodeTopologyRuntimeContract:
    """Build canonical node topology runtime contract."""
    node_runtime_split = build_node_runtime_split_contract()
    wrist_contract = build_wrist_terminal_contract()

    node_ids = {entry.node_id for entry in node_runtime_split.entries}
    wrist_ids = {entry.wrist_terminal_id for entry in wrist_contract.entries}

    required_node_ids = {"dev_001", "home_001", "mobile_001"}
    missing_node_ids = required_node_ids - node_ids
    if missing_node_ids:
        raise ValueError(f"Missing node ids: {sorted(missing_node_ids)}")

    if "wrist_terminal_core_001" not in wrist_ids:
        raise ValueError("Expected wrist_terminal_core_001 in wrist contract")

    entries = (
        NodeTopologyRuntimeEntry(
            topology_entry_id="nodetopology_dev_001",
            node_id="dev_001",
            node_role="DEV_NODE",
            topology_class="development_topology",
            runtime_connectivity_mode="orchestration_and_validation",
            heavy_execution_allowed=False,
            control_plane_allowed=True,
            mobile_proxy_allowed=False,
            wrist_terminal_linked=False,
            linked_wrist_terminal_id=None,
            production_path_allowed=True,
            topology_runtime_status="defined",
            description="Canonical DEV node runtime topology entry.",
        ),
        NodeTopologyRuntimeEntry(
            topology_entry_id="nodetopology_home_001",
            node_id="home_001",
            node_role="HOME_NODE",
            topology_class="home_compute_topology",
            runtime_connectivity_mode="heavy_compute_execution",
            heavy_execution_allowed=True,
            control_plane_allowed=False,
            mobile_proxy_allowed=False,
            wrist_terminal_linked=False,
            linked_wrist_terminal_id=None,
            production_path_allowed=True,
            topology_runtime_status="defined",
            description="Canonical HOME node runtime topology entry.",
        ),
        NodeTopologyRuntimeEntry(
            topology_entry_id="nodetopology_mobile_001",
            node_id="mobile_001",
            node_role="MOBILE_NODE",
            topology_class="mobile_access_topology",
            runtime_connectivity_mode="mobile_entry_and_proxy",
            heavy_execution_allowed=False,
            control_plane_allowed=False,
            mobile_proxy_allowed=True,
            wrist_terminal_linked=True,
            linked_wrist_terminal_id="wrist_terminal_core_001",
            production_path_allowed=True,
            topology_runtime_status="defined",
            description="Canonical MOBILE node runtime topology entry.",
        ),
    )

    heavy_execution_entries = sum(
        1 for entry in entries if entry.heavy_execution_allowed
    )
    control_plane_entries = sum(
        1 for entry in entries if entry.control_plane_allowed
    )
    mobile_proxy_entries = sum(
        1 for entry in entries if entry.mobile_proxy_allowed
    )
    wrist_linked_entries = sum(
        1 for entry in entries if entry.wrist_terminal_linked
    )
    defined_entries = sum(
        1 for entry in entries if entry.topology_runtime_status == "defined"
    )

    return NodeTopologyRuntimeContract(
        total_entries=len(entries),
        heavy_execution_entries=heavy_execution_entries,
        control_plane_entries=control_plane_entries,
        mobile_proxy_entries=mobile_proxy_entries,
        wrist_linked_entries=wrist_linked_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
