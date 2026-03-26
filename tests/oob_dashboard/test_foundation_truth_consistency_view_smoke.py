from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view import (
    build_foundation_truth_consistency_view,
)


def test_foundation_truth_consistency_view_counts() -> None:
    """Truth consistency view should expose expected counts."""
    view = build_foundation_truth_consistency_view()

    assert view.view_id == "foundation_truth_consistency_view_001"
    assert view.total_entries == 4
    assert view.consistent_entries == 1
    assert view.partial_entries == 3
    assert view.mismatch_entries == 0
    assert view.unknown_entries == 0


def test_foundation_truth_consistency_view_runtime_entry() -> None:
    """Truth consistency view should expose runtime entry."""
    view = build_foundation_truth_consistency_view()
    entry = view.entries[0]

    assert entry.view_entry_id == "foundationtruthview_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "CONSISTENT"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is True
    assert entry.log_truth is True
    assert entry.read_only is True


def test_foundation_truth_consistency_view_kernel_entry() -> None:
    """Truth consistency view should expose kernel entry."""
    view = build_foundation_truth_consistency_view()
    entry = view.entries[-1]

    assert entry.view_entry_id == "foundationtruthview_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "PARTIAL"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is False
    assert entry.log_truth is True
    assert entry.read_only is True


def test_foundation_truth_consistency_view_scope_order() -> None:
    """Truth consistency view should preserve canonical scope order."""
    view = build_foundation_truth_consistency_view()

    assert [entry.truth_scope for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
