from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.engine_adapter_boundary import (
    build_engine_adapter_boundary_contract,
)


EngineCapabilityId = Literal[
    "enginecap_simulation_001",
    "enginecap_optics_001",
    "enginecap_display_transform_001",
]

EngineKind = Literal[
    "simulation_engine",
    "optics_engine",
    "display_transform_engine",
]

LanguageRuntime = Literal[
    "python",
    "native",
    "gpu",
    "hybrid",
]

SupportedWorkload = Literal[
    "simulation_workload",
    "optics_workload",
    "display_transform_workload",
]

LatencyProfile = Literal[
    "interactive",
    "bounded_realtime",
]

EngineCapabilityStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^enginecap_[a-z][a-z0-9_]*$")
_ADAPTER_ID_PATTERN = re.compile(r"^engineadapter_[a-z][a-z0-9_]*$")
_WORKLOAD_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _validate_unique_non_empty_str_tuple(
    *,
    values: tuple[str, ...],
    field_name: str,
    owner_id: str,
) -> None:
    """Validate tuple items are non-empty and unique."""
    if len(set(values)) != len(values):
        raise ValueError(f"Duplicate values in {field_name} for {owner_id}")
    for value in values:
        if not value.strip():
            raise ValueError(f"{field_name} contains empty value for {owner_id}")


@dataclass(frozen=True, slots=True)
class EngineCapabilityEntry:
    """Canonical engine capability contract entry."""

    engine_capability_id: EngineCapabilityId
    linked_engine_adapter_id: str
    engine_kind: EngineKind
    language_runtime: LanguageRuntime
    supported_workloads: tuple[SupportedWorkload, ...]
    latency_profile: LatencyProfile
    requires_gpu: bool
    requires_native_runtime: bool
    fallback_available: bool
    production_path_allowed: bool
    capability_status: EngineCapabilityStatus
    description: str

    def __post_init__(self) -> None:
        """Validate engine capability invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.engine_capability_id):
            raise ValueError(
                f"Invalid engine_capability_id: {self.engine_capability_id}"
            )

        if not _ADAPTER_ID_PATTERN.fullmatch(self.linked_engine_adapter_id):
            raise ValueError(
                f"Invalid linked_engine_adapter_id: {self.linked_engine_adapter_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.engine_capability_id}"
            )

        _validate_unique_non_empty_str_tuple(
            values=self.supported_workloads,
            field_name="supported_workloads",
            owner_id=self.engine_capability_id,
        )

        for workload in self.supported_workloads:
            if not _WORKLOAD_PATTERN.fullmatch(workload):
                raise ValueError(
                    f"Invalid workload '{workload}' for {self.engine_capability_id}"
                )

        if not self.fallback_available:
            raise ValueError(
                f"fallback_available must be True: {self.engine_capability_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.engine_capability_id}"
            )

        if self.capability_status != "defined":
            raise ValueError(
                f"capability_status must be defined: {self.engine_capability_id}"
            )

        if self.engine_capability_id == "enginecap_simulation_001":
            if self.linked_engine_adapter_id != "engineadapter_simulation_worker_001":
                raise ValueError(
                    "enginecap_simulation_001 must link engineadapter_simulation_worker_001"
                )
            if self.engine_kind != "simulation_engine":
                raise ValueError(
                    "enginecap_simulation_001 must use simulation_engine"
                )
            if self.language_runtime != "hybrid":
                raise ValueError(
                    "enginecap_simulation_001 must use hybrid runtime"
                )
            if self.supported_workloads != ("simulation_workload",):
                raise ValueError(
                    "enginecap_simulation_001 must expose simulation_workload only"
                )
            if self.latency_profile != "bounded_realtime":
                raise ValueError(
                    "enginecap_simulation_001 must use bounded_realtime"
                )
            if self.requires_gpu:
                raise ValueError(
                    "enginecap_simulation_001 must not require_gpu canonically"
                )
            if self.requires_native_runtime:
                raise ValueError(
                    "enginecap_simulation_001 must not require_native_runtime canonically"
                )

        if self.engine_capability_id == "enginecap_optics_001":
            if self.linked_engine_adapter_id != "engineadapter_optics_worker_001":
                raise ValueError(
                    "enginecap_optics_001 must link engineadapter_optics_worker_001"
                )
            if self.engine_kind != "optics_engine":
                raise ValueError(
                    "enginecap_optics_001 must use optics_engine"
                )
            if self.language_runtime != "hybrid":
                raise ValueError(
                    "enginecap_optics_001 must use hybrid runtime"
                )
            if self.supported_workloads != ("optics_workload",):
                raise ValueError(
                    "enginecap_optics_001 must expose optics_workload only"
                )
            if self.latency_profile != "interactive":
                raise ValueError(
                    "enginecap_optics_001 must use interactive latency"
                )
            if self.requires_gpu:
                raise ValueError(
                    "enginecap_optics_001 must not require_gpu canonically"
                )
            if self.requires_native_runtime:
                raise ValueError(
                    "enginecap_optics_001 must not require_native_runtime canonically"
                )

        if self.engine_capability_id == "enginecap_display_transform_001":
            if self.linked_engine_adapter_id != "engineadapter_display_transform_001":
                raise ValueError(
                    "enginecap_display_transform_001 must link engineadapter_display_transform_001"
                )
            if self.engine_kind != "display_transform_engine":
                raise ValueError(
                    "enginecap_display_transform_001 must use display_transform_engine"
                )
            if self.language_runtime != "python":
                raise ValueError(
                    "enginecap_display_transform_001 must use python runtime"
                )
            if self.supported_workloads != ("display_transform_workload",):
                raise ValueError(
                    "enginecap_display_transform_001 must expose display_transform_workload only"
                )
            if self.latency_profile != "interactive":
                raise ValueError(
                    "enginecap_display_transform_001 must use interactive latency"
                )
            if self.requires_gpu:
                raise ValueError(
                    "enginecap_display_transform_001 must not require_gpu"
                )
            if self.requires_native_runtime:
                raise ValueError(
                    "enginecap_display_transform_001 must not require_native_runtime"
                )


@dataclass(frozen=True, slots=True)
class EngineCapabilityContract:
    """Unified engine capability contract."""

    total_entries: int
    hybrid_runtime_entries: int
    interactive_latency_entries: int
    fallback_available_entries: int
    defined_entries: int
    entries: tuple[EngineCapabilityEntry, ...]

    def __post_init__(self) -> None:
        """Validate engine capability contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        hybrid_runtime_entries = sum(
            1 for entry in self.entries if entry.language_runtime == "hybrid"
        )
        interactive_latency_entries = sum(
            1 for entry in self.entries if entry.latency_profile == "interactive"
        )
        fallback_available_entries = sum(
            1 for entry in self.entries if entry.fallback_available
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.capability_status == "defined"
        )

        if self.hybrid_runtime_entries != hybrid_runtime_entries:
            raise ValueError("hybrid_runtime_entries must match computed count")

        if self.interactive_latency_entries != interactive_latency_entries:
            raise ValueError(
                "interactive_latency_entries must match computed count"
            )

        if self.fallback_available_entries != fallback_available_entries:
            raise ValueError(
                "fallback_available_entries must match computed count"
            )

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.engine_capability_id for entry in self.entries)
        kinds = tuple(entry.engine_kind for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate engine_capability_id values detected")

        if len(set(kinds)) != len(kinds):
            raise ValueError("Duplicate engine_kind values detected")


def build_engine_capability_contract() -> EngineCapabilityContract:
    """Build canonical engine capability contract."""
    boundary_contract = build_engine_adapter_boundary_contract()
    adapter_ids = {entry.engine_adapter_id for entry in boundary_contract.entries}

    required_adapter_ids = {
        "engineadapter_simulation_worker_001",
        "engineadapter_optics_worker_001",
        "engineadapter_display_transform_001",
    }
    missing_adapter_ids = required_adapter_ids - adapter_ids
    if missing_adapter_ids:
        raise ValueError(
            f"Missing engine adapter ids: {sorted(missing_adapter_ids)}"
        )

    entries = (
        EngineCapabilityEntry(
            engine_capability_id="enginecap_simulation_001",
            linked_engine_adapter_id="engineadapter_simulation_worker_001",
            engine_kind="simulation_engine",
            language_runtime="hybrid",
            supported_workloads=("simulation_workload",),
            latency_profile="bounded_realtime",
            requires_gpu=False,
            requires_native_runtime=False,
            fallback_available=True,
            production_path_allowed=True,
            capability_status="defined",
            description="Canonical engine capability for simulation engine.",
        ),
        EngineCapabilityEntry(
            engine_capability_id="enginecap_optics_001",
            linked_engine_adapter_id="engineadapter_optics_worker_001",
            engine_kind="optics_engine",
            language_runtime="hybrid",
            supported_workloads=("optics_workload",),
            latency_profile="interactive",
            requires_gpu=False,
            requires_native_runtime=False,
            fallback_available=True,
            production_path_allowed=True,
            capability_status="defined",
            description="Canonical engine capability for optics engine.",
        ),
        EngineCapabilityEntry(
            engine_capability_id="enginecap_display_transform_001",
            linked_engine_adapter_id="engineadapter_display_transform_001",
            engine_kind="display_transform_engine",
            language_runtime="python",
            supported_workloads=("display_transform_workload",),
            latency_profile="interactive",
            requires_gpu=False,
            requires_native_runtime=False,
            fallback_available=True,
            production_path_allowed=True,
            capability_status="defined",
            description="Canonical engine capability for display transform engine.",
        ),
    )

    hybrid_runtime_entries = sum(
        1 for entry in entries if entry.language_runtime == "hybrid"
    )
    interactive_latency_entries = sum(
        1 for entry in entries if entry.latency_profile == "interactive"
    )
    fallback_available_entries = sum(
        1 for entry in entries if entry.fallback_available
    )
    defined_entries = sum(
        1 for entry in entries if entry.capability_status == "defined"
    )

    return EngineCapabilityContract(
        total_entries=len(entries),
        hybrid_runtime_entries=hybrid_runtime_entries,
        interactive_latency_entries=interactive_latency_entries,
        fallback_available_entries=fallback_available_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
