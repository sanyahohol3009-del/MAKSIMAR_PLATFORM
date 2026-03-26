from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_diagnostics_correlation_view import (
    build_foundation_diagnostics_correlation_view,
)


def test_foundation_diagnostics_correlation_view_shape() -> None:
    """Diagnostics correlation view should expose expected shape."""
    view = build_foundation_diagnostics_correlation_view()

    assert view.view_id == "foundation_diagnostics_correlation_view_001"
    assert view.total_entries == 4
    assert len(view.entries) == 4
    assert view.alive_entries >= 0
    assert view.flowing_entries >= 0
    assert view.incident_visible_entries >= 0
    assert view.failure_visible_entries >= 0


def test_foundation_diagnostics_correlation_view_runtime_entry() -> None:
    """Diagnostics correlation view should expose runtime entry."""
    view = build_foundation_diagnostics_correlation_view()
    entry = view.entries[0]

    assert entry.correlation_entry_id == "foundationdiagnostics_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.failure_stage == "runtime_execution"
    assert entry.suspected_source_file == "SUPERVISOR/process_supervisor.py"


def test_foundation_diagnostics_correlation_view_kernel_entry() -> None:
    """Diagnostics correlation view should expose kernel entry."""
    view = build_foundation_diagnostics_correlation_view()
    entry = view.entries[-1]

    assert entry.correlation_entry_id == "foundationdiagnostics_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.failure_stage == "kernel_watchdog_supervision"
    assert entry.suspected_source_file == "CORE_ROOT/kernel_watchdog.py"


def test_foundation_diagnostics_correlation_view_scope_order() -> None:
    """Diagnostics correlation view should preserve canonical scope order."""
    view = build_foundation_diagnostics_correlation_view()

    assert [entry.truth_scope for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
