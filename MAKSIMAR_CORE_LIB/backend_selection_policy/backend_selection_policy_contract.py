from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.engine_capability_contract import (
    build_engine_capability_contract,
)


BackendPolicyId = Literal[
    "backendpolicy_simulation_001",
    "backendpolicy_optics_001",
    "backendpolicy_display_transform_001",
]

BackendSelectionMode = Literal[
    "policy_selected",
]

SelectedBackendSlot = Literal[
    "python_backend_slot",
    "native_backend_slot",
    "gpu_backend_slot",
    "fallback_backend_slot",
]

LatencySensitivity = Literal[
    "interactive",
    "bounded_realtime",
]

DegradedMode = Literal[
    "normal_path",
    "fallback_path",
]

BackendPolicyStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^backendpolicy_[a-z][a-z0-9_]*$")
_ENGINE_CAP_ID_PATTERN = re.compile(r"^enginecap_[a-z][a-z0-9_]*$")
_SLOT_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class BackendSelectionPolicyEntry:
    """Canonical backend selection policy entry."""

    backend_policy_id: BackendPolicyId
    linked_engine_capability_id: str
    selection_mode: BackendSelectionMode
    selected_backend_slot: SelectedBackendSlot
    latency_sensitivity: LatencySensitivity
    degraded_mode: DegradedMode
    fallback_available: bool
    gpu_preferred_when_available: bool
    native_preferred_when_available: bool
    production_path_allowed: bool
    policy_status: BackendPolicyStatus
    description: str

    def __post_init__(self) -> None:
        """Validate backend selection policy invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.backend_policy_id):
            raise ValueError(f"Invalid backend_policy_id: {self.backend_policy_id}")

        if not _ENGINE_CAP_ID_PATTERN.fullmatch(self.linked_engine_capability_id):
            raise ValueError(
                f"Invalid linked_engine_capability_id: {self.linked_engine_capability_id}"
            )

        if not _SLOT_PATTERN.fullmatch(self.selected_backend_slot):
            raise ValueError(
                f"Invalid selected_backend_slot: {self.selected_backend_slot}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.backend_policy_id}"
            )

        if self.selection_mode != "policy_selected":
            raise ValueError(
                f"selection_mode must be policy_selected: {self.backend_policy_id}"
            )

        if not self.fallback_available:
            raise ValueError(
                f"fallback_available must be True: {self.backend_policy_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.backend_policy_id}"
            )

        if self.policy_status != "defined":
            raise ValueError(
                f"policy_status must be defined: {self.backend_policy_id}"
            )

        if self.backend_policy_id == "backendpolicy_simulation_001":
            if self.linked_engine_capability_id != "enginecap_simulation_001":
                raise ValueError(
                    "backendpolicy_simulation_001 must link enginecap_simulation_001"
                )
            if self.selected_backend_slot != "native_backend_slot":
                raise ValueError(
                    "backendpolicy_simulation_001 must select native_backend_slot"
                )
            if self.latency_sensitivity != "bounded_realtime":
                raise ValueError(
                    "backendpolicy_simulation_001 must use bounded_realtime"
                )
            if self.degraded_mode != "normal_path":
                raise ValueError(
                    "backendpolicy_simulation_001 must use normal_path"
                )
            if self.gpu_preferred_when_available:
                raise ValueError(
                    "backendpolicy_simulation_001 must not prefer GPU canonically"
                )
            if not self.native_preferred_when_available:
                raise ValueError(
                    "backendpolicy_simulation_001 must prefer native when available"
                )

        if self.backend_policy_id == "backendpolicy_optics_001":
            if self.linked_engine_capability_id != "enginecap_optics_001":
                raise ValueError(
                    "backendpolicy_optics_001 must link enginecap_optics_001"
                )
            if self.selected_backend_slot != "gpu_backend_slot":
                raise ValueError(
                    "backendpolicy_optics_001 must select gpu_backend_slot"
                )
            if self.latency_sensitivity != "interactive":
                raise ValueError(
                    "backendpolicy_optics_001 must use interactive latency"
                )
            if self.degraded_mode != "normal_path":
                raise ValueError(
                    "backendpolicy_optics_001 must use normal_path"
                )
            if not self.gpu_preferred_when_available:
                raise ValueError(
                    "backendpolicy_optics_001 must prefer GPU when available"
                )
            if self.native_preferred_when_available:
                raise ValueError(
                    "backendpolicy_optics_001 must not prefer native canonically"
                )

        if self.backend_policy_id == "backendpolicy_display_transform_001":
            if self.linked_engine_capability_id != "enginecap_display_transform_001":
                raise ValueError(
                    "backendpolicy_display_transform_001 must link enginecap_display_transform_001"
                )
            if self.selected_backend_slot != "python_backend_slot":
                raise ValueError(
                    "backendpolicy_display_transform_001 must select python_backend_slot"
                )
            if self.latency_sensitivity != "interactive":
                raise ValueError(
                    "backendpolicy_display_transform_001 must use interactive latency"
                )
            if self.degraded_mode != "fallback_path":
                raise ValueError(
                    "backendpolicy_display_transform_001 must use fallback_path"
                )
            if self.gpu_preferred_when_available:
                raise ValueError(
                    "backendpolicy_display_transform_001 must not prefer GPU"
                )
            if self.native_preferred_when_available:
                raise ValueError(
                    "backendpolicy_display_transform_001 must not prefer native"
                )


@dataclass(frozen=True, slots=True)
class BackendSelectionPolicyContract:
    """Unified backend selection policy contract."""

    total_entries: int
    gpu_selected_entries: int
    native_selected_entries: int
    fallback_path_entries: int
    defined_entries: int
    entries: tuple[BackendSelectionPolicyEntry, ...]

    def __post_init__(self) -> None:
        """Validate backend selection policy contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        gpu_selected_entries = sum(
            1 for entry in self.entries if entry.selected_backend_slot == "gpu_backend_slot"
        )
        native_selected_entries = sum(
            1 for entry in self.entries if entry.selected_backend_slot == "native_backend_slot"
        )
        fallback_path_entries = sum(
            1 for entry in self.entries if entry.degraded_mode == "fallback_path"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.policy_status == "defined"
        )

        if self.gpu_selected_entries != gpu_selected_entries:
            raise ValueError("gpu_selected_entries must match computed count")

        if self.native_selected_entries != native_selected_entries:
            raise ValueError("native_selected_entries must match computed count")

        if self.fallback_path_entries != fallback_path_entries:
            raise ValueError("fallback_path_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.backend_policy_id for entry in self.entries)
        cap_ids = tuple(entry.linked_engine_capability_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate backend_policy_id values detected")

        if len(set(cap_ids)) != len(cap_ids):
            raise ValueError("Duplicate linked_engine_capability_id values detected")


def build_backend_selection_policy_contract() -> BackendSelectionPolicyContract:
    """Build canonical backend selection policy contract."""
    capability_contract = build_engine_capability_contract()
    capability_ids = {entry.engine_capability_id for entry in capability_contract.entries}

    required_capability_ids = {
        "enginecap_simulation_001",
        "enginecap_optics_001",
        "enginecap_display_transform_001",
    }
    missing_capability_ids = required_capability_ids - capability_ids
    if missing_capability_ids:
        raise ValueError(
            f"Missing engine capability ids: {sorted(missing_capability_ids)}"
        )

    entries = (
        BackendSelectionPolicyEntry(
            backend_policy_id="backendpolicy_simulation_001",
            linked_engine_capability_id="enginecap_simulation_001",
            selection_mode="policy_selected",
            selected_backend_slot="native_backend_slot",
            latency_sensitivity="bounded_realtime",
            degraded_mode="normal_path",
            fallback_available=True,
            gpu_preferred_when_available=False,
            native_preferred_when_available=True,
            production_path_allowed=True,
            policy_status="defined",
            description="Canonical backend selection policy for simulation engine.",
        ),
        BackendSelectionPolicyEntry(
            backend_policy_id="backendpolicy_optics_001",
            linked_engine_capability_id="enginecap_optics_001",
            selection_mode="policy_selected",
            selected_backend_slot="gpu_backend_slot",
            latency_sensitivity="interactive",
            degraded_mode="normal_path",
            fallback_available=True,
            gpu_preferred_when_available=True,
            native_preferred_when_available=False,
            production_path_allowed=True,
            policy_status="defined",
            description="Canonical backend selection policy for optics engine.",
        ),
        BackendSelectionPolicyEntry(
            backend_policy_id="backendpolicy_display_transform_001",
            linked_engine_capability_id="enginecap_display_transform_001",
            selection_mode="policy_selected",
            selected_backend_slot="python_backend_slot",
            latency_sensitivity="interactive",
            degraded_mode="fallback_path",
            fallback_available=True,
            gpu_preferred_when_available=False,
            native_preferred_when_available=False,
            production_path_allowed=True,
            policy_status="defined",
            description="Canonical backend selection policy for display transform runtime.",
        ),
    )

    gpu_selected_entries = sum(
        1 for entry in entries if entry.selected_backend_slot == "gpu_backend_slot"
    )
    native_selected_entries = sum(
        1 for entry in entries if entry.selected_backend_slot == "native_backend_slot"
    )
    fallback_path_entries = sum(
        1 for entry in entries if entry.degraded_mode == "fallback_path"
    )
    defined_entries = sum(
        1 for entry in entries if entry.policy_status == "defined"
    )

    return BackendSelectionPolicyContract(
        total_entries=len(entries),
        gpu_selected_entries=gpu_selected_entries,
        native_selected_entries=native_selected_entries,
        fallback_path_entries=fallback_path_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
