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
