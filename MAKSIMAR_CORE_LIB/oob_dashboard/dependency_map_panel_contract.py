from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DependencyMapPanelEntry:
    """Canonical dependency map panel entry."""

    upstream_module_id: str
    downstream_module_id: str
    dependency_kind: str
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class DependencyMapPanelContract:
    """Canonical dependency map panel contract."""

    panel_id: str
    total_entries: int
    entries: Tuple[DependencyMapPanelEntry, ...]
    operator_visible: bool
    description: str


def build_dependency_map_panel_contract() -> DependencyMapPanelContract:
    """Build canonical dependency map panel contract."""
    entries = (
        DependencyMapPanelEntry(
            upstream_module_id="control_plane",
            downstream_module_id="execution_control",
            dependency_kind="execution_dependency",
            operator_visible=True,
            description="Canonical control-plane to execution-control dependency.",
        ),
        DependencyMapPanelEntry(
            upstream_module_id="execution_control",
            downstream_module_id="execution_observability",
            dependency_kind="execution_dependency",
            operator_visible=True,
            description="Canonical execution-control to execution-observability dependency.",
        ),
        DependencyMapPanelEntry(
            upstream_module_id="execution_observability",
            downstream_module_id="oob_dashboard",
            dependency_kind="projection_dependency",
            operator_visible=True,
            description="Canonical execution-observability to OOB dashboard dependency.",
        ),
    )

    return DependencyMapPanelContract(
        panel_id="panel_dependency_map",
        total_entries=len(entries),
        entries=entries,
        operator_visible=True,
        description="Canonical dependency map panel contract.",
    )
