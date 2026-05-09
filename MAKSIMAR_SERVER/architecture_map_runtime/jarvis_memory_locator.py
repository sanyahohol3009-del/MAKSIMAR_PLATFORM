from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import build_memory_registry_contract
from MAKSIMAR_SERVER.architecture_map_runtime.memory_data_flow_binding import (
    build_memory_data_flow_binding_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.memory_layer_architecture_binding import (
    build_memory_layer_architecture_binding_contract,
)


_LOCATOR_ID_PATTERN = re.compile(r"^jarvis_memory_locator_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class JarvisMemoryLocatorEntry:
    locator_id: str
    memory_surface: str
    runtime_path: str
    architecture_binding_ref: str
    dashboard_binding_ref: str
    read_only: bool
    locator_ready: bool

    def __post_init__(self) -> None:
        locator_id = _ensure_non_empty_str(self.locator_id, "locator_id")
        memory_surface = _ensure_non_empty_str(self.memory_surface, "memory_surface")
        runtime_path = _ensure_non_empty_str(self.runtime_path, "runtime_path")
        architecture_binding_ref = _ensure_non_empty_str(
            self.architecture_binding_ref,
            "architecture_binding_ref",
        )
        dashboard_binding_ref = _ensure_non_empty_str(
            self.dashboard_binding_ref,
            "dashboard_binding_ref",
        )

        if not _LOCATOR_ID_PATTERN.fullmatch(locator_id):
            raise ValueError(f"Invalid locator_id: {locator_id}")

        _ensure_bool(self.read_only, "read_only")
        _ensure_bool(self.locator_ready, "locator_ready")

        if not self.read_only:
            raise ValueError("JARVIS memory locator must be read-only")
        if not self.locator_ready:
            raise ValueError("JARVIS memory locator must be ready")

        object.__setattr__(self, "locator_id", locator_id)
        object.__setattr__(self, "memory_surface", memory_surface)
        object.__setattr__(self, "runtime_path", runtime_path)
        object.__setattr__(self, "architecture_binding_ref", architecture_binding_ref)
        object.__setattr__(self, "dashboard_binding_ref", dashboard_binding_ref)


@dataclass(frozen=True, slots=True)
class JarvisMemoryLocatorContract:
    total_locators: int
    ready_locators: int
    read_only_locators: int
    entries: tuple[JarvisMemoryLocatorEntry, ...]

    def __post_init__(self) -> None:
        if self.total_locators != len(self.entries):
            raise ValueError("total_locators must match entries length")
        if self.total_locators <= 0:
            raise ValueError("total_locators must be >= 1")

        if self.ready_locators != sum(1 for entry in self.entries if entry.locator_ready):
            raise ValueError("ready_locators must match computed count")
        if self.read_only_locators != sum(1 for entry in self.entries if entry.read_only):
            raise ValueError("read_only_locators must match computed count")

        if self.ready_locators != self.total_locators:
            raise ValueError("all JARVIS memory locators must be ready")
        if self.read_only_locators != self.total_locators:
            raise ValueError("all JARVIS memory locators must be read-only")

        locator_ids = tuple(entry.locator_id for entry in self.entries)
        if len(set(locator_ids)) != len(locator_ids):
            raise ValueError("duplicate locator_id values detected")


def build_jarvis_memory_locator_contract() -> JarvisMemoryLocatorContract:
    memory_registry = build_memory_registry_contract()
    architecture_binding = build_memory_layer_architecture_binding_contract()
    data_flow = build_memory_data_flow_binding_contract()
    dashboard = build_dashboard_read_only_views_phase_readiness()

    if architecture_binding.ready_bindings != architecture_binding.total_bindings:
        raise ValueError("architecture memory bindings must be ready")
    if data_flow.ready_flows != data_flow.total_flows:
        raise ValueError("memory data flow bindings must be ready")
    if not dashboard.phase_ready:
        raise ValueError("dashboard read-only phase must be ready")

    memory_entry = memory_registry.entries[0]

    entries = (
        JarvisMemoryLocatorEntry(
            locator_id="jarvis_memory_locator_memory_registry",
            memory_surface="MEMORY_REGISTRY",
            runtime_path="MAKSIMAR_SERVER/MEMORY_REGISTRY",
            architecture_binding_ref="arch_memory_binding_memory_registry",
            dashboard_binding_ref="dashboardview_memory_domain_map",
            read_only=True,
            locator_ready=True,
        ),
        JarvisMemoryLocatorEntry(
            locator_id="jarvis_memory_locator_project_architecture",
            memory_surface=memory_entry.memory_tier_id,
            runtime_path="MAKSIMAR_CORE_LIB/memory_engine/history_binding",
            architecture_binding_ref="arch_memory_binding_memory_registry",
            dashboard_binding_ref="dashboardview_memory_project_architecture",
            read_only=True,
            locator_ready=True,
        ),
        JarvisMemoryLocatorEntry(
            locator_id="jarvis_memory_locator_retrieval_trace",
            memory_surface="RETRIEVAL_ORCHESTRATION",
            runtime_path="MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing",
            architecture_binding_ref="arch_memory_binding_dashboard_views",
            dashboard_binding_ref="dashboardview_memory_retrieval_trace",
            read_only=True,
            locator_ready=True,
        ),
    )

    return JarvisMemoryLocatorContract(
        total_locators=len(entries),
        ready_locators=sum(1 for entry in entries if entry.locator_ready),
        read_only_locators=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
