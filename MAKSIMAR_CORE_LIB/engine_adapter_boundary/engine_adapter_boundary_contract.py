from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.optics_light_field_engine import (
    build_optics_light_field_engine_contract,
)
from MAKSIMAR_CORE_LIB.physics_simulation_mode import (
    build_physics_simulation_mode_contract,
)
from MAKSIMAR_CORE_LIB.wrist_psc_display_integration import (
    build_wrist_psc_display_integration_contract,
)


EngineAdapterId = Literal[
    "engineadapter_simulation_worker_001",
    "engineadapter_optics_worker_001",
    "engineadapter_display_transform_001",
]

WorkerKind = Literal[
    "simulation_worker",
    "optics_worker",
    "display_transform_runtime",
]

EngineBoundaryMode = Literal[
    "adapter_required",
]

ContractShape = Literal[
    "engine_neutral",
]

BackendSlot = Literal[
    "python_backend_slot",
    "native_backend_slot",
    "gpu_backend_slot",
    "fallback_backend_slot",
]

BoundaryStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^engineadapter_[a-z][a-z0-9_]*$")
_ENGINE_ID_PATTERN = re.compile(r"^opticsengine_[a-z][a-z0-9_]*$")
_INTEGRATION_ID_PATTERN = re.compile(r"^wristdisplayint_[a-z][a-z0-9_]*$")


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
class EngineAdapterBoundaryEntry:
    """Canonical engine adapter boundary entry."""

    engine_adapter_id: EngineAdapterId
    worker_kind: WorkerKind
    boundary_mode: EngineBoundaryMode
    contract_shape: ContractShape
    backend_slots: tuple[BackendSlot, ...]
    linked_optics_engine_id: str | None
    linked_integration_entry_id: str | None
    adapter_required: bool
    backend_specific_contracts_forbidden: bool
    direct_worker_to_backend_binding_forbidden: bool
    fallback_required: bool
    production_path_allowed: bool
    boundary_status: BoundaryStatus
    description: str

    def __post_init__(self) -> None:
        """Validate engine adapter boundary invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.engine_adapter_id):
            raise ValueError(f"Invalid engine_adapter_id: {self.engine_adapter_id}")

        if self.linked_optics_engine_id is not None:
            if not _ENGINE_ID_PATTERN.fullmatch(self.linked_optics_engine_id):
                raise ValueError(
                    f"Invalid linked_optics_engine_id: {self.linked_optics_engine_id}"
                )

        if self.linked_integration_entry_id is not None:
            if not _INTEGRATION_ID_PATTERN.fullmatch(
                self.linked_integration_entry_id
            ):
                raise ValueError(
                    f"Invalid linked_integration_entry_id: {self.linked_integration_entry_id}"
                )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.engine_adapter_id}"
            )

        _validate_unique_non_empty_str_tuple(
            values=self.backend_slots,
            field_name="backend_slots",
            owner_id=self.engine_adapter_id,
        )

        expected_slots = (
            "python_backend_slot",
            "native_backend_slot",
            "gpu_backend_slot",
            "fallback_backend_slot",
        )
        if self.backend_slots != expected_slots:
            raise ValueError(
                f"backend_slots must preserve canonical order for {self.engine_adapter_id}"
            )

        if self.boundary_mode != "adapter_required":
            raise ValueError(
                f"boundary_mode must be adapter_required: {self.engine_adapter_id}"
            )

        if self.contract_shape != "engine_neutral":
            raise ValueError(
                f"contract_shape must be engine_neutral: {self.engine_adapter_id}"
            )

        if not self.adapter_required:
            raise ValueError(
                f"adapter_required must be True: {self.engine_adapter_id}"
            )

        if not self.backend_specific_contracts_forbidden:
            raise ValueError(
                f"backend_specific_contracts_forbidden must be True: {self.engine_adapter_id}"
            )

        if not self.direct_worker_to_backend_binding_forbidden:
            raise ValueError(
                f"direct_worker_to_backend_binding_forbidden must be True: {self.engine_adapter_id}"
            )

        if not self.fallback_required:
            raise ValueError(
                f"fallback_required must be True: {self.engine_adapter_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.engine_adapter_id}"
            )

        if self.boundary_status != "defined":
            raise ValueError(
                f"boundary_status must be defined: {self.engine_adapter_id}"
            )

        if self.engine_adapter_id == "engineadapter_simulation_worker_001":
            if self.worker_kind != "simulation_worker":
                raise ValueError(
                    "engineadapter_simulation_worker_001 must use simulation_worker"
                )
            if self.linked_optics_engine_id is not None:
                raise ValueError(
                    "engineadapter_simulation_worker_001 must not link optics engine directly"
                )
            if self.linked_integration_entry_id is not None:
                raise ValueError(
                    "engineadapter_simulation_worker_001 must not link integration entry directly"
                )

        if self.engine_adapter_id == "engineadapter_optics_worker_001":
            if self.worker_kind != "optics_worker":
                raise ValueError(
                    "engineadapter_optics_worker_001 must use optics_worker"
                )
            if self.linked_optics_engine_id != "opticsengine_ar_glasses_projection_001":
                raise ValueError(
                    "engineadapter_optics_worker_001 must link opticsengine_ar_glasses_projection_001"
                )

        if self.engine_adapter_id == "engineadapter_display_transform_001":
            if self.worker_kind != "display_transform_runtime":
                raise ValueError(
                    "engineadapter_display_transform_001 must use display_transform_runtime"
                )
            if self.linked_integration_entry_id != "wristdisplayint_ar_001":
                raise ValueError(
                    "engineadapter_display_transform_001 must link wristdisplayint_ar_001"
                )


@dataclass(frozen=True, slots=True)
class EngineAdapterBoundaryContract:
    """Unified engine adapter boundary contract."""

    total_entries: int
    optics_linked_entries: int
    integration_linked_entries: int
    fallback_required_entries: int
    defined_entries: int
    entries: tuple[EngineAdapterBoundaryEntry, ...]

    def __post_init__(self) -> None:
        """Validate engine adapter boundary contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        optics_linked_entries = sum(
            1 for entry in self.entries if entry.linked_optics_engine_id is not None
        )
        integration_linked_entries = sum(
            1
            for entry in self.entries
            if entry.linked_integration_entry_id is not None
        )
        fallback_required_entries = sum(
            1 for entry in self.entries if entry.fallback_required
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.boundary_status == "defined"
        )

        if self.optics_linked_entries != optics_linked_entries:
            raise ValueError("optics_linked_entries must match computed count")

        if self.integration_linked_entries != integration_linked_entries:
            raise ValueError("integration_linked_entries must match computed count")

        if self.fallback_required_entries != fallback_required_entries:
            raise ValueError("fallback_required_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.engine_adapter_id for entry in self.entries)
        worker_kinds = tuple(entry.worker_kind for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate engine_adapter_id values detected")

        if len(set(worker_kinds)) != len(worker_kinds):
            raise ValueError("Duplicate worker_kind values detected")


def build_engine_adapter_boundary_contract() -> EngineAdapterBoundaryContract:
    """Build canonical engine adapter boundary contract."""
    simulation_modes = build_physics_simulation_mode_contract()
    optics_contract = build_optics_light_field_engine_contract()
    integration_contract = build_wrist_psc_display_integration_contract()

    mode_names = {entry.simulation_mode for entry in simulation_modes.entries}
    optics_ids = {entry.engine_entry_id for entry in optics_contract.entries}
    integration_ids = {
        entry.integration_entry_id for entry in integration_contract.entries
    }

    required_modes = {
        "strict_physics",
        "engineering_realistic",
        "research_relaxed",
        "control_learning",
    }
    missing_modes = required_modes - mode_names
    if missing_modes:
        raise ValueError(f"Missing simulation modes: {sorted(missing_modes)}")

    if "opticsengine_ar_glasses_projection_001" not in optics_ids:
        raise ValueError(
            "Expected opticsengine_ar_glasses_projection_001 in optics engine contract"
        )

    if "wristdisplayint_ar_001" not in integration_ids:
        raise ValueError(
            "Expected wristdisplayint_ar_001 in wrist/display integration contract"
        )

    canonical_slots = (
        "python_backend_slot",
        "native_backend_slot",
        "gpu_backend_slot",
        "fallback_backend_slot",
    )

    entries = (
        EngineAdapterBoundaryEntry(
            engine_adapter_id="engineadapter_simulation_worker_001",
            worker_kind="simulation_worker",
            boundary_mode="adapter_required",
            contract_shape="engine_neutral",
            backend_slots=canonical_slots,
            linked_optics_engine_id=None,
            linked_integration_entry_id=None,
            adapter_required=True,
            backend_specific_contracts_forbidden=True,
            direct_worker_to_backend_binding_forbidden=True,
            fallback_required=True,
            production_path_allowed=True,
            boundary_status="defined",
            description="Engine adapter boundary for simulation worker runtime.",
        ),
        EngineAdapterBoundaryEntry(
            engine_adapter_id="engineadapter_optics_worker_001",
            worker_kind="optics_worker",
            boundary_mode="adapter_required",
            contract_shape="engine_neutral",
            backend_slots=canonical_slots,
            linked_optics_engine_id="opticsengine_ar_glasses_projection_001",
            linked_integration_entry_id=None,
            adapter_required=True,
            backend_specific_contracts_forbidden=True,
            direct_worker_to_backend_binding_forbidden=True,
            fallback_required=True,
            production_path_allowed=True,
            boundary_status="defined",
            description="Engine adapter boundary for optics worker runtime.",
        ),
        EngineAdapterBoundaryEntry(
            engine_adapter_id="engineadapter_display_transform_001",
            worker_kind="display_transform_runtime",
            boundary_mode="adapter_required",
            contract_shape="engine_neutral",
            backend_slots=canonical_slots,
            linked_optics_engine_id=None,
            linked_integration_entry_id="wristdisplayint_ar_001",
            adapter_required=True,
            backend_specific_contracts_forbidden=True,
            direct_worker_to_backend_binding_forbidden=True,
            fallback_required=True,
            production_path_allowed=True,
            boundary_status="defined",
            description="Engine adapter boundary for display transform runtime.",
        ),
    )

    optics_linked_entries = sum(
        1 for entry in entries if entry.linked_optics_engine_id is not None
    )
    integration_linked_entries = sum(
        1 for entry in entries if entry.linked_integration_entry_id is not None
    )
    fallback_required_entries = sum(
        1 for entry in entries if entry.fallback_required
    )
    defined_entries = sum(
        1 for entry in entries if entry.boundary_status == "defined"
    )

    return EngineAdapterBoundaryContract(
        total_entries=len(entries),
        optics_linked_entries=optics_linked_entries,
        integration_linked_entries=integration_linked_entries,
        fallback_required_entries=fallback_required_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
