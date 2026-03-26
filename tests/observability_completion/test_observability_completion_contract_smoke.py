from __future__ import annotations

from MAKSIMAR_CORE_LIB.observability_completion import (
    build_observability_completion_contract,
)


def test_observability_completion_contract_builds() -> None:
    """Observability completion contract should build successfully."""
    contract = build_observability_completion_contract()

    assert contract.total_entries == 6
    assert contract.total_events_across_components == 28
    assert contract.total_alerting_events == 4
    assert contract.critical_components == 2
    assert contract.completed_entries == 6


def test_observability_completion_contract_contains_expected_validation_entry() -> None:
    """Observability completion should expose expected validation entry."""
    contract = build_observability_completion_contract()
    entry = contract.entries[0]

    assert entry.source_component == "validation_metrics"
    assert entry.total_events == 4
    assert entry.critical_events == 1
    assert entry.alerting_events == 1
    assert entry.highest_severity == "critical"


def test_observability_completion_contract_contains_expected_pressure_entry() -> None:
    """Observability completion should expose expected pressure entry."""
    contract = build_observability_completion_contract()
    entry = contract.entries[1]

    assert entry.source_component == "pressure_metrics"
    assert entry.total_events == 3
    assert entry.warning_events == 1
    assert entry.alerting_events == 1
    assert entry.highest_severity == "warning"


def test_observability_completion_contract_contains_expected_execution_views_entry() -> None:
    """Observability completion should expose expected execution views entry."""
    contract = build_observability_completion_contract()
    entry = contract.entries[3]

    assert entry.source_component == "execution_views"
    assert entry.total_events == 10
    assert entry.warning_events == 3
    assert entry.critical_events == 1
    assert entry.alerting_events == 2
    assert entry.highest_severity == "critical"


def test_observability_completion_contract_preserves_completed_status() -> None:
    """Observability completion should preserve completed status."""
    contract = build_observability_completion_contract()

    for entry in contract.entries:
        assert entry.explanation_ready is True
        assert entry.active is True
        assert entry.completion_valid is True
        assert entry.completion_status == "completed"
