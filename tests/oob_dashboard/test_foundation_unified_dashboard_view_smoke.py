from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view import (
    build_foundation_unified_dashboard_view,
)


def test_foundation_unified_dashboard_view_counts() -> None:
    """Unified foundation dashboard view should expose expected counts."""
    view = build_foundation_unified_dashboard_view()

    assert view.view_id == "foundation_unified_dashboard_view_001"
    assert view.view_title == "Foundation Unified Dashboard View"
    assert view.total_panels == 4
    assert view.left_menu_panels == 4
    assert view.center_core_panels == 1
    assert view.guard_ring_panels == 3
    assert view.startup_order_valid is True


def test_foundation_unified_dashboard_view_runtime_panel() -> None:
    """Unified foundation dashboard view should expose runtime center panel."""
    view = build_foundation_unified_dashboard_view()
    panel = view.panels[0]

    assert panel.panel_id == "panel_foundation_runtime_status_001"
    assert panel.display_title == "Runtime Core"
    assert panel.menu_label == "Runtime Core"
    assert panel.short_status_label == "RUNTIME"
    assert panel.truth_scope == "runtime"
    assert panel.layout_zone == "center_core"
    assert panel.visual_layer == "central_core"
    assert panel.visual_anchor == "center"
    assert panel.startup_stage_index == 1
    assert panel.left_menu_visible is True
    assert panel.signal_path_visible is True
    assert panel.execution_stage_visible is True
    assert panel.read_only is True


def test_foundation_unified_dashboard_view_kernel_panel() -> None:
    """Unified foundation dashboard view should expose kernel outer ring panel."""
    view = build_foundation_unified_dashboard_view()
    panel = view.panels[-1]

    assert panel.panel_id == "panel_foundation_kernel_guard_status_001"
    assert panel.display_title == "Kernel Watchdog"
    assert panel.menu_label == "Kernel Watchdog"
    assert panel.short_status_label == "KERNEL"
    assert panel.truth_scope == "kernel_guard"
    assert panel.layout_zone == "outer_ring"
    assert panel.visual_layer == "outer_guard_ring"
    assert panel.visual_anchor == "ring_outer_top"
    assert panel.startup_stage_index == 4
    assert panel.left_menu_visible is True
    assert panel.signal_path_visible is True
    assert panel.execution_stage_visible is True
    assert panel.read_only is True


def test_foundation_unified_dashboard_view_preserves_order() -> None:
    """Unified foundation dashboard view should preserve startup order."""
    view = build_foundation_unified_dashboard_view()

    assert [panel.startup_stage_index for panel in view.panels] == [1, 2, 3, 4]
    assert [panel.truth_scope for panel in view.panels] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
