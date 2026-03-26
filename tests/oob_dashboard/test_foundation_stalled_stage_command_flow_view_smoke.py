from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_stalled_stage_command_flow_view import (
    build_foundation_stalled_stage_command_flow_view,
)


def test_foundation_stalled_stage_command_flow_view_shape() -> None:
    """Stalled-stage / command-flow view should expose expected shape."""
    view = build_foundation_stalled_stage_command_flow_view()

    assert view.view_id == "foundation_stalled_stage_command_flow_view_001"
    assert view.total_entries == 4
    assert len(view.entries) == 4
    assert view.command_flow_visible_entries == 4
    assert view.stalled_stage_visible_entries >= 0


def test_foundation_stalled_stage_command_flow_view_runtime_entry() -> None:
    """Stalled-stage / command-flow view should expose runtime entry."""
    view = build_foundation_stalled_stage_command_flow_view()
    entry = view.entries[0]

    assert entry.flow_entry_id == "foundationflow_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.command_stage == "runtime_execution"
    assert entry.command_flow_visible is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.suspected_source_file == "SUPERVISOR/process_supervisor.py"


def test_foundation_stalled_stage_command_flow_view_kernel_entry() -> None:
    """Stalled-stage / command-flow view should expose kernel entry."""
    view = build_foundation_stalled_stage_command_flow_view()
    entry = view.entries[-1]

    assert entry.flow_entry_id == "foundationflow_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.command_stage == "kernel_watchdog_supervision"
    assert entry.command_flow_visible is True
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.suspected_source_file == "CORE_ROOT/kernel_watchdog.py"


def test_foundation_stalled_stage_command_flow_view_scope_order() -> None:
    """Stalled-stage / command-flow view should preserve canonical scope order."""
    view = build_foundation_stalled_stage_command_flow_view()

    assert [entry.truth_scope for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
