from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_phase_readiness,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_phase_readiness,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_phase_readiness,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import build_memory_registry_contract


_FLOW_ID_PATTERN = re.compile(r"^arch_memory_flow_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_positive_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value <= 0:
        raise ValueError(f"{field_name} must be > 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class MemoryDataFlowBindingEntry:
    flow_id: str
    step_order: int
    source_layer: str
    target_layer: str
    flow_name: str
    source_contract_bound: bool
    target_contract_bound: bool
    dashboard_visible: bool
    flow_ready: bool

    def __post_init__(self) -> None:
        flow_id = _ensure_non_empty_str(self.flow_id, "flow_id")
        source_layer = _ensure_non_empty_str(self.source_layer, "source_layer")
        target_layer = _ensure_non_empty_str(self.target_layer, "target_layer")
        flow_name = _ensure_non_empty_str(self.flow_name, "flow_name")
        step_order = _ensure_positive_int(self.step_order, "step_order")

        if not _FLOW_ID_PATTERN.fullmatch(flow_id):
            raise ValueError(f"Invalid flow_id: {flow_id}")

        for field_name in (
            "source_contract_bound",
            "target_contract_bound",
            "dashboard_visible",
            "flow_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_contract_bound:
            raise ValueError("source_contract_bound must be True")
        if not self.target_contract_bound:
            raise ValueError("target_contract_bound must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.flow_ready:
            raise ValueError("flow_ready must be True")

        object.__setattr__(self, "flow_id", flow_id)
        object.__setattr__(self, "step_order", step_order)
        object.__setattr__(self, "source_layer", source_layer)
        object.__setattr__(self, "target_layer", target_layer)
        object.__setattr__(self, "flow_name", flow_name)


@dataclass(frozen=True, slots=True)
class MemoryDataFlowBindingContract:
    total_flows: int
    ready_flows: int
    dashboard_visible_flows: int
    source_bound_flows: int
    target_bound_flows: int
    entries: tuple[MemoryDataFlowBindingEntry, ...]

    def __post_init__(self) -> None:
        total_flows = _ensure_positive_int(self.total_flows, "total_flows")

        if total_flows != len(self.entries):
            raise ValueError("total_flows must match entries length")

        computed_ready = sum(1 for entry in self.entries if entry.flow_ready)
        computed_dashboard = sum(1 for entry in self.entries if entry.dashboard_visible)
        computed_source = sum(1 for entry in self.entries if entry.source_contract_bound)
        computed_target = sum(1 for entry in self.entries if entry.target_contract_bound)

        if self.ready_flows != computed_ready:
            raise ValueError("ready_flows must match computed count")
        if self.dashboard_visible_flows != computed_dashboard:
            raise ValueError("dashboard_visible_flows must match computed count")
        if self.source_bound_flows != computed_source:
            raise ValueError("source_bound_flows must match computed count")
        if self.target_bound_flows != computed_target:
            raise ValueError("target_bound_flows must match computed count")

        if self.ready_flows != total_flows:
            raise ValueError("all memory data flows must be ready")
        if self.dashboard_visible_flows != total_flows:
            raise ValueError("all memory data flows must be dashboard-visible")
        if self.source_bound_flows != total_flows or self.target_bound_flows != total_flows:
            raise ValueError("all memory data flows must be source/target bound")

        orders = tuple(entry.step_order for entry in self.entries)
        if orders != tuple(sorted(orders)):
            raise ValueError("memory data flow entries must be ordered")
        if len(set(orders)) != len(orders):
            raise ValueError("duplicate step_order values detected")

        flow_ids = tuple(entry.flow_id for entry in self.entries)
        if len(set(flow_ids)) != len(flow_ids):
            raise ValueError("duplicate flow_id values detected")


def build_memory_data_flow_binding_contract() -> MemoryDataFlowBindingContract:
    memory_registry = build_memory_registry_contract()
    storage = build_storage_registry_phase_readiness()
    media = build_media_memory_phase_readiness()
    retrieval = build_retrieval_phase_readiness()
    dashboard = build_dashboard_read_only_views_phase_readiness()

    if memory_registry.active_entries <= 0:
        raise ValueError("memory registry must expose active entries")
    if not storage.phase_core_ready:
        raise ValueError("storage registry phase must be ready")
    if not media.phase_core_ready:
        raise ValueError("media memory phase must be ready")
    if not retrieval.phase_ready:
        raise ValueError("retrieval phase must be ready")
    if not dashboard.phase_ready:
        raise ValueError("dashboard read-only phase must be ready")

    entries = (
        MemoryDataFlowBindingEntry(
            flow_id="arch_memory_flow_registry_to_storage",
            step_order=1,
            source_layer="MEMORY_REGISTRY",
            target_layer="STORAGE_REGISTRY",
            flow_name="memory_registry_to_storage_registry",
            source_contract_bound=True,
            target_contract_bound=True,
            dashboard_visible=True,
            flow_ready=True,
        ),
        MemoryDataFlowBindingEntry(
            flow_id="arch_memory_flow_storage_to_media",
            step_order=2,
            source_layer="STORAGE_REGISTRY",
            target_layer="MEDIA_MEMORY",
            flow_name="storage_registry_to_media_memory",
            source_contract_bound=True,
            target_contract_bound=True,
            dashboard_visible=True,
            flow_ready=True,
        ),
        MemoryDataFlowBindingEntry(
            flow_id="arch_memory_flow_media_to_retrieval",
            step_order=3,
            source_layer="MEDIA_MEMORY",
            target_layer="RETRIEVAL_ORCHESTRATION",
            flow_name="media_memory_to_retrieval_orchestration",
            source_contract_bound=True,
            target_contract_bound=True,
            dashboard_visible=True,
            flow_ready=True,
        ),
        MemoryDataFlowBindingEntry(
            flow_id="arch_memory_flow_retrieval_to_dashboard",
            step_order=4,
            source_layer="RETRIEVAL_ORCHESTRATION",
            target_layer="DASHBOARD_READ_ONLY_VIEWS",
            flow_name="retrieval_trace_to_dashboard_read_only_views",
            source_contract_bound=True,
            target_contract_bound=True,
            dashboard_visible=True,
            flow_ready=True,
        ),
    )

    return MemoryDataFlowBindingContract(
        total_flows=len(entries),
        ready_flows=sum(1 for entry in entries if entry.flow_ready),
        dashboard_visible_flows=sum(1 for entry in entries if entry.dashboard_visible),
        source_bound_flows=sum(1 for entry in entries if entry.source_contract_bound),
        target_bound_flows=sum(1 for entry in entries if entry.target_contract_bound),
        entries=entries,
    )
