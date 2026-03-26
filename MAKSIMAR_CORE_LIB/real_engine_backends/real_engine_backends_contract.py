from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.backend_selection_policy import (
    build_backend_selection_policy_contract,
)
from MAKSIMAR_CORE_LIB.engine_capability_contract import (
    build_engine_capability_contract,
)
from MAKSIMAR_CORE_LIB.engine_observability_binding import (
    build_engine_observability_binding_contract,
)


RealBackendEntryId = Literal[
    "realbackend_simulation_native_001",
    "realbackend_optics_gpu_001",
    "realbackend_display_python_001",
]

EngineCapabilityId = Literal[
    "enginecap_simulation_001",
    "enginecap_optics_001",
    "enginecap_display_transform_001",
]

BackendRuntimeKind = Literal[
    "native_runtime",
    "gpu_runtime",
    "python_runtime",
]

SelectedBackendSlot = Literal[
    "native_backend_slot",
    "gpu_backend_slot",
    "python_backend_slot",
]

BackendHealthClass = Literal[
    "healthy_runtime",
    "healthy_fallback_runtime",
]

BackendRuntimeStatus = Literal[
    "active",
]


_ENTRY_ID_PATTERN = re.compile(r"^realbackend_[a-z][a-z0-9_]*$")
_CAPABILITY_ID_PATTERN = re.compile(r"^enginecap_[a-z][a-z0-9_]*$")
_POLICY_ID_PATTERN = re.compile(r"^backendpolicy_[a-z][a-z0-9_]*$")
_OBS_ID_PATTERN = re.compile(r"^engineobs_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class RealEngineBackendEntry:
    """Canonical real engine backend runtime entry."""

    real_backend_entry_id: RealBackendEntryId
    linked_engine_capability_id: EngineCapabilityId
    linked_backend_policy_id: str
    linked_observability_entry_id: str
    backend_runtime_kind: BackendRuntimeKind
    selected_backend_slot: SelectedBackendSlot
    runtime_loaded: bool
    fallback_ready: bool
    backend_health_class: BackendHealthClass
    backend_runtime_status: BackendRuntimeStatus
    explainable_required: bool
    production_path_allowed: bool
    description: str

    def __post_init__(self) -> None:
        """Validate real backend runtime invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.real_backend_entry_id):
            raise ValueError(
                f"Invalid real_backend_entry_id: {self.real_backend_entry_id}"
            )

        if not _CAPABILITY_ID_PATTERN.fullmatch(self.linked_engine_capability_id):
            raise ValueError(
                f"Invalid linked_engine_capability_id: {self.linked_engine_capability_id}"
            )

        if not _POLICY_ID_PATTERN.fullmatch(self.linked_backend_policy_id):
            raise ValueError(
                f"Invalid linked_backend_policy_id: {self.linked_backend_policy_id}"
            )

        if not _OBS_ID_PATTERN.fullmatch(self.linked_observability_entry_id):
            raise ValueError(
                f"Invalid linked_observability_entry_id: {self.linked_observability_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.real_backend_entry_id}"
            )

        if not self.runtime_loaded:
            raise ValueError(
                f"runtime_loaded must be True: {self.real_backend_entry_id}"
            )

        if not self.fallback_ready:
            raise ValueError(
                f"fallback_ready must be True: {self.real_backend_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.real_backend_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.real_backend_entry_id}"
            )

        if self.backend_runtime_status != "active":
            raise ValueError(
                f"backend_runtime_status must be active: {self.real_backend_entry_id}"
            )

        if self.real_backend_entry_id == "realbackend_simulation_native_001":
            if self.linked_engine_capability_id != "enginecap_simulation_001":
                raise ValueError(
                    "realbackend_simulation_native_001 must link enginecap_simulation_001"
                )
            if self.linked_backend_policy_id != "backendpolicy_simulation_001":
                raise ValueError(
                    "realbackend_simulation_native_001 must link backendpolicy_simulation_001"
                )
            if self.linked_observability_entry_id != "engineobs_simulation_001":
                raise ValueError(
                    "realbackend_simulation_native_001 must link engineobs_simulation_001"
                )
            if self.backend_runtime_kind != "native_runtime":
                raise ValueError(
                    "realbackend_simulation_native_001 must use native_runtime"
                )
            if self.selected_backend_slot != "native_backend_slot":
                raise ValueError(
                    "realbackend_simulation_native_001 must use native_backend_slot"
                )
            if self.backend_health_class != "healthy_runtime":
                raise ValueError(
                    "realbackend_simulation_native_001 must use healthy_runtime"
                )

        if self.real_backend_entry_id == "realbackend_optics_gpu_001":
            if self.linked_engine_capability_id != "enginecap_optics_001":
                raise ValueError(
                    "realbackend_optics_gpu_001 must link enginecap_optics_001"
                )
            if self.linked_backend_policy_id != "backendpolicy_optics_001":
                raise ValueError(
                    "realbackend_optics_gpu_001 must link backendpolicy_optics_001"
                )
            if self.linked_observability_entry_id != "engineobs_optics_001":
                raise ValueError(
                    "realbackend_optics_gpu_001 must link engineobs_optics_001"
                )
            if self.backend_runtime_kind != "gpu_runtime":
                raise ValueError(
                    "realbackend_optics_gpu_001 must use gpu_runtime"
                )
            if self.selected_backend_slot != "gpu_backend_slot":
                raise ValueError(
                    "realbackend_optics_gpu_001 must use gpu_backend_slot"
                )
            if self.backend_health_class != "healthy_runtime":
                raise ValueError(
                    "realbackend_optics_gpu_001 must use healthy_runtime"
                )

        if self.real_backend_entry_id == "realbackend_display_python_001":
            if self.linked_engine_capability_id != "enginecap_display_transform_001":
                raise ValueError(
                    "realbackend_display_python_001 must link enginecap_display_transform_001"
                )
            if self.linked_backend_policy_id != "backendpolicy_display_transform_001":
                raise ValueError(
                    "realbackend_display_python_001 must link backendpolicy_display_transform_001"
                )
            if self.linked_observability_entry_id != "engineobs_display_transform_001":
                raise ValueError(
                    "realbackend_display_python_001 must link engineobs_display_transform_001"
                )
            if self.backend_runtime_kind != "python_runtime":
                raise ValueError(
                    "realbackend_display_python_001 must use python_runtime"
                )
            if self.selected_backend_slot != "python_backend_slot":
                raise ValueError(
                    "realbackend_display_python_001 must use python_backend_slot"
                )
            if self.backend_health_class != "healthy_fallback_runtime":
                raise ValueError(
                    "realbackend_display_python_001 must use healthy_fallback_runtime"
                )


@dataclass(frozen=True, slots=True)
class RealEngineBackendsContract:
    """Unified real engine backends contract."""

    total_entries: int
    native_runtime_entries: int
    gpu_runtime_entries: int
    fallback_class_entries: int
    active_entries: int
    entries: tuple[RealEngineBackendEntry, ...]

    def __post_init__(self) -> None:
        """Validate real engine backends contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        native_runtime_entries = sum(
            1 for entry in self.entries if entry.backend_runtime_kind == "native_runtime"
        )
        gpu_runtime_entries = sum(
            1 for entry in self.entries if entry.backend_runtime_kind == "gpu_runtime"
        )
        fallback_class_entries = sum(
            1 for entry in self.entries if entry.backend_health_class == "healthy_fallback_runtime"
        )
        active_entries = sum(
            1 for entry in self.entries if entry.backend_runtime_status == "active"
        )

        if self.native_runtime_entries != native_runtime_entries:
            raise ValueError("native_runtime_entries must match computed count")

        if self.gpu_runtime_entries != gpu_runtime_entries:
            raise ValueError("gpu_runtime_entries must match computed count")

        if self.fallback_class_entries != fallback_class_entries:
            raise ValueError("fallback_class_entries must match computed count")

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        entry_ids = tuple(entry.real_backend_entry_id for entry in self.entries)
        capability_ids = tuple(entry.linked_engine_capability_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate real_backend_entry_id values detected")

        if len(set(capability_ids)) != len(capability_ids):
            raise ValueError("Duplicate linked_engine_capability_id values detected")


def build_real_engine_backends_contract() -> RealEngineBackendsContract:
    """Build canonical real engine backends contract."""
    capability_contract = build_engine_capability_contract()
    policy_contract = build_backend_selection_policy_contract()
    observability_contract = build_engine_observability_binding_contract()

    capability_ids = {entry.engine_capability_id for entry in capability_contract.entries}
    policy_ids = {entry.backend_policy_id for entry in policy_contract.entries}
    observability_ids = {entry.observability_entry_id for entry in observability_contract.entries}

    required_capability_ids = {
        "enginecap_simulation_001",
        "enginecap_optics_001",
        "enginecap_display_transform_001",
    }
    required_policy_ids = {
        "backendpolicy_simulation_001",
        "backendpolicy_optics_001",
        "backendpolicy_display_transform_001",
    }
    required_observability_ids = {
        "engineobs_simulation_001",
        "engineobs_optics_001",
        "engineobs_display_transform_001",
    }

    missing_capability_ids = required_capability_ids - capability_ids
    if missing_capability_ids:
        raise ValueError(
            f"Missing engine capability ids: {sorted(missing_capability_ids)}"
        )

    missing_policy_ids = required_policy_ids - policy_ids
    if missing_policy_ids:
        raise ValueError(
            f"Missing backend policy ids: {sorted(missing_policy_ids)}"
        )

    missing_observability_ids = required_observability_ids - observability_ids
    if missing_observability_ids:
        raise ValueError(
            f"Missing observability ids: {sorted(missing_observability_ids)}"
        )

    entries = (
        RealEngineBackendEntry(
            real_backend_entry_id="realbackend_simulation_native_001",
            linked_engine_capability_id="enginecap_simulation_001",
            linked_backend_policy_id="backendpolicy_simulation_001",
            linked_observability_entry_id="engineobs_simulation_001",
            backend_runtime_kind="native_runtime",
            selected_backend_slot="native_backend_slot",
            runtime_loaded=True,
            fallback_ready=True,
            backend_health_class="healthy_runtime",
            backend_runtime_status="active",
            explainable_required=True,
            production_path_allowed=True,
            description="Canonical real backend runtime for simulation engine.",
        ),
        RealEngineBackendEntry(
            real_backend_entry_id="realbackend_optics_gpu_001",
            linked_engine_capability_id="enginecap_optics_001",
            linked_backend_policy_id="backendpolicy_optics_001",
            linked_observability_entry_id="engineobs_optics_001",
            backend_runtime_kind="gpu_runtime",
            selected_backend_slot="gpu_backend_slot",
            runtime_loaded=True,
            fallback_ready=True,
            backend_health_class="healthy_runtime",
            backend_runtime_status="active",
            explainable_required=True,
            production_path_allowed=True,
            description="Canonical real backend runtime for optics engine.",
        ),
        RealEngineBackendEntry(
            real_backend_entry_id="realbackend_display_python_001",
            linked_engine_capability_id="enginecap_display_transform_001",
            linked_backend_policy_id="backendpolicy_display_transform_001",
            linked_observability_entry_id="engineobs_display_transform_001",
            backend_runtime_kind="python_runtime",
            selected_backend_slot="python_backend_slot",
            runtime_loaded=True,
            fallback_ready=True,
            backend_health_class="healthy_fallback_runtime",
            backend_runtime_status="active",
            explainable_required=True,
            production_path_allowed=True,
            description="Canonical real backend runtime for display transform engine.",
        ),
    )

    native_runtime_entries = sum(
        1 for entry in entries if entry.backend_runtime_kind == "native_runtime"
    )
    gpu_runtime_entries = sum(
        1 for entry in entries if entry.backend_runtime_kind == "gpu_runtime"
    )
    fallback_class_entries = sum(
        1 for entry in entries if entry.backend_health_class == "healthy_fallback_runtime"
    )
    active_entries = sum(
        1 for entry in entries if entry.backend_runtime_status == "active"
    )

    return RealEngineBackendsContract(
        total_entries=len(entries),
        native_runtime_entries=native_runtime_entries,
        gpu_runtime_entries=gpu_runtime_entries,
        fallback_class_entries=fallback_class_entries,
        active_entries=active_entries,
        entries=entries,
    )
