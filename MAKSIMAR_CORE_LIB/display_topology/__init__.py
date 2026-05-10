from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    DisplayAvailabilityStatus,
    DisplayCapability,
    DisplayTargetRole,
    DisplayTopologyContract,
    DisplayTopologyEntry,
    DisplayVisibilityMode,
    build_display_topology_contract,
)

_LAZY_EXPORTS = {
    "build_display_assignment_binding_contract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_assignment_binding_models",
        "build_display_assignment_binding_contract",
    ),
    "build_display_capability_binding_contract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_capability_models",
        "build_display_capability_binding_contract",
    ),
    "build_zone_layout_contract": (
        "MAKSIMAR_CORE_LIB.display_topology.zone_layout_models",
        "build_zone_layout_contract",
    ),
    "build_display_role_binding_contract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_role_models",
        "build_display_role_binding_contract",
    ),
    "build_display_registry_contract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_registry_models",
        "build_display_registry_contract",
    ),
    "DisplayAssignmentBindingEntry": (
        "MAKSIMAR_CORE_LIB.display_topology.display_assignment_binding_models",
        "DisplayAssignmentBindingEntry",
    ),
    "DisplayAssignmentBindingContract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_assignment_binding_models",
        "DisplayAssignmentBindingContract",
    ),
    "DisplayCapabilityBindingEntry": (
        "MAKSIMAR_CORE_LIB.display_topology.display_capability_models",
        "DisplayCapabilityBindingEntry",
    ),
    "DisplayCapabilityBindingContract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_capability_models",
        "DisplayCapabilityBindingContract",
    ),
    "ZoneLayoutEntry": (
        "MAKSIMAR_CORE_LIB.display_topology.zone_layout_models",
        "ZoneLayoutEntry",
    ),
    "ZoneLayoutContract": (
        "MAKSIMAR_CORE_LIB.display_topology.zone_layout_models",
        "ZoneLayoutContract",
    ),
    "DisplayRoleBindingEntry": (
        "MAKSIMAR_CORE_LIB.display_topology.display_role_models",
        "DisplayRoleBindingEntry",
    ),
    "DisplayRoleBindingContract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_role_models",
        "DisplayRoleBindingContract",
    ),
    "DisplayRegistryEntry": (
        "MAKSIMAR_CORE_LIB.display_topology.display_registry_models",
        "DisplayRegistryEntry",
    ),
    "DisplayRegistryContract": (
        "MAKSIMAR_CORE_LIB.display_topology.display_registry_models",
        "DisplayRegistryContract",
    ),
    "DisplayTopologyPhaseReadiness": (
        "MAKSIMAR_CORE_LIB.display_topology.display_topology_phase_readiness",
        "DisplayTopologyPhaseReadiness",
    ),
    "build_display_topology_summary": (
        "MAKSIMAR_CORE_LIB.display_topology.display_topology_summary_builder",
        "build_display_topology_summary",
    ),
    "build_display_topology_preview": (
        "MAKSIMAR_CORE_LIB.display_topology.display_topology_preview_builder",
        "build_display_topology_preview",
    ),
    "build_display_topology_phase_preview": (
        "MAKSIMAR_CORE_LIB.display_topology.display_topology_phase_readiness",
        "build_display_topology_phase_preview",
    ),
    "build_display_topology_phase_readiness": (
        "MAKSIMAR_CORE_LIB.display_topology.display_topology_phase_readiness",
        "build_display_topology_phase_readiness",
    ),
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, attr_name = _LAZY_EXPORTS[name]

    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


__all__ = [
    "DisplayAvailabilityStatus",
    "DisplayCapability",
    "DisplayTargetRole",
    "DisplayTopologyContract",
    "DisplayTopologyEntry",
    "DisplayTopologyPhaseReadiness",
    "DisplayVisibilityMode",
    "build_display_topology_contract",
    "build_display_topology_phase_preview",
    "build_display_topology_phase_readiness",
    "build_display_topology_preview",
    "build_display_topology_summary",
]
