from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_dashboard_layout_read_view_contract import (
    build_foundation_dashboard_layout_read_view_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_dashboard_workspace_contract import (
    build_foundation_dashboard_workspace_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter import (
    build_foundation_live_status_snapshot,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_menu_registry_contract import (
    build_foundation_status_menu_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_visual_composition_contract import (
    build_foundation_visual_composition_contract,
)


@dataclass(frozen=True)
class FoundationUnifiedDashboardPanelView:
    """Unified read-only panel view for the foundation dashboard."""

    panel_id: str
    display_title: str
    menu_label: str
    short_status_label: str
    truth_scope: str
    derived_state: str
    layout_zone: str
    visual_layer: str
    visual_anchor: str
    startup_stage_index: int
    left_menu_visible: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    read_only: bool


@dataclass(frozen=True)
class FoundationUnifiedDashboardView:
    """Unified read-only dashboard view for foundation monitoring."""

    view_id: str
    view_title: str
    total_panels: int
    alive_panels: int
    dead_panels: int
    degraded_panels: int
    broken_panels: int
    warming_up_panels: int
    left_menu_panels: int
    center_core_panels: int
    guard_ring_panels: int
    startup_order_valid: bool
    panels: tuple[FoundationUnifiedDashboardPanelView, ...]


def build_foundation_unified_dashboard_view() -> FoundationUnifiedDashboardView:
    """Build a unified read-only foundation dashboard view."""
    live_snapshot = build_foundation_live_status_snapshot()
    menu_registry = build_foundation_status_menu_registry_contract()
    visual_composition = build_foundation_visual_composition_contract()
    layout_view = build_foundation_dashboard_layout_read_view_contract()
    workspace = build_foundation_dashboard_workspace_contract()

    live_by_panel = {record.truth_scope: record for record in live_snapshot.records}
    menu_by_panel = {entry.panel_id: entry for entry in menu_registry.entries}
    visual_by_panel = {entry.panel_id: entry for entry in visual_composition.entries}
    layout_by_panel = {entry.panel_id: entry for entry in layout_view.entries}

    scope_by_panel_id = {
        "panel_foundation_runtime_status_001": "runtime",
        "panel_foundation_guard_status_001": "guard",
        "panel_foundation_core_guard_status_001": "core_guard",
        "panel_foundation_kernel_guard_status_001": "kernel_guard",
    }

    panels = []
    for workspace_entry in workspace.entries:
        panel_id = workspace_entry.panel_id
        truth_scope = scope_by_panel_id[panel_id]

        live_record = live_by_panel[truth_scope]
        menu_entry = menu_by_panel[panel_id]
        visual_entry = visual_by_panel[panel_id]
        layout_entry = layout_by_panel[panel_id]

        panels.append(
            FoundationUnifiedDashboardPanelView(
                panel_id=panel_id,
                display_title=workspace_entry.display_title,
                menu_label=menu_entry.menu_label,
                short_status_label=menu_entry.short_status_label,
                truth_scope=truth_scope,
                derived_state=live_record.derived_state,
                layout_zone=layout_entry.layout_zone,
                visual_layer=visual_entry.visual_layer,
                visual_anchor=visual_entry.visual_anchor,
                startup_stage_index=workspace_entry.startup_stage_index,
                left_menu_visible=workspace_entry.left_menu_visible,
                signal_path_visible=workspace_entry.signal_path_visible,
                execution_stage_visible=workspace_entry.execution_stage_visible,
                read_only=workspace_entry.read_only,
            )
        )

    panel_tuple = tuple(sorted(panels, key=lambda item: item.startup_stage_index))

    startup_order_valid = [panel.startup_stage_index for panel in panel_tuple] == [1, 2, 3, 4]

    return FoundationUnifiedDashboardView(
        view_id="foundation_unified_dashboard_view_001",
        view_title="Foundation Unified Dashboard View",
        total_panels=len(panel_tuple),
        alive_panels=sum(1 for panel in panel_tuple if panel.derived_state == "ALIVE"),
        dead_panels=sum(1 for panel in panel_tuple if panel.derived_state == "DEAD"),
        degraded_panels=sum(
            1 for panel in panel_tuple if panel.derived_state == "DEGRADED"
        ),
        broken_panels=sum(1 for panel in panel_tuple if panel.derived_state == "BROKEN"),
        warming_up_panels=sum(
            1 for panel in panel_tuple if panel.derived_state == "WARMING_UP"
        ),
        left_menu_panels=sum(1 for panel in panel_tuple if panel.left_menu_visible),
        center_core_panels=sum(1 for panel in panel_tuple if panel.layout_zone == "center_core"),
        guard_ring_panels=sum(
            1 for panel in panel_tuple if panel.layout_zone in {"inner_ring", "outer_ring"}
        ),
        startup_order_valid=startup_order_valid,
        panels=panel_tuple,
    )
