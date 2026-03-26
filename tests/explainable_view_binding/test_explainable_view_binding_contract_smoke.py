from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_view_binding_contract,
)


def test_explainable_view_binding_contract_builds() -> None:
    """Explainable view binding contract should build successfully."""
    contract = build_explainable_view_binding_contract()

    assert contract.total_entries == 3
    assert contract.multilingual_ready_entries == 3
    assert contract.explanation_text_entries == 3
    assert contract.explanation_payload_entries == 3


def test_explainable_view_binding_contract_contains_expected_bindings() -> None:
    """Explainable view binding contract should expose expected view bindings."""
    contract = build_explainable_view_binding_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.view_id == "view_memory_project_architecture"
    assert first.panel_id == "panel_memory_project_architecture"
    assert first.display_role == "mobile_display_proxy"

    assert second.view_id == "view_simulation_skill_overview"
    assert second.panel_id == "panel_simulation_skill_overview"
    assert second.display_role == "engineering_display"

    assert last.view_id == "view_monitoring_panel"
    assert last.panel_id == "panel_monitoring_panel"
    assert last.display_role == "primary_dashboard_display"


def test_explainable_view_binding_contract_preserves_explanation_flags() -> None:
    """Explainable view binding contract should preserve explanation flags."""
    contract = build_explainable_view_binding_contract()

    for entry in contract.entries:
        assert entry.summary_mode == "summary_available"
        assert entry.reasoning_mode == "reasoning_payload_available"
        assert entry.safety_mode == "safety_note_available"
        assert entry.multilingual_ready is True
        assert entry.explanation_text_available is True
        assert entry.explanation_payload_available is True
        assert entry.binding_status == "bound"
