from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_degraded_state_contract import (
    build_foundation_degraded_state_contract,
)


def test_foundation_degraded_state_contract_counts() -> None:
    """Degraded-state contract should expose expected counts."""
    contract = build_foundation_degraded_state_contract()

    assert contract.total_entries == 4
    assert contract.currently_degraded_entries == 0
    assert contract.historical_only_entries == 0
    assert contract.recovered_entries == 0


def test_foundation_degraded_state_contract_runtime_entry() -> None:
    """Degraded-state contract should expose runtime entry."""
    contract = build_foundation_degraded_state_contract()
    entry = contract.entries[0]

    assert entry.degraded_entry_id == "foundationdegraded_runtime_001"
    assert entry.component_id == "foundation_runtime_component_001"
    assert entry.truth_scope == "runtime"
    assert entry.is_currently_degraded is False
    assert entry.degraded_since_monotonic is None
    assert entry.degraded_reason is None
    assert entry.recovered_at_monotonic is None
    assert entry.historical_only is False


def test_foundation_degraded_state_contract_kernel_entry() -> None:
    """Degraded-state contract should expose kernel entry."""
    contract = build_foundation_degraded_state_contract()
    entry = contract.entries[-1]

    assert entry.degraded_entry_id == "foundationdegraded_kernel_guard_001"
    assert entry.component_id == "foundation_kernel_guard_component_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.is_currently_degraded is False
    assert entry.degraded_since_monotonic is None
    assert entry.degraded_reason is None
    assert entry.recovered_at_monotonic is None
    assert entry.historical_only is False


def test_foundation_degraded_state_contract_scope_order() -> None:
    """Degraded-state contract should preserve canonical scope order."""
    contract = build_foundation_degraded_state_contract()

    assert [entry.truth_scope for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
