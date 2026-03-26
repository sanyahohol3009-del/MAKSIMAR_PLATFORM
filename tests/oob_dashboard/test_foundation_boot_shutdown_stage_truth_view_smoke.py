from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_boot_shutdown_stage_truth_view import (
    build_foundation_boot_shutdown_stage_truth_view,
)


def test_foundation_boot_shutdown_stage_truth_view_counts() -> None:
    """Boot/shutdown stage truth view should expose expected counts."""
    view = build_foundation_boot_shutdown_stage_truth_view()

    assert view.view_id == "foundation_boot_shutdown_stage_truth_view_001"
    assert view.total_entries == 6
    assert view.boot_entries == 3
    assert view.shutdown_entries == 3
    assert view.pending_entries == 3
    assert view.active_entries == 0
    assert view.completed_entries == 3
    assert view.failed_entries == 0


def test_foundation_boot_shutdown_stage_truth_view_boot_entry() -> None:
    """Boot/shutdown stage truth view should expose first boot entry."""
    view = build_foundation_boot_shutdown_stage_truth_view()
    entry = view.entries[0]

    assert entry.stage_entry_id == "foundation_boot_stage_001"
    assert entry.lifecycle_kind == "boot"
    assert entry.stage_order_index == 1
    assert entry.stage_id == "boot_integrity_check"
    assert entry.display_title == "Boot Integrity Check"
    assert entry.stage_state == "COMPLETED"
    assert entry.timeout_threshold_seconds == 15
    assert entry.waiting_condition is None
    assert entry.failed_stage is False
    assert entry.read_only is True


def test_foundation_boot_shutdown_stage_truth_view_shutdown_entry() -> None:
    """Boot/shutdown stage truth view should expose last shutdown entry."""
    view = build_foundation_boot_shutdown_stage_truth_view()
    entry = view.entries[-1]

    assert entry.stage_entry_id == "foundation_shutdown_stage_003"
    assert entry.lifecycle_kind == "shutdown"
    assert entry.stage_order_index == 3
    assert entry.stage_id == "shutdown_runtime_stop"
    assert entry.display_title == "Runtime Stop"
    assert entry.stage_state == "PENDING"
    assert entry.timeout_threshold_seconds == 15
    assert entry.waiting_condition == "Awaiting shutdown command."
    assert entry.failed_stage is False
    assert entry.read_only is True


def test_foundation_boot_shutdown_stage_truth_view_order() -> None:
    """Boot/shutdown stage truth view should preserve canonical ordering."""
    view = build_foundation_boot_shutdown_stage_truth_view()

    assert [entry.lifecycle_kind for entry in view.entries] == [
        "boot",
        "boot",
        "boot",
        "shutdown",
        "shutdown",
        "shutdown",
    ]
    assert [entry.stage_order_index for entry in view.entries] == [1, 2, 3, 1, 2, 3]
