from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_snapshot_contract import (
    build_foundation_incident_snapshot_contract,
)


def test_foundation_incident_snapshot_contract_counts() -> None:
    """Incident snapshot contract should expose expected counts."""
    contract = build_foundation_incident_snapshot_contract()

    assert contract.total_entries == 4
    assert contract.snapshot_available_entries == 4
    assert contract.current_incident_entries == 4
    assert contract.kill_chain_triggered_entries == 1
    assert contract.critical_entries == 1
    assert contract.warning_entries == 3
    assert contract.info_entries == 0


def test_foundation_incident_snapshot_contract_runtime_entry() -> None:
    """Incident snapshot contract should expose runtime snapshot entry."""
    contract = build_foundation_incident_snapshot_contract()
    entry = contract.entries[0]

    assert entry.snapshot_entry_id == "foundation_snapshot_runtime_001"
    assert entry.incident_id == "foundationincident_runtime_001"
    assert entry.source_component == "runtime"
    assert entry.failing_stage == "runtime_execution"
    assert entry.severity == "warning"
    assert entry.incident_state == "ACTIVE"
    assert entry.kill_chain_triggered is False
    assert entry.snapshot_available is True
    assert entry.current_incident is True


def test_foundation_incident_snapshot_contract_kernel_entry() -> None:
    """Incident snapshot contract should expose kernel snapshot entry."""
    contract = build_foundation_incident_snapshot_contract()
    entry = contract.entries[-1]

    assert entry.snapshot_entry_id == "foundation_snapshot_kernel_guard_001"
    assert entry.incident_id == "foundationincident_kernel_guard_001"
    assert entry.source_component == "kernel_guard"
    assert entry.failing_stage == "kernel_watchdog_supervision"
    assert entry.severity == "critical"
    assert entry.incident_state == "ACTIVE"
    assert entry.kill_chain_triggered is True
    assert entry.snapshot_available is True
    assert entry.current_incident is True


def test_foundation_incident_snapshot_contract_scope_order() -> None:
    """Incident snapshot contract should preserve canonical scope order."""
    contract = build_foundation_incident_snapshot_contract()

    assert [entry.source_component for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
