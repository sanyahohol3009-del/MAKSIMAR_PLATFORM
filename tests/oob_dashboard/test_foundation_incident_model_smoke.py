from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_model import (
    build_foundation_incident_model,
)


def test_foundation_incident_model_counts() -> None:
    """Incident model should expose expected counts."""
    model = build_foundation_incident_model()

    assert model.total_entries == 4
    assert model.new_entries == 0
    assert model.active_entries == 4
    assert model.confirmed_entries == 0
    assert model.recovered_entries == 0
    assert model.archived_entries == 0
    assert model.critical_entries == 1
    assert model.warning_entries == 3
    assert model.info_entries == 0


def test_foundation_incident_model_runtime_entry() -> None:
    """Incident model should expose runtime incident entry."""
    model = build_foundation_incident_model()
    entry = model.entries[0]

    assert entry.incident_id == "foundationincident_runtime_001"
    assert entry.incident_state == "ACTIVE"
    assert entry.source_component == "runtime"
    assert entry.failing_stage == "runtime_execution"
    assert entry.truth_source_trigger == "heartbeat_truth"
    assert entry.severity == "warning"
    assert entry.kill_chain_triggered is False
    assert entry.recovered_at_monotonic is None


def test_foundation_incident_model_kernel_entry() -> None:
    """Incident model should expose kernel incident entry."""
    model = build_foundation_incident_model()
    entry = model.entries[-1]

    assert entry.incident_id == "foundationincident_kernel_guard_001"
    assert entry.incident_state == "ACTIVE"
    assert entry.source_component == "kernel_guard"
    assert entry.failing_stage == "kernel_watchdog_supervision"
    assert entry.truth_source_trigger == "heartbeat_truth"
    assert entry.severity == "critical"
    assert entry.kill_chain_triggered is True
    assert entry.recovered_at_monotonic is None


def test_foundation_incident_model_scope_order() -> None:
    """Incident model should preserve canonical scope order."""
    model = build_foundation_incident_model()

    assert [entry.source_component for entry in model.entries] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]
