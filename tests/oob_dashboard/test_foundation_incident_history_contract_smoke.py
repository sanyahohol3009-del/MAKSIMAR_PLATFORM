from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_history_contract import (
    build_foundation_incident_history_contract,
)


def test_foundation_incident_history_contract_counts() -> None:
    """Incident history contract should expose expected counts."""
    contract = build_foundation_incident_history_contract()

    assert contract.total_entries == 4
    assert contract.history_visible_entries == 4
    assert contract.archived_entries == 0
    assert contract.recovered_entries == 0
    assert contract.critical_entries == 1
    assert contract.warning_entries == 3
    assert contract.info_entries == 0


def test_foundation_incident_history_contract_runtime_entry() -> None:
    """Incident history contract should expose runtime history entry."""
    contract = build_foundation_incident_history_contract()
    entry = contract.entries[0]

    assert entry.history_entry_id == "foundation_history_runtime_001"
    assert entry.incident_id == "foundationincident_runtime_001"
    assert entry.source_component == "runtime"
    assert entry.failing_stage == "runtime_execution"
    assert entry.incident_state == "ACTIVE"
    assert entry.severity == "warning"
    assert entry.archived is False
    assert entry.recovered is False
    assert entry.history_visible is True


def test_foundation_incident_history_contract_kernel_entry() -> None:
    """Incident history contract should expose kernel history entry."""
    contract = build_foundation_incident_history_contract()
    entry = contract.entries[-1]

    assert entry.history_entry_id == "foundation_history_kernel_guard_001"
    assert entry.incident_id == "foundationincident_kernel_guard_001"
    assert entry.source_component == "kernel_guard"
    assert entry.failing_stage == "kernel_watchdog_supervision"
    assert entry.incident_state == "ACTIVE"
    assert entry.severity == "critical"
    assert entry.archived is False
    assert entry.recovered is False
    assert entry.history_visible is True


def test_foundation_incident_history_contract_scope_order() -> None:
    """Incident history contract should preserve canonical scope order."""
    contract = build_foundation_incident_history_contract()

    assert [entry.source_component for entry in contract.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
