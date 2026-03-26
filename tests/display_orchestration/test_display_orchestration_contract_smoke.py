from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)


def test_display_orchestration_contract_builds() -> None:
    """Display orchestration contract should build successfully."""
    contract = build_display_orchestration_contract()

    assert contract.total_entries == 3
    assert contract.explanation_required_entries == 3
    assert contract.registry_routed_entries == 3
    assert contract.multilingual_ready_entries == 3


def test_display_orchestration_contract_contains_expected_routes() -> None:
    """Display orchestration contract should expose expected routed intents."""
    contract = build_display_orchestration_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.route_request_id == "displayroute_show_memory_001"
    assert first.command_intent == "show_memory"
    assert first.resolved_view_id == "view_memory_project_architecture"
    assert first.selected_display_role == "mobile_display_proxy"
    assert first.selected_panel_id == "panel_memory_project_architecture"

    assert second.route_request_id == "displayroute_show_simulation_001"
    assert second.command_intent == "show_simulation"
    assert second.resolved_view_id == "view_simulation_skill_overview"
    assert second.selected_display_role == "engineering_display"
    assert second.selected_panel_id == "panel_simulation_skill_overview"

    assert last.route_request_id == "displayroute_show_monitoring_001"
    assert last.command_intent == "show_monitoring"
    assert last.resolved_view_id == "view_monitoring_panel"
    assert last.selected_display_role == "primary_dashboard_display"
    assert last.selected_panel_id == "panel_monitoring_panel"


def test_display_orchestration_contract_preserves_explainable_and_multilingual_flags() -> None:
    """Display orchestration contract should preserve explainability and multilingual routing."""
    contract = build_display_orchestration_contract()

    for entry in contract.entries:
        assert entry.explanation_required is True
        assert entry.registry_routed is True
        assert entry.multilingual_ready is True
        assert entry.route_status == "routed"
