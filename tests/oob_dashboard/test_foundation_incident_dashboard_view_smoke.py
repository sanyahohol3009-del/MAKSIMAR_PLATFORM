from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_dashboard_view import (
    build_foundation_incident_dashboard_view,
)


def test_foundation_incident_dashboard_view_counts() -> None:
    """Incident dashboard view should expose expected counts."""
    view = build_foundation_incident_dashboard_view()

    assert view.view_id == "foundation_incident_dashboard_view_001"
    assert view.total_entries == 4
    assert view.current_incident_entries == 4
    assert view.history_visible_entries == 4
    assert view.kill_chain_triggered_entries == 1
    assert view.archived_entries == 0
    assert view.recovered_entries == 0
    assert view.critical_entries == 1
    assert view.warning_entries == 3
    assert view.info_entries == 0


def test_foundation_incident_dashboard_view_runtime_entry() -> None:
    """Incident dashboard view should expose runtime entry."""
    view = build_foundation_incident_dashboard_view()
    entry = view.entries[0]

    assert (
        entry.dashboard_entry_id
        == "foundation_incident_dashboard_runtime_001"
    )
    assert entry.incident_id == "foundationincident_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.source_component == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.failing_stage == "runtime_execution"
    assert entry.incident_state == "ACTIVE"
    assert entry.severity == "warning"
    assert entry.current_incident is True
    assert entry.history_visible is True
    assert entry.kill_chain_triggered is False
    assert entry.archived is False
    assert entry.recovered is False
    assert entry.read_only is True


def test_foundation_incident_dashboard_view_kernel_entry() -> None:
    """Incident dashboard view should expose kernel entry."""
    view = build_foundation_incident_dashboard_view()
    entry = view.entries[-1]

    assert (
        entry.dashboard_entry_id
        == "foundation_incident_dashboard_kernel_guard_001"
    )
    assert entry.incident_id == "foundationincident_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.source_component == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.failing_stage == "kernel_watchdog_supervision"
    assert entry.incident_state == "ACTIVE"
    assert entry.severity == "critical"
    assert entry.current_incident is True
    assert entry.history_visible is True
    assert entry.kill_chain_triggered is True
    assert entry.archived is False
    assert entry.recovered is False
    assert entry.read_only is True


def test_foundation_incident_dashboard_view_scope_order() -> None:
    """Incident dashboard view should preserve canonical scope order."""
    view = build_foundation_incident_dashboard_view()

    assert [entry.source_component for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
