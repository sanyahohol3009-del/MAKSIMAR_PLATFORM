from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.backend_selection_policy import (
    build_backend_selection_policy_contract,
)
from MAKSIMAR_CORE_LIB.engine_adapter_boundary import (
    build_engine_adapter_boundary_contract,
)
from MAKSIMAR_CORE_LIB.engine_capability_contract import (
    build_engine_capability_contract,
)


ObservabilityEntryId = Literal[
    "engineobs_simulation_001",
    "engineobs_optics_001",
    "engineobs_display_transform_001",
]

SelectedBackendSlot = Literal[
    "python_backend_slot",
    "native_backend_slot",
    "gpu_backend_slot",
    "fallback_backend_slot",
]

LatencyPathClass = Literal[
    "bounded_realtime_path",
    "interactive_path",
    "fallback_interactive_path",
]

MismatchCondition = Literal[
    "none",
    "fallback_active",
]

ObservabilityBindingStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^engineobs_[a-z][a-z0-9_]*$")
_POLICY_ID_PATTERN = re.compile(r"^backendpolicy_[a-z][a-z0-9_]*$")
_CAPABILITY_ID_PATTERN = re.compile(r"^enginecap_[a-z][a-z0-9_]*$")
_ADAPTER_ID_PATTERN = re.compile(r"^engineadapter_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class EngineObservabilityBindingEntry:
    """Canonical engine observability binding entry."""

    observability_entry_id: ObservabilityEntryId
    linked_backend_policy_id: str
    linked_engine_capability_id: str
    linked_engine_adapter_id: str
    selected_backend_slot: SelectedBackendSlot
    latency_path_class: LatencyPathClass
    fallback_active: bool
    mismatch_condition: MismatchCondition
    selected_backend_metric_required: bool
    latency_metric_required: bool
    fallback_switch_metric_required: bool
    explainable_required: bool
    production_path_allowed: bool
    binding_status: ObservabilityBindingStatus
    description: str

    def __post_init__(self) -> None:
        """Validate engine observability binding invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.observability_entry_id):
            raise ValueError(
                f"Invalid observability_entry_id: {self.observability_entry_id}"
            )

        if not _POLICY_ID_PATTERN.fullmatch(self.linked_backend_policy_id):
            raise ValueError(
                f"Invalid linked_backend_policy_id: {self.linked_backend_policy_id}"
            )

        if not _CAPABILITY_ID_PATTERN.fullmatch(self.linked_engine_capability_id):
            raise ValueError(
                f"Invalid linked_engine_capability_id: {self.linked_engine_capability_id}"
            )

        if not _ADAPTER_ID_PATTERN.fullmatch(self.linked_engine_adapter_id):
            raise ValueError(
                f"Invalid linked_engine_adapter_id: {self.linked_engine_adapter_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.observability_entry_id}"
            )

        if not self.selected_backend_metric_required:
            raise ValueError(
                f"selected_backend_metric_required must be True: {self.observability_entry_id}"
            )

        if not self.latency_metric_required:
            raise ValueError(
                f"latency_metric_required must be True: {self.observability_entry_id}"
            )

        if not self.fallback_switch_metric_required:
            raise ValueError(
                f"fallback_switch_metric_required must be True: {self.observability_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.observability_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.observability_entry_id}"
            )

        if self.binding_status != "defined":
            raise ValueError(
                f"binding_status must be defined: {self.observability_entry_id}"
            )

        if self.observability_entry_id == "engineobs_simulation_001":
            if self.linked_backend_policy_id != "backendpolicy_simulation_001":
                raise ValueError(
                    "engineobs_simulation_001 must link backendpolicy_simulation_001"
                )
            if self.linked_engine_capability_id != "enginecap_simulation_001":
                raise ValueError(
                    "engineobs_simulation_001 must link enginecap_simulation_001"
                )
            if self.linked_engine_adapter_id != "engineadapter_simulation_worker_001":
                raise ValueError(
                    "engineobs_simulation_001 must link engineadapter_simulation_worker_001"
                )
            if self.selected_backend_slot != "native_backend_slot":
                raise ValueError(
                    "engineobs_simulation_001 must select native_backend_slot"
                )
            if self.latency_path_class != "bounded_realtime_path":
                raise ValueError(
                    "engineobs_simulation_001 must use bounded_realtime_path"
                )
            if self.fallback_active:
                raise ValueError(
                    "engineobs_simulation_001 must not have fallback_active"
                )
            if self.mismatch_condition != "none":
                raise ValueError("engineobs_simulation_001 must use mismatch_condition=none")

        if self.observability_entry_id == "engineobs_optics_001":
            if self.linked_backend_policy_id != "backendpolicy_optics_001":
                raise ValueError(
                    "engineobs_optics_001 must link backendpolicy_optics_001"
                )
            if self.linked_engine_capability_id != "enginecap_optics_001":
                raise ValueError(
                    "engineobs_optics_001 must link enginecap_optics_001"
                )
            if self.linked_engine_adapter_id != "engineadapter_optics_worker_001":
                raise ValueError(
                    "engineobs_optics_001 must link engineadapter_optics_worker_001"
                )
            if self.selected_backend_slot != "gpu_backend_slot":
                raise ValueError(
                    "engineobs_optics_001 must select gpu_backend_slot"
                )
            if self.latency_path_class != "interactive_path":
                raise ValueError(
                    "engineobs_optics_001 must use interactive_path"
                )
            if self.fallback_active:
                raise ValueError(
                    "engineobs_optics_001 must not have fallback_active"
                )
            if self.mismatch_condition != "none":
                raise ValueError("engineobs_optics_001 must use mismatch_condition=none")

        if self.observability_entry_id == "engineobs_display_transform_001":
            if self.linked_backend_policy_id != "backendpolicy_display_transform_001":
                raise ValueError(
                    "engineobs_display_transform_001 must link backendpolicy_display_transform_001"
                )
            if self.linked_engine_capability_id != "enginecap_display_transform_001":
                raise ValueError(
                    "engineobs_display_transform_001 must link enginecap_display_transform_001"
                )
            if self.linked_engine_adapter_id != "engineadapter_display_transform_001":
                raise ValueError(
                    "engineobs_display_transform_001 must link engineadapter_display_transform_001"
                )
            if self.selected_backend_slot != "python_backend_slot":
                raise ValueError(
                    "engineobs_display_transform_001 must select python_backend_slot"
                )
            if self.latency_path_class != "fallback_interactive_path":
                raise ValueError(
                    "engineobs_display_transform_001 must use fallback_interactive_path"
                )
            if not self.fallback_active:
                raise ValueError(
                    "engineobs_display_transform_001 must have fallback_active=True"
                )
            if self.mismatch_condition != "fallback_active":
                raise ValueError(
                    "engineobs_display_transform_001 must use mismatch_condition=fallback_active"
                )


@dataclass(frozen=True, slots=True)
class EngineObservabilityBindingContract:
    """Unified engine observability binding contract."""

    total_entries: int
    gpu_selected_entries: int
    fallback_active_entries: int
    interactive_latency_entries: int
    defined_entries: int
    entries: tuple[EngineObservabilityBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate engine observability binding contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        gpu_selected_entries = sum(
            1 for entry in self.entries if entry.selected_backend_slot == "gpu_backend_slot"
        )
        fallback_active_entries = sum(
            1 for entry in self.entries if entry.fallback_active
        )
        interactive_latency_entries = sum(
            1
            for entry in self.entries
            if entry.latency_path_class in ("interactive_path", "fallback_interactive_path")
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.binding_status == "defined"
        )

        if self.gpu_selected_entries != gpu_selected_entries:
            raise ValueError("gpu_selected_entries must match computed count")

        if self.fallback_active_entries != fallback_active_entries:
            raise ValueError("fallback_active_entries must match computed count")

        if self.interactive_latency_entries != interactive_latency_entries:
            raise ValueError(
                "interactive_latency_entries must match computed count"
            )

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.observability_entry_id for entry in self.entries)
        policy_ids = tuple(entry.linked_backend_policy_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate observability_entry_id values detected")

        if len(set(policy_ids)) != len(policy_ids):
            raise ValueError("Duplicate linked_backend_policy_id values detected")


def build_engine_observability_binding_contract() -> EngineObservabilityBindingContract:
    """Build canonical engine observability binding contract."""
    policy_contract = build_backend_selection_policy_contract()
    capability_contract = build_engine_capability_contract()
    adapter_contract = build_engine_adapter_boundary_contract()

    policy_ids = {entry.backend_policy_id for entry in policy_contract.entries}
    capability_ids = {entry.engine_capability_id for entry in capability_contract.entries}
    adapter_ids = {entry.engine_adapter_id for entry in adapter_contract.entries}

    required_policy_ids = {
        "backendpolicy_simulation_001",
        "backendpolicy_optics_001",
        "backendpolicy_display_transform_001",
    }
    required_capability_ids = {
        "enginecap_simulation_001",
        "enginecap_optics_001",
        "enginecap_display_transform_001",
    }
    required_adapter_ids = {
        "engineadapter_simulation_worker_001",
        "engineadapter_optics_worker_001",
        "engineadapter_display_transform_001",
    }

    missing_policy_ids = required_policy_ids - policy_ids
    if missing_policy_ids:
        raise ValueError(
            f"Missing backend policy ids: {sorted(missing_policy_ids)}"
        )

    missing_capability_ids = required_capability_ids - capability_ids
    if missing_capability_ids:
        raise ValueError(
            f"Missing engine capability ids: {sorted(missing_capability_ids)}"
        )

    missing_adapter_ids = required_adapter_ids - adapter_ids
    if missing_adapter_ids:
        raise ValueError(
            f"Missing engine adapter ids: {sorted(missing_adapter_ids)}"
        )

    entries = (
        EngineObservabilityBindingEntry(
            observability_entry_id="engineobs_simulation_001",
            linked_backend_policy_id="backendpolicy_simulation_001",
            linked_engine_capability_id="enginecap_simulation_001",
            linked_engine_adapter_id="engineadapter_simulation_worker_001",
            selected_backend_slot="native_backend_slot",
            latency_path_class="bounded_realtime_path",
            fallback_active=False,
            mismatch_condition="none",
            selected_backend_metric_required=True,
            latency_metric_required=True,
            fallback_switch_metric_required=True,
            explainable_required=True,
            production_path_allowed=True,
            binding_status="defined",
            description="Engine observability binding for simulation engine.",
        ),
        EngineObservabilityBindingEntry(
            observability_entry_id="engineobs_optics_001",
            linked_backend_policy_id="backendpolicy_optics_001",
            linked_engine_capability_id="enginecap_optics_001",
            linked_engine_adapter_id="engineadapter_optics_worker_001",
            selected_backend_slot="gpu_backend_slot",
            latency_path_class="interactive_path",
            fallback_active=False,
            mismatch_condition="none",
            selected_backend_metric_required=True,
            latency_metric_required=True,
            fallback_switch_metric_required=True,
            explainable_required=True,
            production_path_allowed=True,
            binding_status="defined",
            description="Engine observability binding for optics engine.",
        ),
        EngineObservabilityBindingEntry(
            observability_entry_id="engineobs_display_transform_001",
            linked_backend_policy_id="backendpolicy_display_transform_001",
            linked_engine_capability_id="enginecap_display_transform_001",
            linked_engine_adapter_id="engineadapter_display_transform_001",
            selected_backend_slot="python_backend_slot",
            latency_path_class="fallback_interactive_path",
            fallback_active=True,
            mismatch_condition="fallback_active",
            selected_backend_metric_required=True,
            latency_metric_required=True,
            fallback_switch_metric_required=True,
            explainable_required=True,
            production_path_allowed=True,
            binding_status="defined",
            description="Engine observability binding for display transform engine.",
        ),
    )

    gpu_selected_entries = sum(
        1 for entry in entries if entry.selected_backend_slot == "gpu_backend_slot"
    )
    fallback_active_entries = sum(
        1 for entry in entries if entry.fallback_active
    )
    interactive_latency_entries = sum(
        1
        for entry in entries
        if entry.latency_path_class in ("interactive_path", "fallback_interactive_path")
    )
    defined_entries = sum(
        1 for entry in entries if entry.binding_status == "defined"
    )

    return EngineObservabilityBindingContract(
        total_entries=len(entries),
        gpu_selected_entries=gpu_selected_entries,
        fallback_active_entries=fallback_active_entries,
        interactive_latency_entries=interactive_latency_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
