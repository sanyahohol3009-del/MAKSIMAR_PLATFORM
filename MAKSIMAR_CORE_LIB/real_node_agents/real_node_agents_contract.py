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
from MAKSIMAR_CORE_LIB.real_engine_backends import (
    build_real_engine_backends_contract,
)
from MAKSIMAR_CORE_LIB.secure_sync_update_transport import (
    build_secure_sync_update_transport_contract,
)


RealNodeAgentEntryId = Literal[
    "nodeagent_dev_001",
    "nodeagent_home_001",
    "nodeagent_mobile_001",
]

NodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

NodeAgentClass = Literal[
    "control_agent",
    "execution_agent",
    "mobile_proxy_agent",
]

AgentRuntimeMode = Literal[
    "control_runtime",
    "execution_runtime",
    "proxy_runtime",
]

AgentHealthClass = Literal[
    "healthy_agent",
    "healthy_degraded_agent",
]

NodeAgentStatus = Literal[
    "active",
]


_ENTRY_ID_PATTERN = re.compile(r"^nodeagent_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")
_TOPOLOGY_ID_PATTERN = re.compile(r"^nodetopology_[a-z][a-z0-9_]*$")
_HEALTH_ID_PATTERN = re.compile(r"^nodehealth_[a-z][a-z0-9_]*$")
_TRANSPORT_ID_PATTERN = re.compile(r"^transport_[a-z][a-z0-9_]*$")
_BACKEND_ID_PATTERN = re.compile(r"^realbackend_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class RealNodeAgentEntry:
    """Canonical real node agent runtime entry."""

    real_node_agent_entry_id: RealNodeAgentEntryId
    node_id: NodeId
    linked_topology_entry_id: str
    linked_health_entry_id: str
    linked_transport_entry_id: str
    linked_real_backend_entry_id: str | None
    node_agent_class: NodeAgentClass
    agent_runtime_mode: AgentRuntimeMode
    agent_health_class: AgentHealthClass
    control_plane_attached: bool
    heavy_execution_attached: bool
    mobile_proxy_attached: bool
    runtime_loaded: bool
    explainable_required: bool
    production_path_allowed: bool
    node_agent_status: NodeAgentStatus
    description: str

    def __post_init__(self) -> None:
        """Validate real node agent invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.real_node_agent_entry_id):
            raise ValueError(
                f"Invalid real_node_agent_entry_id: {self.real_node_agent_entry_id}"
            )

        if not _NODE_ID_PATTERN.fullmatch(self.node_id):
            raise ValueError(f"Invalid node_id: {self.node_id}")

        if not _TOPOLOGY_ID_PATTERN.fullmatch(self.linked_topology_entry_id):
            raise ValueError(
                f"Invalid linked_topology_entry_id: {self.linked_topology_entry_id}"
            )

        if not _HEALTH_ID_PATTERN.fullmatch(self.linked_health_entry_id):
            raise ValueError(
                f"Invalid linked_health_entry_id: {self.linked_health_entry_id}"
            )

        if not _TRANSPORT_ID_PATTERN.fullmatch(self.linked_transport_entry_id):
            raise ValueError(
                f"Invalid linked_transport_entry_id: {self.linked_transport_entry_id}"
            )

        if self.linked_real_backend_entry_id is not None:
            if not _BACKEND_ID_PATTERN.fullmatch(self.linked_real_backend_entry_id):
                raise ValueError(
                    f"Invalid linked_real_backend_entry_id: {self.linked_real_backend_entry_id}"
                )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.real_node_agent_entry_id}"
            )

        if not self.runtime_loaded:
            raise ValueError(
                f"runtime_loaded must be True: {self.real_node_agent_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.real_node_agent_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.real_node_agent_entry_id}"
            )

        if self.node_agent_status != "active":
            raise ValueError(
                f"node_agent_status must be active: {self.real_node_agent_entry_id}"
            )

        if self.real_node_agent_entry_id == "nodeagent_dev_001":
            if self.node_id != "dev_001":
                raise ValueError("nodeagent_dev_001 must use dev_001")
            if self.linked_topology_entry_id != "nodetopology_dev_001":
                raise ValueError(
                    "nodeagent_dev_001 must link nodetopology_dev_001"
                )
            if self.linked_health_entry_id != "nodehealth_dev_001":
                raise ValueError(
                    "nodeagent_dev_001 must link nodehealth_dev_001"
                )
            if self.linked_transport_entry_id != "transport_dev_local_001":
                raise ValueError(
                    "nodeagent_dev_001 must link transport_dev_local_001"
                )
            if self.linked_real_backend_entry_id is not None:
                raise ValueError(
                    "nodeagent_dev_001 must not link real backend directly"
                )
            if self.node_agent_class != "control_agent":
                raise ValueError("nodeagent_dev_001 must use control_agent")
            if self.agent_runtime_mode != "control_runtime":
                raise ValueError("nodeagent_dev_001 must use control_runtime")
            if self.agent_health_class != "healthy_agent":
                raise ValueError("nodeagent_dev_001 must use healthy_agent")
            if not self.control_plane_attached:
                raise ValueError(
                    "nodeagent_dev_001 must have control_plane_attached=True"
                )
            if self.heavy_execution_attached:
                raise ValueError(
                    "nodeagent_dev_001 must not have heavy_execution_attached"
                )
            if self.mobile_proxy_attached:
                raise ValueError(
                    "nodeagent_dev_001 must not have mobile_proxy_attached"
                )

        if self.real_node_agent_entry_id == "nodeagent_home_001":
            if self.node_id != "home_001":
                raise ValueError("nodeagent_home_001 must use home_001")
            if self.linked_topology_entry_id != "nodetopology_home_001":
                raise ValueError(
                    "nodeagent_home_001 must link nodetopology_home_001"
                )
            if self.linked_health_entry_id != "nodehealth_home_001":
                raise ValueError(
                    "nodeagent_home_001 must link nodehealth_home_001"
                )
            if self.linked_transport_entry_id != "transport_dev_home_001":
                raise ValueError(
                    "nodeagent_home_001 must link transport_dev_home_001"
                )
            if self.linked_real_backend_entry_id != "realbackend_simulation_native_001":
                raise ValueError(
                    "nodeagent_home_001 must link realbackend_simulation_native_001"
                )
            if self.node_agent_class != "execution_agent":
                raise ValueError("nodeagent_home_001 must use execution_agent")
            if self.agent_runtime_mode != "execution_runtime":
                raise ValueError("nodeagent_home_001 must use execution_runtime")
            if self.agent_health_class != "healthy_degraded_agent":
                raise ValueError(
                    "nodeagent_home_001 must use healthy_degraded_agent"
                )
            if self.control_plane_attached:
                raise ValueError(
                    "nodeagent_home_001 must not have control_plane_attached"
                )
            if not self.heavy_execution_attached:
                raise ValueError(
                    "nodeagent_home_001 must have heavy_execution_attached=True"
                )
            if self.mobile_proxy_attached:
                raise ValueError(
                    "nodeagent_home_001 must not have mobile_proxy_attached"
                )

        if self.real_node_agent_entry_id == "nodeagent_mobile_001":
            if self.node_id != "mobile_001":
                raise ValueError("nodeagent_mobile_001 must use mobile_001")
            if self.linked_topology_entry_id != "nodetopology_mobile_001":
                raise ValueError(
                    "nodeagent_mobile_001 must link nodetopology_mobile_001"
                )
            if self.linked_health_entry_id != "nodehealth_mobile_001":
                raise ValueError(
                    "nodeagent_mobile_001 must link nodehealth_mobile_001"
                )
            if self.linked_transport_entry_id != "transport_mobile_local_001":
                raise ValueError(
                    "nodeagent_mobile_001 must link transport_mobile_local_001"
                )
            if self.linked_real_backend_entry_id != "realbackend_display_python_001":
                raise ValueError(
                    "nodeagent_mobile_001 must link realbackend_display_python_001"
                )
            if self.node_agent_class != "mobile_proxy_agent":
                raise ValueError("nodeagent_mobile_001 must use mobile_proxy_agent")
            if self.agent_runtime_mode != "proxy_runtime":
                raise ValueError("nodeagent_mobile_001 must use proxy_runtime")
            if self.agent_health_class != "healthy_agent":
                raise ValueError("nodeagent_mobile_001 must use healthy_agent")
            if self.control_plane_attached:
                raise ValueError(
                    "nodeagent_mobile_001 must not have control_plane_attached"
                )
            if self.heavy_execution_attached:
                raise ValueError(
                    "nodeagent_mobile_001 must not have heavy_execution_attached"
                )
            if not self.mobile_proxy_attached:
                raise ValueError(
                    "nodeagent_mobile_001 must have mobile_proxy_attached=True"
                )


@dataclass(frozen=True, slots=True)
class RealNodeAgentsContract:
    """Unified real node agents contract."""

    total_entries: int
    control_agent_entries: int
    execution_agent_entries: int
    mobile_proxy_agent_entries: int
    active_entries: int
    entries: tuple[RealNodeAgentEntry, ...]

    def __post_init__(self) -> None:
        """Validate real node agents contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        control_agent_entries = sum(
            1 for entry in self.entries if entry.node_agent_class == "control_agent"
        )
        execution_agent_entries = sum(
            1 for entry in self.entries if entry.node_agent_class == "execution_agent"
        )
        mobile_proxy_agent_entries = sum(
            1 for entry in self.entries if entry.node_agent_class == "mobile_proxy_agent"
        )
        active_entries = sum(
            1 for entry in self.entries if entry.node_agent_status == "active"
        )

        if self.control_agent_entries != control_agent_entries:
            raise ValueError("control_agent_entries must match computed count")

        if self.execution_agent_entries != execution_agent_entries:
            raise ValueError("execution_agent_entries must match computed count")

        if self.mobile_proxy_agent_entries != mobile_proxy_agent_entries:
            raise ValueError("mobile_proxy_agent_entries must match computed count")

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        entry_ids = tuple(entry.real_node_agent_entry_id for entry in self.entries)
        node_ids = tuple(entry.node_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate real_node_agent_entry_id values detected")

        if len(set(node_ids)) != len(node_ids):
            raise ValueError("Duplicate node_id values detected")


def build_real_node_agents_contract() -> RealNodeAgentsContract:
    """Build canonical real node agents contract."""
    topology_contract = build_node_topology_runtime_contract()
    health_contract = build_multi_node_health_registry_contract()
    transport_contract = build_secure_sync_update_transport_contract()
    backend_contract = build_real_engine_backends_contract()

    topology_ids = {entry.topology_entry_id for entry in topology_contract.entries}
    health_ids = {entry.health_registry_entry_id for entry in health_contract.entries}
    transport_ids = {entry.secure_transport_entry_id for entry in transport_contract.entries}
    backend_ids = {entry.real_backend_entry_id for entry in backend_contract.entries}

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
    required_transport_ids = {
        "transport_dev_local_001",
        "transport_dev_home_001",
        "transport_mobile_local_001",
    }
    required_backend_ids = {
        "realbackend_simulation_native_001",
        "realbackend_display_python_001",
    }

    missing_topology_ids = required_topology_ids - topology_ids
    if missing_topology_ids:
        raise ValueError(
            f"Missing topology ids: {sorted(missing_topology_ids)}"
        )

    missing_health_ids = required_health_ids - health_ids
    if missing_health_ids:
        raise ValueError(f"Missing health ids: {sorted(missing_health_ids)}")

    missing_transport_ids = required_transport_ids - transport_ids
    if missing_transport_ids:
        raise ValueError(
            f"Missing transport ids: {sorted(missing_transport_ids)}"
        )

    missing_backend_ids = required_backend_ids - backend_ids
    if missing_backend_ids:
        raise ValueError(
            f"Missing real backend ids: {sorted(missing_backend_ids)}"
        )

    entries = (
        RealNodeAgentEntry(
            real_node_agent_entry_id="nodeagent_dev_001",
            node_id="dev_001",
            linked_topology_entry_id="nodetopology_dev_001",
            linked_health_entry_id="nodehealth_dev_001",
            linked_transport_entry_id="transport_dev_local_001",
            linked_real_backend_entry_id=None,
            node_agent_class="control_agent",
            agent_runtime_mode="control_runtime",
            agent_health_class="healthy_agent",
            control_plane_attached=True,
            heavy_execution_attached=False,
            mobile_proxy_attached=False,
            runtime_loaded=True,
            explainable_required=True,
            production_path_allowed=True,
            node_agent_status="active",
            description="Canonical real node agent for DEV control runtime.",
        ),
        RealNodeAgentEntry(
            real_node_agent_entry_id="nodeagent_home_001",
            node_id="home_001",
            linked_topology_entry_id="nodetopology_home_001",
            linked_health_entry_id="nodehealth_home_001",
            linked_transport_entry_id="transport_dev_home_001",
            linked_real_backend_entry_id="realbackend_simulation_native_001",
            node_agent_class="execution_agent",
            agent_runtime_mode="execution_runtime",
            agent_health_class="healthy_degraded_agent",
            control_plane_attached=False,
            heavy_execution_attached=True,
            mobile_proxy_attached=False,
            runtime_loaded=True,
            explainable_required=True,
            production_path_allowed=True,
            node_agent_status="active",
            description="Canonical real node agent for HOME execution runtime.",
        ),
        RealNodeAgentEntry(
            real_node_agent_entry_id="nodeagent_mobile_001",
            node_id="mobile_001",
            linked_topology_entry_id="nodetopology_mobile_001",
            linked_health_entry_id="nodehealth_mobile_001",
            linked_transport_entry_id="transport_mobile_local_001",
            linked_real_backend_entry_id="realbackend_display_python_001",
            node_agent_class="mobile_proxy_agent",
            agent_runtime_mode="proxy_runtime",
            agent_health_class="healthy_agent",
            control_plane_attached=False,
            heavy_execution_attached=False,
            mobile_proxy_attached=True,
            runtime_loaded=True,
            explainable_required=True,
            production_path_allowed=True,
            node_agent_status="active",
            description="Canonical real node agent for MOBILE proxy runtime.",
        ),
    )

    control_agent_entries = sum(
        1 for entry in entries if entry.node_agent_class == "control_agent"
    )
    execution_agent_entries = sum(
        1 for entry in entries if entry.node_agent_class == "execution_agent"
    )
    mobile_proxy_agent_entries = sum(
        1 for entry in entries if entry.node_agent_class == "mobile_proxy_agent"
    )
    active_entries = sum(
        1 for entry in entries if entry.node_agent_status == "active"
    )

    return RealNodeAgentsContract(
        total_entries=len(entries),
        control_agent_entries=control_agent_entries,
        execution_agent_entries=execution_agent_entries,
        mobile_proxy_agent_entries=mobile_proxy_agent_entries,
        active_entries=active_entries,
        entries=entries,
    )
