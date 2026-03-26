from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_failure_localization_view import (
    build_foundation_incident_failure_localization_view,
)


def test_foundation_incident_failure_localization_view_shape() -> None:
    """Incident/failure localization view should expose expected top-level shape."""
    view = build_foundation_incident_failure_localization_view()

    assert view.view_id == "foundation_incident_failure_localization_view_001"
    assert view.total_entries == 4
    assert len(view.entries) == 4
    assert view.critical_entries >= 0
    assert view.warning_entries >= 0
    assert view.info_entries >= 0


def test_foundation_incident_failure_localization_view_runtime_entry() -> None:
    """Incident/failure localization view should expose runtime entry."""
    view = build_foundation_incident_failure_localization_view()
    entry = view.entries[0]

    assert entry.localization_entry_id == "foundationfailure_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.failure_stage == "runtime_execution"
    assert entry.suspected_source_file == "SUPERVISOR/process_supervisor.py"


def test_foundation_incident_failure_localization_view_kernel_entry() -> None:
    """Incident/failure localization view should expose kernel entry."""
    view = build_foundation_incident_failure_localization_view()
    entry = view.entries[-1]

    assert entry.localization_entry_id == "foundationfailure_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.failure_stage == "kernel_watchdog_supervision"
    assert entry.suspected_source_file == "CORE_ROOT/kernel_watchdog.py"


def test_foundation_incident_failure_localization_view_scope_order() -> None:
    """Incident/failure localization view should preserve canonical scope order."""
    view = build_foundation_incident_failure_localization_view()

    assert [entry.truth_scope for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
