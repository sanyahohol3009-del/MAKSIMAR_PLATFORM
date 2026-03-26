from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_contract import (
    build_foundation_truth_consistency_contract,
)


def test_foundation_truth_consistency_contract_counts() -> None:
    """Truth consistency contract should expose expected counts."""
    contract = build_foundation_truth_consistency_contract()

    assert contract.total_entries == 4
    assert contract.consistent_entries == 1
    assert contract.mismatch_entries == 0
    assert contract.partial_entries == 3
    assert contract.unknown_entries == 0


def test_foundation_truth_consistency_contract_runtime_entry() -> None:
    """Truth consistency contract should expose runtime entry."""
    contract = build_foundation_truth_consistency_contract()
    entry = contract.entries[0]

    assert entry.consistency_entry_id == "foundationconsistency_runtime_001"
    assert entry.component_id == "foundation_runtime_component_001"
    assert entry.truth_scope == "runtime"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is True
    assert entry.log_truth is True
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "CONSISTENT"


def test_foundation_truth_consistency_contract_kernel_entry() -> None:
    """Truth consistency contract should expose kernel entry."""
    contract = build_foundation_truth_consistency_contract()
    entry = contract.entries[-1]

    assert entry.consistency_entry_id == "foundationconsistency_kernel_guard_001"
    assert entry.component_id == "foundation_kernel_guard_component_001"
    assert entry.truth_scope == "kernel_guard"
    assert entry.heartbeat_truth is True
    assert entry.process_truth is True
    assert entry.session_truth is True
    assert entry.api_truth is False
    assert entry.log_truth is True
    assert entry.derived_status == "ALIVE"
    assert entry.consistency_status == "PARTIAL"


def test_foundation_truth_consistency_contract_scope_order() -> None:
    """Truth consistency contract should preserve canonical scope order."""
    contract = build_foundation_truth_consistency_contract()

    assert [entry.truth_scope for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
