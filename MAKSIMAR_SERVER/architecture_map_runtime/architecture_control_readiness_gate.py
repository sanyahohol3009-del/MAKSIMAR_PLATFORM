from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_phase_readiness,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)
from MAKSIMAR_SERVER.architecture_map_runtime.domain_cube_memory_locator import (
    build_domain_cube_memory_locator_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.jarvis_memory_locator import (
    build_jarvis_memory_locator_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.memory_data_flow_binding import (
    build_memory_data_flow_binding_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.memory_dependency_summary_builder import (
    build_memory_dependency_summary,
)
from MAKSIMAR_SERVER.architecture_map_runtime.memory_layer_architecture_binding import (
    build_memory_layer_architecture_binding_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.server_architecture_shell_contract import (
    build_server_architecture_map_shell_contract,
)


_EXPECTED_PHASE_2_FLOW = (
    "server_architecture_shell",
    "memory_layer_architecture_binding",
    "memory_data_flow_binding",
    "jarvis_memory_locator",
    "domain_cube_memory_locator",
    "dashboard_read_only_binding",
    "retrieval_policy_gate",
    "architecture_control_readiness",
)


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
class ArchitectureControlPhaseReadiness:
    architecture_module_views: int
    architecture_dependency_views: int
    architecture_flow_views: int
    memory_architecture_bindings: int
    memory_data_flows: int
    jarvis_memory_locators: int
    domain_cube_memory_locators: int
    dashboard_root_entries: int
    retrieval_selected_sources: int
    retrieval_evidence_items: int
    flow: tuple[str, ...]
    architecture_shell_ready: bool
    memory_architecture_binding_ready: bool
    memory_data_flow_ready: bool
    jarvis_memory_locator_ready: bool
    domain_cube_memory_locator_ready: bool
    dashboard_read_only_ready: bool
    retrieval_ready: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    read_only: bool
    no_mutation_surface: bool
    no_network_surface: bool
    no_new_architecture_root: bool
    no_platform_inspector_root: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        for field_name in (
            "architecture_module_views",
            "architecture_dependency_views",
            "architecture_flow_views",
            "memory_architecture_bindings",
            "memory_data_flows",
            "jarvis_memory_locators",
            "domain_cube_memory_locators",
            "dashboard_root_entries",
            "retrieval_selected_sources",
            "retrieval_evidence_items",
        ):
            value = _ensure_non_negative_int(getattr(self, field_name), field_name)
            if value <= 0:
                raise ValueError(f"{field_name} must be >= 1")

        if tuple(self.flow) != _EXPECTED_PHASE_2_FLOW:
            raise ValueError("flow must match expected PHASE 2 flow")

        for field_name in (
            "architecture_shell_ready",
            "memory_architecture_binding_ready",
            "memory_data_flow_ready",
            "jarvis_memory_locator_ready",
            "domain_cube_memory_locator_ready",
            "dashboard_read_only_ready",
            "retrieval_ready",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
            "read_only",
            "no_mutation_surface",
            "no_network_surface",
            "no_new_architecture_root",
            "no_platform_inspector_root",
            "phase_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.architecture_shell_ready:
            raise ValueError("architecture_shell_ready must be True")
        if not self.memory_architecture_binding_ready:
            raise ValueError("memory_architecture_binding_ready must be True")
        if not self.memory_data_flow_ready:
            raise ValueError("memory_data_flow_ready must be True")
        if not self.jarvis_memory_locator_ready:
            raise ValueError("jarvis_memory_locator_ready must be True")
        if not self.domain_cube_memory_locator_ready:
            raise ValueError("domain_cube_memory_locator_ready must be True")
        if not self.dashboard_read_only_ready:
            raise ValueError("dashboard_read_only_ready must be True")
        if not self.retrieval_ready:
            raise ValueError("retrieval_ready must be True")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False in PHASE 2")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.no_mutation_surface:
            raise ValueError("no_mutation_surface must be True")
        if not self.no_network_surface:
            raise ValueError("no_network_surface must be True")
        if not self.no_new_architecture_root:
            raise ValueError("no_new_architecture_root must be True")
        if not self.no_platform_inspector_root:
            raise ValueError("no_platform_inspector_root must be True")
        if not self.phase_ready:
            raise ValueError("phase_ready must be True")


def build_architecture_control_phase_readiness() -> ArchitectureControlPhaseReadiness:
    shell = build_server_architecture_map_shell_contract()
    architecture_binding = build_memory_layer_architecture_binding_contract()
    data_flow = build_memory_data_flow_binding_contract()
    jarvis_locator = build_jarvis_memory_locator_contract()
    domain_cube_locator = build_domain_cube_memory_locator_contract()
    dependency_summary = build_memory_dependency_summary()
    dashboard = build_dashboard_read_only_views_phase_readiness()
    retrieval = build_retrieval_phase_readiness()

    no_new_architecture_root = (
        not Path("MAKSIMAR_SERVER/ARCHITECTURE_MAP_RUNTIME").exists()
        and not Path("MAKSIMAR_SERVER/ARCHITECTURE_MAP").exists()
    )
    no_platform_inspector_root = not Path("MAKSIMAR_SERVER/PLATFORM_INSPECTOR").exists()

    architecture_shell_ready = (
        shell.total_module_views >= 1
        and shell.total_dependency_views >= 1
        and shell.total_flow_views >= 1
    )
    memory_architecture_binding_ready = (
        architecture_binding.ready_bindings == architecture_binding.total_bindings
    )
    memory_data_flow_ready = data_flow.ready_flows == data_flow.total_flows
    jarvis_memory_locator_ready = (
        jarvis_locator.ready_locators == jarvis_locator.total_locators
        and jarvis_locator.read_only_locators == jarvis_locator.total_locators
    )
    domain_cube_memory_locator_ready = (
        domain_cube_locator.ready_cubes == domain_cube_locator.total_cubes
        and domain_cube_locator.dashboard_visible_cubes == domain_cube_locator.total_cubes
    )

    read_only = (
        bool(dependency_summary["read_only"])
        and jarvis_locator.read_only_locators == jarvis_locator.total_locators
        and dashboard.read_only_entries == dashboard.root_total_entries
    )
    no_mutation_surface = (
        read_only
        and dashboard.no_mutation_surface
        and not retrieval.backend_execution_allowed
    )
    no_network_surface = True

    phase_ready = (
        architecture_shell_ready
        and memory_architecture_binding_ready
        and memory_data_flow_ready
        and jarvis_memory_locator_ready
        and domain_cube_memory_locator_ready
        and dashboard.phase_ready
        and retrieval.phase_ready
        and retrieval.mgrep_blocked
        and retrieval.sqlite_vec_blocked
        and not retrieval.backend_execution_allowed
        and read_only
        and no_mutation_surface
        and no_network_surface
        and no_new_architecture_root
        and no_platform_inspector_root
    )

    return ArchitectureControlPhaseReadiness(
        architecture_module_views=shell.total_module_views,
        architecture_dependency_views=shell.total_dependency_views,
        architecture_flow_views=shell.total_flow_views,
        memory_architecture_bindings=architecture_binding.total_bindings,
        memory_data_flows=data_flow.total_flows,
        jarvis_memory_locators=jarvis_locator.total_locators,
        domain_cube_memory_locators=domain_cube_locator.total_cubes,
        dashboard_root_entries=dashboard.root_total_entries,
        retrieval_selected_sources=retrieval.selected_source_count,
        retrieval_evidence_items=retrieval.evidence_item_count,
        flow=_EXPECTED_PHASE_2_FLOW,
        architecture_shell_ready=architecture_shell_ready,
        memory_architecture_binding_ready=memory_architecture_binding_ready,
        memory_data_flow_ready=memory_data_flow_ready,
        jarvis_memory_locator_ready=jarvis_memory_locator_ready,
        domain_cube_memory_locator_ready=domain_cube_memory_locator_ready,
        dashboard_read_only_ready=dashboard.phase_ready,
        retrieval_ready=retrieval.phase_ready,
        mgrep_blocked=retrieval.mgrep_blocked,
        sqlite_vec_blocked=retrieval.sqlite_vec_blocked,
        backend_execution_allowed=retrieval.backend_execution_allowed,
        read_only=read_only,
        no_mutation_surface=no_mutation_surface,
        no_network_surface=no_network_surface,
        no_new_architecture_root=no_new_architecture_root,
        no_platform_inspector_root=no_platform_inspector_root,
        phase_ready=phase_ready,
    )


def build_architecture_control_phase_preview() -> Dict[str, object]:
    readiness = build_architecture_control_phase_readiness()

    return {
        "flow": readiness.flow,
        "architecture_module_views": readiness.architecture_module_views,
        "architecture_dependency_views": readiness.architecture_dependency_views,
        "architecture_flow_views": readiness.architecture_flow_views,
        "memory_architecture_bindings": readiness.memory_architecture_bindings,
        "memory_data_flows": readiness.memory_data_flows,
        "jarvis_memory_locators": readiness.jarvis_memory_locators,
        "domain_cube_memory_locators": readiness.domain_cube_memory_locators,
        "dashboard_root_entries": readiness.dashboard_root_entries,
        "retrieval_selected_sources": readiness.retrieval_selected_sources,
        "retrieval_evidence_items": readiness.retrieval_evidence_items,
        "architecture_shell_ready": readiness.architecture_shell_ready,
        "memory_architecture_binding_ready": readiness.memory_architecture_binding_ready,
        "memory_data_flow_ready": readiness.memory_data_flow_ready,
        "jarvis_memory_locator_ready": readiness.jarvis_memory_locator_ready,
        "domain_cube_memory_locator_ready": readiness.domain_cube_memory_locator_ready,
        "dashboard_read_only_ready": readiness.dashboard_read_only_ready,
        "retrieval_ready": readiness.retrieval_ready,
        "mgrep_blocked": readiness.mgrep_blocked,
        "sqlite_vec_blocked": readiness.sqlite_vec_blocked,
        "backend_execution_allowed": readiness.backend_execution_allowed,
        "read_only": readiness.read_only,
        "no_mutation_surface": readiness.no_mutation_surface,
        "no_network_surface": readiness.no_network_surface,
        "no_new_architecture_root": readiness.no_new_architecture_root,
        "no_platform_inspector_root": readiness.no_platform_inspector_root,
        "phase_ready": readiness.phase_ready,
        "preview_ready": True,
    }
