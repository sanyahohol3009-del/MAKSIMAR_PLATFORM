from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_global_registry_preview,
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.server_architecture_shell_contract import (
    build_server_architecture_map_shell_contract,
)


_BINDING_ID_PATTERN = re.compile(r"^arch_memory_binding_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class MemoryLayerArchitectureBindingEntry:
    binding_id: str
    memory_layer: str
    architecture_surface: str
    memory_entries: int
    architecture_modules: int
    architecture_dependencies: int
    architecture_flows: int
    dashboard_views: int
    source_contract_bound: bool
    dashboard_visible: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        memory_layer = _ensure_non_empty_str(self.memory_layer, "memory_layer")
        architecture_surface = _ensure_non_empty_str(
            self.architecture_surface,
            "architecture_surface",
        )

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")

        for field_name in (
            "memory_entries",
            "architecture_modules",
            "architecture_dependencies",
            "architecture_flows",
            "dashboard_views",
        ):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in ("source_contract_bound", "dashboard_visible", "binding_ready"):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.architecture_modules <= 0:
            raise ValueError("architecture_modules must be >= 1")
        if self.dashboard_views <= 0:
            raise ValueError("dashboard_views must be >= 1")
        if not self.source_contract_bound:
            raise ValueError("source_contract_bound must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "memory_layer", memory_layer)
        object.__setattr__(self, "architecture_surface", architecture_surface)


@dataclass(frozen=True, slots=True)
class MemoryLayerArchitectureBindingContract:
    total_bindings: int
    ready_bindings: int
    dashboard_visible_bindings: int
    source_contract_bound_bindings: int
    entries: tuple[MemoryLayerArchitectureBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(self.total_bindings, "total_bindings")
        ready_bindings = _ensure_non_negative_int(self.ready_bindings, "ready_bindings")
        dashboard_visible_bindings = _ensure_non_negative_int(
            self.dashboard_visible_bindings,
            "dashboard_visible_bindings",
        )
        source_contract_bound_bindings = _ensure_non_negative_int(
            self.source_contract_bound_bindings,
            "source_contract_bound_bindings",
        )

        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")
        if ready_bindings != sum(1 for entry in self.entries if entry.binding_ready):
            raise ValueError("ready_bindings must match computed count")
        if dashboard_visible_bindings != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_bindings must match computed count")
        if source_contract_bound_bindings != sum(
            1 for entry in self.entries if entry.source_contract_bound
        ):
            raise ValueError("source_contract_bound_bindings must match computed count")

        if ready_bindings != total_bindings:
            raise ValueError("all architecture memory bindings must be ready")
        if dashboard_visible_bindings != total_bindings:
            raise ValueError("all architecture memory bindings must be dashboard-visible")
        if source_contract_bound_bindings != total_bindings:
            raise ValueError("all architecture memory bindings must be source-bound")

        binding_ids = tuple(entry.binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate binding_id values detected")

        object.__setattr__(self, "total_bindings", total_bindings)
        object.__setattr__(self, "ready_bindings", ready_bindings)
        object.__setattr__(self, "dashboard_visible_bindings", dashboard_visible_bindings)
        object.__setattr__(
            self,
            "source_contract_bound_bindings",
            source_contract_bound_bindings,
        )


def build_memory_layer_architecture_binding_contract() -> MemoryLayerArchitectureBindingContract:
    shell = build_server_architecture_map_shell_contract()
    memory_registry = build_memory_registry_contract()
    global_registry = build_global_registry_preview()
    dashboard = build_dashboard_read_only_views_phase_readiness()

    entries = (
        MemoryLayerArchitectureBindingEntry(
            binding_id="arch_memory_binding_memory_registry",
            memory_layer="MEMORY_REGISTRY",
            architecture_surface="MAKSIMAR_SERVER/architecture_map_runtime",
            memory_entries=memory_registry.total_entries,
            architecture_modules=shell.total_module_views,
            architecture_dependencies=shell.total_dependency_views,
            architecture_flows=shell.total_flow_views,
            dashboard_views=dashboard.root_total_entries,
            source_contract_bound=True,
            dashboard_visible=True,
            binding_ready=True,
        ),
        MemoryLayerArchitectureBindingEntry(
            binding_id="arch_memory_binding_global_registry",
            memory_layer="GLOBAL_REGISTRY",
            architecture_surface="MAKSIMAR_SERVER/architecture_map_runtime",
            memory_entries=int(global_registry["total_entries"]),
            architecture_modules=shell.total_module_views,
            architecture_dependencies=shell.total_dependency_views,
            architecture_flows=shell.total_flow_views,
            dashboard_views=dashboard.root_total_entries,
            source_contract_bound=True,
            dashboard_visible=True,
            binding_ready=True,
        ),
        MemoryLayerArchitectureBindingEntry(
            binding_id="arch_memory_binding_dashboard_views",
            memory_layer="DASHBOARD_READ_ONLY_VIEWS",
            architecture_surface="MAKSIMAR_SERVER/architecture_map_runtime",
            memory_entries=dashboard.root_total_entries,
            architecture_modules=shell.total_module_views,
            architecture_dependencies=shell.total_dependency_views,
            architecture_flows=shell.total_flow_views,
            dashboard_views=dashboard.root_total_entries,
            source_contract_bound=True,
            dashboard_visible=True,
            binding_ready=True,
        ),
    )

    return MemoryLayerArchitectureBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        dashboard_visible_bindings=sum(1 for entry in entries if entry.dashboard_visible),
        source_contract_bound_bindings=sum(
            1 for entry in entries if entry.source_contract_bound
        ),
        entries=entries,
    )
