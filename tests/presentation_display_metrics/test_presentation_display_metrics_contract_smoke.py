from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.presentation_display_metrics import (
    build_presentation_display_metrics_contract,
)


def test_presentation_display_metrics_contract_builds() -> None:
    """Presentation/display metrics contract should build successfully."""
    contract = build_presentation_display_metrics_contract()

    assert contract.total_entries == 3
    assert contract.private_route_entries == 1
    assert contract.shared_route_entries == 2
    assert contract.explanation_bound_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_presentation_display_metrics_contract_contains_expected_routes() -> None:
    """Presentation/display metrics should expose expected routed entries."""
    contract = build_presentation_display_metrics_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.route_request_id == "displayroute_show_memory_001"
    assert first.display_role == "mobile_display_proxy"
    assert first.visibility_mode == "private"
    assert first.panel_id == "panel_memory_project_architecture"

    assert second.route_request_id == "displayroute_show_simulation_001"
    assert second.display_role == "engineering_display"
    assert second.visibility_mode == "shared"
    assert second.panel_id == "panel_simulation_skill_overview"

    assert last.route_request_id == "displayroute_show_monitoring_001"
    assert last.display_role == "primary_dashboard_display"
    assert last.visibility_mode == "shared"
    assert last.panel_id == "panel_monitoring_panel"


def test_presentation_display_metrics_contract_preserves_explanation_and_registry_flags() -> None:
    """Presentation/display metrics should preserve explanation and registry flags."""
    contract = build_presentation_display_metrics_contract()

    for entry in contract.entries:
        assert entry.explanation_bound is True
        assert entry.multilingual_ready is True
        assert entry.registry_routed is True
        assert entry.event_severity == "info"
        assert entry.alert_emitted is False
