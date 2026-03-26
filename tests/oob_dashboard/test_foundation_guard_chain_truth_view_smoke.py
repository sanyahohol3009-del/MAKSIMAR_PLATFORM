from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view import (
    build_foundation_guard_chain_truth_view,
)


def test_foundation_guard_chain_truth_view_counts() -> None:
    """Guard-chain truth view should expose expected counts."""
    view = build_foundation_guard_chain_truth_view()

    assert view.view_id == "foundation_guard_chain_truth_view_001"
    assert view.total_entries == 4
    assert view.consistent_entries == 1
    assert view.partial_entries == 3
    assert view.mismatch_entries == 0
    assert view.unknown_entries == 0
    assert view.alive_entries == 4
    assert view.degraded_entries == 0
    assert view.dead_entries == 0
    assert view.broken_entries == 0


def test_foundation_guard_chain_truth_view_runtime_entry() -> None:
    """Guard-chain truth view should expose runtime entry."""
    view = build_foundation_guard_chain_truth_view()
    entry = view.entries[0]

    assert entry.guard_entry_id == "foundation_guard_chain_runtime_001"
    assert entry.chain_order_index == 1
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is True
    assert entry.log_truth is True
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "CONSISTENT"
    assert entry.last_seen_label == "fresh"
    assert entry.reason is None
    assert entry.read_only is True


def test_foundation_guard_chain_truth_view_kernel_entry() -> None:
    """Guard-chain truth view should expose kernel entry."""
    view = build_foundation_guard_chain_truth_view()
    entry = view.entries[-1]

    assert entry.guard_entry_id == "foundation_guard_chain_kernel_guard_001"
    assert entry.chain_order_index == 4
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is False
    assert entry.log_truth is True
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "PARTIAL"
    assert entry.last_seen_label == "fresh"
    assert entry.reason == "Truth sources are only partially aligned."
    assert entry.read_only is True


def test_foundation_guard_chain_truth_view_order() -> None:
    """Guard-chain truth view should preserve canonical chain order."""
    view = build_foundation_guard_chain_truth_view()

    assert [entry.truth_scope for entry in view.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
    assert [entry.chain_order_index for entry in view.entries] == [1, 2, 3, 4]
