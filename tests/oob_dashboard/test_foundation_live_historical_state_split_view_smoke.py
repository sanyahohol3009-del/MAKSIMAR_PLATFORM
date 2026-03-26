from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_historical_state_split_view import (
    build_foundation_live_historical_state_split_view,
)


def test_foundation_live_historical_state_split_view_counts() -> None:
    """Live/historical split view should expose expected counts."""
    view = build_foundation_live_historical_state_split_view()

    assert view.view_id == "foundation_live_historical_state_split_view_001"
    assert view.total_entries == 4
    assert view.live_entries == 4
    assert view.historical_only_entries == 0
    assert view.current_degraded_entries == 0
    assert view.current_live_visible_entries == 4


def test_foundation_live_historical_state_split_view_runtime_entry() -> None:
    """Live/historical split view should expose runtime entry."""
    view = build_foundation_live_historical_state_split_view()
    entry = view.entries[0]

    assert entry.split_entry_id == "foundationstatesplit_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.currently_degraded is False
    assert entry.historical_only is False
    assert entry.historical_state_visible is False
    assert entry.show_as_current_live_state is True
    assert entry.read_only is True


def test_foundation_live_historical_state_split_view_kernel_entry() -> None:
    """Live/historical split view should expose kernel entry."""
    view = build_foundation_live_historical_state_split_view()
    entry = view.entries[-1]

    assert entry.split_entry_id == "foundationstatesplit_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.currently_degraded is False
    assert entry.historical_only is False
    assert entry.historical_state_visible is False
    assert entry.show_as_current_live_state is True
    assert entry.read_only is True


def test_foundation_live_historical_state_split_view_scope_order() -> None:
    """Live/historical split view should preserve canonical scope order."""
    view = build_foundation_live_historical_state_split_view()

    assert [entry.truth_scope for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
