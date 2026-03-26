from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_derived_view_contract import (
    build_foundation_live_status_derived_view_contract,
)


def test_foundation_live_status_derived_view_contract_counts() -> None:
    """Foundation derived live-status contract should expose expected counts."""
    contract = build_foundation_live_status_derived_view_contract()

    assert contract.total_entries == 4
    assert contract.alive_entries == 4
    assert contract.dead_entries == 0
    assert contract.degraded_entries == 0
    assert contract.broken_entries == 0
    assert contract.warming_up_entries == 0
    assert contract.signal_visible_entries == 4
    assert contract.execution_stage_visible_entries == 4


def test_foundation_live_status_derived_view_contract_runtime_entry() -> None:
    """Foundation derived live-status contract should expose runtime entry."""
    contract = build_foundation_live_status_derived_view_contract()
    entry = contract.entries[0]

    assert entry.derived_entry_id == "foundationderived_runtime_001"
    assert entry.panel_id == "panel_foundation_runtime_status_001"
    assert entry.truth_scope == "runtime"
    assert entry.display_title == "Runtime Core"
    assert entry.status_command == "./tools/ctl status"
    assert entry.expected_alive_label == "ALIVE"
    assert entry.expected_dead_label == "NOT_ALIVE"
    assert entry.derived_state == "ALIVE"
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.read_only is True


def test_foundation_live_status_derived_view_contract_kernel_entry() -> None:
    """Foundation derived live-status contract should expose kernel entry."""
    contract = build_foundation_live_status_derived_view_contract()
    entry = contract.entries[-1]

    assert entry.derived_entry_id == "foundationderived_kernel_guard_001"
    assert entry.panel_id == "panel_foundation_kernel_guard_status_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.display_title == "Kernel Watchdog"
    assert entry.status_command == "./tools/kernel_guard_ctl status"
    assert entry.expected_alive_label == "ALIVE"
    assert entry.expected_dead_label == "NOT_ALIVE"
    assert entry.derived_state == "ALIVE"
    assert entry.signal_path_visible is True
    assert entry.execution_stage_visible is True
    assert entry.read_only is True


def test_foundation_live_status_derived_view_contract_preserves_scope_order() -> None:
    """Foundation derived live-status contract should preserve expected scope order."""
    contract = build_foundation_live_status_derived_view_contract()

    assert [entry.truth_scope for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
    assert [entry.derived_state for entry in contract.entries] == [
        "ALIVE",
        "ALIVE",
        "ALIVE",
        "ALIVE",
    ]
