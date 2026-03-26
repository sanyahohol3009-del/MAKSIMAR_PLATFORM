from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_module_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.project_map_panel_models import (
    ProjectMapPanelContract,
    ProjectMapPanelEntry,
)


def build_project_map_panel_contract() -> ProjectMapPanelContract:
    """Build unified read-only project map panel contract."""
    registry = build_module_registry_contract()

    entries = tuple(
        ProjectMapPanelEntry(
            module_id=module.module_id,
            layer_name=module.layer_name,
            criticality=module.criticality,
            read_only_view_available=module.read_only_view_available,
        )
        for module in registry.modules
    )

    return ProjectMapPanelContract(
        panel_id="panel_project_map",
        total_entries=len(entries),
        entries=entries,
    )
