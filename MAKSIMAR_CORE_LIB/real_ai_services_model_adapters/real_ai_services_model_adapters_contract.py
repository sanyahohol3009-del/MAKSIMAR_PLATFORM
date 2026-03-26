from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.end_to_end_orchestration_runtime import (
    build_end_to_end_orchestration_runtime_contract,
)
from MAKSIMAR_CORE_LIB.engine_adapter_boundary import (
    build_engine_adapter_boundary_contract,
)
from MAKSIMAR_CORE_LIB.engine_capability_contract import (
    build_engine_capability_contract,
)
from MAKSIMAR_CORE_LIB.real_engine_backends import (
    build_real_engine_backends_contract,
)
from MAKSIMAR_CORE_LIB.real_voice_runtime import (
    build_real_voice_runtime_contract,
)


RealAiServiceEntryId = Literal[
    "aiservice_reasoning_001",
    "aiservice_coding_001",
    "aiservice_visual_001",
]

ServiceKind = Literal[
    "reasoning_service",
    "coding_service",
    "visual_service",
]

ModelAdapterKind = Literal[
    "glm_adapter",
    "qwen_adapter",
    "deepseek_adapter",
]

AdapterBoundaryMode = Literal[
    "service_via_adapter",
]

ServiceRuntimeStatus = Literal[
    "active",
]


_ENTRY_ID_PATTERN = re.compile(r"^aiservice_[a-z][a-z0-9_]*$")
_ADAPTER_ID_PATTERN = re.compile(r"^engineadapter_[a-z][a-z0-9_]*$")
_CAPABILITY_ID_PATTERN = re.compile(r"^enginecap_[a-z][a-z0-9_]*$")
_BACKEND_ID_PATTERN = re.compile(r"^realbackend_[a-z][a-z0-9_]*$")
_ORCH_ID_PATTERN = re.compile(r"^orchestration_[a-z][a-z0-9_]*$")
_VOICE_ID_PATTERN = re.compile(r"^realvoice_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class RealAiServicesModelAdaptersEntry:
    """Canonical real AI services / model adapters entry."""

    real_ai_service_entry_id: RealAiServiceEntryId
    service_kind: ServiceKind
    model_adapter_kind: ModelAdapterKind
    linked_engine_adapter_id: str
    linked_engine_capability_id: str
    linked_real_backend_id: str
    linked_orchestration_entry_id: str
    linked_voice_runtime_entry_id: str
    adapter_boundary_mode: AdapterBoundaryMode
    network_free_direct_core_access: bool
    sandbox_required: bool
    explainable_required: bool
    production_path_allowed: bool
    service_runtime_status: ServiceRuntimeStatus
    description: str

    def __post_init__(self) -> None:
        """Validate real AI services / model adapters invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.real_ai_service_entry_id):
            raise ValueError(
                f"Invalid real_ai_service_entry_id: {self.real_ai_service_entry_id}"
            )

        if not _ADAPTER_ID_PATTERN.fullmatch(self.linked_engine_adapter_id):
            raise ValueError(
                f"Invalid linked_engine_adapter_id: {self.linked_engine_adapter_id}"
            )

        if not _CAPABILITY_ID_PATTERN.fullmatch(self.linked_engine_capability_id):
            raise ValueError(
                f"Invalid linked_engine_capability_id: {self.linked_engine_capability_id}"
            )

        if not _BACKEND_ID_PATTERN.fullmatch(self.linked_real_backend_id):
            raise ValueError(
                f"Invalid linked_real_backend_id: {self.linked_real_backend_id}"
            )

        if not _ORCH_ID_PATTERN.fullmatch(self.linked_orchestration_entry_id):
            raise ValueError(
                f"Invalid linked_orchestration_entry_id: {self.linked_orchestration_entry_id}"
            )

        if not _VOICE_ID_PATTERN.fullmatch(self.linked_voice_runtime_entry_id):
            raise ValueError(
                f"Invalid linked_voice_runtime_entry_id: {self.linked_voice_runtime_entry_id}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.real_ai_service_entry_id}"
            )

        if self.adapter_boundary_mode != "service_via_adapter":
            raise ValueError(
                f"adapter_boundary_mode must be service_via_adapter: {self.real_ai_service_entry_id}"
            )

        if self.network_free_direct_core_access:
            raise ValueError(
                f"network_free_direct_core_access must be False: {self.real_ai_service_entry_id}"
            )

        if not self.sandbox_required:
            raise ValueError(
                f"sandbox_required must be True: {self.real_ai_service_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.real_ai_service_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.real_ai_service_entry_id}"
            )

        if self.service_runtime_status != "active":
            raise ValueError(
                f"service_runtime_status must be active: {self.real_ai_service_entry_id}"
            )

        if self.real_ai_service_entry_id == "aiservice_reasoning_001":
            if self.service_kind != "reasoning_service":
                raise ValueError("aiservice_reasoning_001 must use reasoning_service")
            if self.model_adapter_kind != "glm_adapter":
                raise ValueError("aiservice_reasoning_001 must use glm_adapter")
            if self.linked_engine_adapter_id != "engineadapter_simulation_worker_001":
                raise ValueError(
                    "aiservice_reasoning_001 must link engineadapter_simulation_worker_001"
                )
            if self.linked_engine_capability_id != "enginecap_simulation_001":
                raise ValueError(
                    "aiservice_reasoning_001 must link enginecap_simulation_001"
                )
            if self.linked_real_backend_id != "realbackend_simulation_native_001":
                raise ValueError(
                    "aiservice_reasoning_001 must link realbackend_simulation_native_001"
                )
            if self.linked_orchestration_entry_id != "orchestration_heavy_execution_001":
                raise ValueError(
                    "aiservice_reasoning_001 must link orchestration_heavy_execution_001"
                )
            if self.linked_voice_runtime_entry_id != "realvoice_show_simulation_001":
                raise ValueError(
                    "aiservice_reasoning_001 must link realvoice_show_simulation_001"
                )

        if self.real_ai_service_entry_id == "aiservice_coding_001":
            if self.service_kind != "coding_service":
                raise ValueError("aiservice_coding_001 must use coding_service")
            if self.model_adapter_kind != "qwen_adapter":
                raise ValueError("aiservice_coding_001 must use qwen_adapter")
            if self.linked_engine_adapter_id != "engineadapter_display_transform_001":
                raise ValueError(
                    "aiservice_coding_001 must link engineadapter_display_transform_001"
                )
            if self.linked_engine_capability_id != "enginecap_display_transform_001":
                raise ValueError(
                    "aiservice_coding_001 must link enginecap_display_transform_001"
                )
            if self.linked_real_backend_id != "realbackend_display_python_001":
                raise ValueError(
                    "aiservice_coding_001 must link realbackend_display_python_001"
                )
            if self.linked_orchestration_entry_id != "orchestration_mobile_entry_001":
                raise ValueError(
                    "aiservice_coding_001 must link orchestration_mobile_entry_001"
                )
            if self.linked_voice_runtime_entry_id != "realvoice_show_memory_001":
                raise ValueError(
                    "aiservice_coding_001 must link realvoice_show_memory_001"
                )

        if self.real_ai_service_entry_id == "aiservice_visual_001":
            if self.service_kind != "visual_service":
                raise ValueError("aiservice_visual_001 must use visual_service")
            if self.model_adapter_kind != "deepseek_adapter":
                raise ValueError("aiservice_visual_001 must use deepseek_adapter")
            if self.linked_engine_adapter_id != "engineadapter_optics_worker_001":
                raise ValueError(
                    "aiservice_visual_001 must link engineadapter_optics_worker_001"
                )
            if self.linked_engine_capability_id != "enginecap_optics_001":
                raise ValueError(
                    "aiservice_visual_001 must link enginecap_optics_001"
                )
            if self.linked_real_backend_id != "realbackend_optics_gpu_001":
                raise ValueError(
                    "aiservice_visual_001 must link realbackend_optics_gpu_001"
                )
            if self.linked_orchestration_entry_id != "orchestration_mobile_entry_001":
                raise ValueError(
                    "aiservice_visual_001 must link orchestration_mobile_entry_001"
                )
            if self.linked_voice_runtime_entry_id != "realvoice_show_monitoring_001":
                raise ValueError(
                    "aiservice_visual_001 must link realvoice_show_monitoring_001"
                )


@dataclass(frozen=True, slots=True)
class RealAiServicesModelAdaptersContract:
    """Unified real AI services / model adapters contract."""

    total_entries: int
    reasoning_entries: int
    coding_entries: int
    visual_entries: int
    active_entries: int
    entries: tuple[RealAiServicesModelAdaptersEntry, ...]

    def __post_init__(self) -> None:
        """Validate real AI services / model adapters contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        reasoning_entries = sum(
            1 for entry in self.entries if entry.service_kind == "reasoning_service"
        )
        coding_entries = sum(
            1 for entry in self.entries if entry.service_kind == "coding_service"
        )
        visual_entries = sum(
            1 for entry in self.entries if entry.service_kind == "visual_service"
        )
        active_entries = sum(
            1 for entry in self.entries if entry.service_runtime_status == "active"
        )

        if self.reasoning_entries != reasoning_entries:
            raise ValueError("reasoning_entries must match computed count")

        if self.coding_entries != coding_entries:
            raise ValueError("coding_entries must match computed count")

        if self.visual_entries != visual_entries:
            raise ValueError("visual_entries must match computed count")

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        entry_ids = tuple(entry.real_ai_service_entry_id for entry in self.entries)
        service_kinds = tuple(entry.service_kind for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate real_ai_service_entry_id values detected")

        if len(set(service_kinds)) != len(service_kinds):
            raise ValueError("Duplicate service_kind values detected")


def build_real_ai_services_model_adapters_contract() -> RealAiServicesModelAdaptersContract:
    """Build canonical real AI services / model adapters contract."""
    engine_adapters = build_engine_adapter_boundary_contract()
    engine_capabilities = build_engine_capability_contract()
    real_backends = build_real_engine_backends_contract()
    orchestration = build_end_to_end_orchestration_runtime_contract()
    real_voice = build_real_voice_runtime_contract()

    engine_adapter_ids = {entry.engine_adapter_id for entry in engine_adapters.entries}
    engine_capability_ids = {entry.engine_capability_id for entry in engine_capabilities.entries}
    real_backend_ids = {entry.real_backend_entry_id for entry in real_backends.entries}
    orchestration_ids = {entry.orchestration_entry_id for entry in orchestration.entries}
    real_voice_ids = {entry.real_voice_runtime_entry_id for entry in real_voice.entries}

    required_engine_adapter_ids = {
        "engineadapter_simulation_worker_001",
        "engineadapter_display_transform_001",
        "engineadapter_optics_worker_001",
    }
    required_engine_capability_ids = {
        "enginecap_simulation_001",
        "enginecap_display_transform_001",
        "enginecap_optics_001",
    }
    required_real_backend_ids = {
        "realbackend_simulation_native_001",
        "realbackend_display_python_001",
        "realbackend_optics_gpu_001",
    }
    required_orchestration_ids = {
        "orchestration_heavy_execution_001",
        "orchestration_mobile_entry_001",
    }
    required_real_voice_ids = {
        "realvoice_show_memory_001",
        "realvoice_show_simulation_001",
        "realvoice_show_monitoring_001",
    }

    for label, required, actual in (
        ("engine adapter ids", required_engine_adapter_ids, engine_adapter_ids),
        ("engine capability ids", required_engine_capability_ids, engine_capability_ids),
        ("real backend ids", required_real_backend_ids, real_backend_ids),
        ("orchestration ids", required_orchestration_ids, orchestration_ids),
        ("real voice ids", required_real_voice_ids, real_voice_ids),
    ):
        missing = required - actual
        if missing:
            raise ValueError(f"Missing {label}: {sorted(missing)}")

    entries = (
        RealAiServicesModelAdaptersEntry(
            real_ai_service_entry_id="aiservice_reasoning_001",
            service_kind="reasoning_service",
            model_adapter_kind="glm_adapter",
            linked_engine_adapter_id="engineadapter_simulation_worker_001",
            linked_engine_capability_id="enginecap_simulation_001",
            linked_real_backend_id="realbackend_simulation_native_001",
            linked_orchestration_entry_id="orchestration_heavy_execution_001",
            linked_voice_runtime_entry_id="realvoice_show_simulation_001",
            adapter_boundary_mode="service_via_adapter",
            network_free_direct_core_access=False,
            sandbox_required=True,
            explainable_required=True,
            production_path_allowed=True,
            service_runtime_status="active",
            description="Canonical real AI reasoning service via model adapter.",
        ),
        RealAiServicesModelAdaptersEntry(
            real_ai_service_entry_id="aiservice_coding_001",
            service_kind="coding_service",
            model_adapter_kind="qwen_adapter",
            linked_engine_adapter_id="engineadapter_display_transform_001",
            linked_engine_capability_id="enginecap_display_transform_001",
            linked_real_backend_id="realbackend_display_python_001",
            linked_orchestration_entry_id="orchestration_mobile_entry_001",
            linked_voice_runtime_entry_id="realvoice_show_memory_001",
            adapter_boundary_mode="service_via_adapter",
            network_free_direct_core_access=False,
            sandbox_required=True,
            explainable_required=True,
            production_path_allowed=True,
            service_runtime_status="active",
            description="Canonical real AI coding service via model adapter.",
        ),
        RealAiServicesModelAdaptersEntry(
            real_ai_service_entry_id="aiservice_visual_001",
            service_kind="visual_service",
            model_adapter_kind="deepseek_adapter",
            linked_engine_adapter_id="engineadapter_optics_worker_001",
            linked_engine_capability_id="enginecap_optics_001",
            linked_real_backend_id="realbackend_optics_gpu_001",
            linked_orchestration_entry_id="orchestration_mobile_entry_001",
            linked_voice_runtime_entry_id="realvoice_show_monitoring_001",
            adapter_boundary_mode="service_via_adapter",
            network_free_direct_core_access=False,
            sandbox_required=True,
            explainable_required=True,
            production_path_allowed=True,
            service_runtime_status="active",
            description="Canonical real AI visual service via model adapter.",
        ),
    )

    reasoning_entries = sum(
        1 for entry in entries if entry.service_kind == "reasoning_service"
    )
    coding_entries = sum(
        1 for entry in entries if entry.service_kind == "coding_service"
    )
    visual_entries = sum(
        1 for entry in entries if entry.service_kind == "visual_service"
    )
    active_entries = sum(
        1 for entry in entries if entry.service_runtime_status == "active"
    )

    return RealAiServicesModelAdaptersContract(
        total_entries=len(entries),
        reasoning_entries=reasoning_entries,
        coding_entries=coding_entries,
        visual_entries=visual_entries,
        active_entries=active_entries,
        entries=entries,
    )
