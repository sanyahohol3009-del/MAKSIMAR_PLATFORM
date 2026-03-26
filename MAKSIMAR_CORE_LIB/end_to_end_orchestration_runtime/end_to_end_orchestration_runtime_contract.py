from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.distributed_workload_placement import (
    build_distributed_workload_placement_contract,
)
from MAKSIMAR_CORE_LIB.persistent_storage_migrations import (
    build_persistent_storage_migrations_contract,
)
from MAKSIMAR_CORE_LIB.real_engine_backends import (
    build_real_engine_backends_contract,
)
from MAKSIMAR_CORE_LIB.real_node_agents import (
    build_real_node_agents_contract,
)
from MAKSIMAR_CORE_LIB.secure_sync_update_transport import (
    build_secure_sync_update_transport_contract,
)


OrchestrationEntryId = Literal[
    "orchestration_control_plane_001",
    "orchestration_heavy_execution_001",
    "orchestration_mobile_entry_001",
]

WorkloadClass = Literal[
    "control_plane_workload",
    "heavy_execution_workload",
    "mobile_entry_workload",
]

OrchestrationFlowClass = Literal[
    "local_control_flow",
    "restricted_execution_flow",
    "local_mobile_flow",
]

RuntimeDecisionClass = Literal[
    "orchestrated",
]

OrchestrationStatus = Literal[
    "active",
]


_ENTRY_ID_PATTERN = re.compile(r"^orchestration_[a-z][a-z0-9_]*$")
_AGENT_ID_PATTERN = re.compile(r"^nodeagent_[a-z][a-z0-9_]*$")
_BACKEND_ID_PATTERN = re.compile(r"^realbackend_[a-z][a-z0-9_]*$")
_STORAGE_ID_PATTERN = re.compile(r"^storage_[a-z][a-z0-9_]*$")
_PLACEMENT_ID_PATTERN = re.compile(r"^placement_[a-z][a-z0-9_]*$")
_TRANSPORT_ID_PATTERN = re.compile(r"^transport_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class EndToEndOrchestrationRuntimeEntry:
    """Canonical end-to-end orchestration runtime entry."""

    orchestration_entry_id: OrchestrationEntryId
    workload_class: WorkloadClass
    linked_node_agent_id: str
    linked_real_backend_id: str | None
    linked_storage_entry_id: str
    linked_placement_entry_id: str
    linked_transport_entry_id: str
    orchestration_flow_class: OrchestrationFlowClass
    runtime_decision_class: RuntimeDecisionClass
    storage_persistence_required: bool
    transport_path_required: bool
    backend_runtime_required: bool
    explainable_required: bool
    production_path_allowed: bool
    orchestration_status: OrchestrationStatus
    description: str

    def __post_init__(self) -> None:
        """Validate end-to-end orchestration runtime invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.orchestration_entry_id):
            raise ValueError(
                f"Invalid orchestration_entry_id: {self.orchestration_entry_id}"
            )

        if not _AGENT_ID_PATTERN.fullmatch(self.linked_node_agent_id):
            raise ValueError(
                f"Invalid linked_node_agent_id: {self.linked_node_agent_id}"
            )

        if self.linked_real_backend_id is not None:
            if not _BACKEND_ID_PATTERN.fullmatch(self.linked_real_backend_id):
                raise ValueError(
                    f"Invalid linked_real_backend_id: {self.linked_real_backend_id}"
                )

        if not _STORAGE_ID_PATTERN.fullmatch(self.linked_storage_entry_id):
            raise ValueError(
                f"Invalid linked_storage_entry_id: {self.linked_storage_entry_id}"
            )

        if not _PLACEMENT_ID_PATTERN.fullmatch(self.linked_placement_entry_id):
            raise ValueError(
                f"Invalid linked_placement_entry_id: {self.linked_placement_entry_id}"
            )

        if not _TRANSPORT_ID_PATTERN.fullmatch(self.linked_transport_entry_id):
            raise ValueError(
                f"Invalid linked_transport_entry_id: {self.linked_transport_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.orchestration_entry_id}"
            )

        if self.runtime_decision_class != "orchestrated":
            raise ValueError(
                f"runtime_decision_class must be orchestrated: {self.orchestration_entry_id}"
            )

        if not self.storage_persistence_required:
            raise ValueError(
                f"storage_persistence_required must be True: {self.orchestration_entry_id}"
            )

        if not self.transport_path_required:
            raise ValueError(
                f"transport_path_required must be True: {self.orchestration_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.orchestration_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.orchestration_entry_id}"
            )

        if self.orchestration_status != "active":
            raise ValueError(
                f"orchestration_status must be active: {self.orchestration_entry_id}"
            )

        if self.orchestration_entry_id == "orchestration_control_plane_001":
            if self.workload_class != "control_plane_workload":
                raise ValueError(
                    "orchestration_control_plane_001 must use control_plane_workload"
                )
            if self.linked_node_agent_id != "nodeagent_dev_001":
                raise ValueError(
                    "orchestration_control_plane_001 must link nodeagent_dev_001"
                )
            if self.linked_real_backend_id is not None:
                raise ValueError(
                    "orchestration_control_plane_001 must not link real backend directly"
                )
            if self.linked_storage_entry_id != "storage_dev_metadata_001":
                raise ValueError(
                    "orchestration_control_plane_001 must link storage_dev_metadata_001"
                )
            if self.linked_placement_entry_id != "placement_control_plane_001":
                raise ValueError(
                    "orchestration_control_plane_001 must link placement_control_plane_001"
                )
            if self.linked_transport_entry_id != "transport_dev_local_001":
                raise ValueError(
                    "orchestration_control_plane_001 must link transport_dev_local_001"
                )
            if self.orchestration_flow_class != "local_control_flow":
                raise ValueError(
                    "orchestration_control_plane_001 must use local_control_flow"
                )
            if self.backend_runtime_required:
                raise ValueError(
                    "orchestration_control_plane_001 must not require backend runtime directly"
                )

        if self.orchestration_entry_id == "orchestration_heavy_execution_001":
            if self.workload_class != "heavy_execution_workload":
                raise ValueError(
                    "orchestration_heavy_execution_001 must use heavy_execution_workload"
                )
            if self.linked_node_agent_id != "nodeagent_home_001":
                raise ValueError(
                    "orchestration_heavy_execution_001 must link nodeagent_home_001"
                )
            if self.linked_real_backend_id != "realbackend_simulation_native_001":
                raise ValueError(
                    "orchestration_heavy_execution_001 must link realbackend_simulation_native_001"
                )
            if self.linked_storage_entry_id != "storage_home_artifacts_001":
                raise ValueError(
                    "orchestration_heavy_execution_001 must link storage_home_artifacts_001"
                )
            if self.linked_placement_entry_id != "placement_heavy_execution_001":
                raise ValueError(
                    "orchestration_heavy_execution_001 must link placement_heavy_execution_001"
                )
            if self.linked_transport_entry_id != "transport_dev_home_001":
                raise ValueError(
                    "orchestration_heavy_execution_001 must link transport_dev_home_001"
                )
            if self.orchestration_flow_class != "restricted_execution_flow":
                raise ValueError(
                    "orchestration_heavy_execution_001 must use restricted_execution_flow"
                )
            if not self.backend_runtime_required:
                raise ValueError(
                    "orchestration_heavy_execution_001 must require backend runtime"
                )

        if self.orchestration_entry_id == "orchestration_mobile_entry_001":
            if self.workload_class != "mobile_entry_workload":
                raise ValueError(
                    "orchestration_mobile_entry_001 must use mobile_entry_workload"
                )
            if self.linked_node_agent_id != "nodeagent_mobile_001":
                raise ValueError(
                    "orchestration_mobile_entry_001 must link nodeagent_mobile_001"
                )
            if self.linked_real_backend_id != "realbackend_display_python_001":
                raise ValueError(
                    "orchestration_mobile_entry_001 must link realbackend_display_python_001"
                )
            if self.linked_storage_entry_id != "storage_mobile_local_state_001":
                raise ValueError(
                    "orchestration_mobile_entry_001 must link storage_mobile_local_state_001"
                )
            if self.linked_placement_entry_id != "placement_mobile_entry_001":
                raise ValueError(
                    "orchestration_mobile_entry_001 must link placement_mobile_entry_001"
                )
            if self.linked_transport_entry_id != "transport_mobile_local_001":
                raise ValueError(
                    "orchestration_mobile_entry_001 must link transport_mobile_local_001"
                )
            if self.orchestration_flow_class != "local_mobile_flow":
                raise ValueError(
                    "orchestration_mobile_entry_001 must use local_mobile_flow"
                )
            if not self.backend_runtime_required:
                raise ValueError(
                    "orchestration_mobile_entry_001 must require backend runtime"
                )


@dataclass(frozen=True, slots=True)
class EndToEndOrchestrationRuntimeContract:
    """Unified end-to-end orchestration runtime contract."""

    total_entries: int
    backend_required_entries: int
    local_flow_entries: int
    restricted_flow_entries: int
    active_entries: int
    entries: tuple[EndToEndOrchestrationRuntimeEntry, ...]

    def __post_init__(self) -> None:
        """Validate end-to-end orchestration runtime contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        backend_required_entries = sum(
            1 for entry in self.entries if entry.backend_runtime_required
        )
        local_flow_entries = sum(
            1
            for entry in self.entries
            if entry.orchestration_flow_class in ("local_control_flow", "local_mobile_flow")
        )
        restricted_flow_entries = sum(
            1
            for entry in self.entries
            if entry.orchestration_flow_class == "restricted_execution_flow"
        )
        active_entries = sum(
            1 for entry in self.entries if entry.orchestration_status == "active"
        )

        if self.backend_required_entries != backend_required_entries:
            raise ValueError("backend_required_entries must match computed count")

        if self.local_flow_entries != local_flow_entries:
            raise ValueError("local_flow_entries must match computed count")

        if self.restricted_flow_entries != restricted_flow_entries:
            raise ValueError("restricted_flow_entries must match computed count")

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        entry_ids = tuple(entry.orchestration_entry_id for entry in self.entries)
        workloads = tuple(entry.workload_class for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate orchestration_entry_id values detected")

        if len(set(workloads)) != len(workloads):
            raise ValueError("Duplicate workload_class values detected")


def build_end_to_end_orchestration_runtime_contract() -> EndToEndOrchestrationRuntimeContract:
    """Build canonical end-to-end orchestration runtime contract."""
    node_agent_contract = build_real_node_agents_contract()
    backend_contract = build_real_engine_backends_contract()
    storage_contract = build_persistent_storage_migrations_contract()
    placement_contract = build_distributed_workload_placement_contract()
    transport_contract = build_secure_sync_update_transport_contract()

    node_agent_ids = {entry.real_node_agent_entry_id for entry in node_agent_contract.entries}
    backend_ids = {entry.real_backend_entry_id for entry in backend_contract.entries}
    storage_ids = {entry.persistent_storage_entry_id for entry in storage_contract.entries}
    placement_ids = {entry.placement_entry_id for entry in placement_contract.entries}
    transport_ids = {entry.secure_transport_entry_id for entry in transport_contract.entries}

    required_node_agent_ids = {
        "nodeagent_dev_001",
        "nodeagent_home_001",
        "nodeagent_mobile_001",
    }
    required_backend_ids = {
        "realbackend_simulation_native_001",
        "realbackend_display_python_001",
    }
    required_storage_ids = {
        "storage_dev_metadata_001",
        "storage_home_artifacts_001",
        "storage_mobile_local_state_001",
    }
    required_placement_ids = {
        "placement_control_plane_001",
        "placement_heavy_execution_001",
        "placement_mobile_entry_001",
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

    missing_backend_ids = required_backend_ids - backend_ids
    if missing_backend_ids:
        raise ValueError(
            f"Missing backend ids: {sorted(missing_backend_ids)}"
        )

    missing_storage_ids = required_storage_ids - storage_ids
    if missing_storage_ids:
        raise ValueError(
            f"Missing storage ids: {sorted(missing_storage_ids)}"
        )

    missing_placement_ids = required_placement_ids - placement_ids
    if missing_placement_ids:
        raise ValueError(
            f"Missing placement ids: {sorted(missing_placement_ids)}"
        )

    missing_transport_ids = required_transport_ids - transport_ids
    if missing_transport_ids:
        raise ValueError(
            f"Missing transport ids: {sorted(missing_transport_ids)}"
        )

    entries = (
        EndToEndOrchestrationRuntimeEntry(
            orchestration_entry_id="orchestration_control_plane_001",
            workload_class="control_plane_workload",
            linked_node_agent_id="nodeagent_dev_001",
            linked_real_backend_id=None,
            linked_storage_entry_id="storage_dev_metadata_001",
            linked_placement_entry_id="placement_control_plane_001",
            linked_transport_entry_id="transport_dev_local_001",
            orchestration_flow_class="local_control_flow",
            runtime_decision_class="orchestrated",
            storage_persistence_required=True,
            transport_path_required=True,
            backend_runtime_required=False,
            explainable_required=True,
            production_path_allowed=True,
            orchestration_status="active",
            description="Canonical end-to-end orchestration for control plane workload.",
        ),
        EndToEndOrchestrationRuntimeEntry(
            orchestration_entry_id="orchestration_heavy_execution_001",
            workload_class="heavy_execution_workload",
            linked_node_agent_id="nodeagent_home_001",
            linked_real_backend_id="realbackend_simulation_native_001",
            linked_storage_entry_id="storage_home_artifacts_001",
            linked_placement_entry_id="placement_heavy_execution_001",
            linked_transport_entry_id="transport_dev_home_001",
            orchestration_flow_class="restricted_execution_flow",
            runtime_decision_class="orchestrated",
            storage_persistence_required=True,
            transport_path_required=True,
            backend_runtime_required=True,
            explainable_required=True,
            production_path_allowed=True,
            orchestration_status="active",
            description="Canonical end-to-end orchestration for heavy execution workload.",
        ),
        EndToEndOrchestrationRuntimeEntry(
            orchestration_entry_id="orchestration_mobile_entry_001",
            workload_class="mobile_entry_workload",
            linked_node_agent_id="nodeagent_mobile_001",
            linked_real_backend_id="realbackend_display_python_001",
            linked_storage_entry_id="storage_mobile_local_state_001",
            linked_placement_entry_id="placement_mobile_entry_001",
            linked_transport_entry_id="transport_mobile_local_001",
            orchestration_flow_class="local_mobile_flow",
            runtime_decision_class="orchestrated",
            storage_persistence_required=True,
            transport_path_required=True,
            backend_runtime_required=True,
            explainable_required=True,
            production_path_allowed=True,
            orchestration_status="active",
            description="Canonical end-to-end orchestration for mobile entry workload.",
        ),
    )

    backend_required_entries = sum(
        1 for entry in entries if entry.backend_runtime_required
    )
    local_flow_entries = sum(
        1
        for entry in entries
        if entry.orchestration_flow_class in ("local_control_flow", "local_mobile_flow")
    )
    restricted_flow_entries = sum(
        1
        for entry in entries
        if entry.orchestration_flow_class == "restricted_execution_flow"
    )
    active_entries = sum(
        1 for entry in entries if entry.orchestration_status == "active"
    )

    return EndToEndOrchestrationRuntimeContract(
        total_entries=len(entries),
        backend_required_entries=backend_required_entries,
        local_flow_entries=local_flow_entries,
        restricted_flow_entries=restricted_flow_entries,
        active_entries=active_entries,
        entries=entries,
    )
