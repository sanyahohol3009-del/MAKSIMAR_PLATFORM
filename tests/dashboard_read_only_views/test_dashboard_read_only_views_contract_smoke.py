from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_contract,
)


def test_dashboard_read_only_views_contract_builds() -> None:
    """Dashboard read-only views contract should build successfully."""

    contract = build_dashboard_read_only_views_contract()
    memory_registry_views = build_memory_registry_view_contract()

    assert contract.total_entries == 2 + memory_registry_views.total_views
    assert contract.active_entries == contract.total_entries
    assert contract.multilingual_ready_entries == contract.total_entries
    assert contract.explanation_available_entries == contract.total_entries


def test_dashboard_read_only_views_contract_contains_expected_memory_view() -> None:
    """Dashboard read-only views contract should expose expected memory dashboard view."""

    contract = build_dashboard_read_only_views_contract()
    entry = contract.entries[0]

    assert entry.view_entry_id == "dashboardview_memory_project_architecture"
    assert entry.view_kind == "memory_dashboard_view"
    assert entry.view_id == "view_memory_project_architecture"
    assert entry.linked_memory_tier_id == "memory_project_architecture"
    assert entry.linked_skill_id == ""
    assert entry.display_role == "mobile_display_proxy"
    assert entry.panel_id == "panel_memory_project_architecture"


def test_dashboard_read_only_views_contract_contains_expected_skill_view() -> None:
    """Dashboard read-only views contract should expose expected skill dashboard view."""

    contract = build_dashboard_read_only_views_contract()
    entry = contract.entries[1]

    assert entry.view_entry_id == "dashboardview_skill_simulation_analysis"
    assert entry.view_kind == "skill_dashboard_view"
    assert entry.view_id == "view_simulation_skill_overview"
    assert entry.linked_memory_tier_id == ""
    assert entry.linked_skill_id == "skill_simulation_simulation_analysis"
    assert entry.display_role == "engineering_display"
    assert entry.panel_id == "panel_simulation_skill_overview"


def test_dashboard_read_only_views_contract_preserves_read_only_and_explanation_flags() -> None:
    """Dashboard read-only views should preserve read-only and explanation semantics."""

    contract = build_dashboard_read_only_views_contract()

    for entry in contract.entries:
        assert entry.read_only_mode == "read_only"
        assert entry.multilingual_ready is True
        assert entry.explanation_available is True
        assert entry.active is True
