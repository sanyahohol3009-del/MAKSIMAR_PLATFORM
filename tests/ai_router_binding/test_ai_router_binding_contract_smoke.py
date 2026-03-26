from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.ai_router_binding import (
    build_ai_router_memory_skill_binding_contract,
)


def test_ai_router_memory_skill_binding_contract_builds() -> None:
    """AI router memory/skill binding contract should build successfully."""
    contract = build_ai_router_memory_skill_binding_contract()

    assert contract.total_entries == 3
    assert contract.active_entries == 3
    assert contract.explanation_ready_entries == 3
    assert contract.policy_compatible_entries == 3


def test_ai_router_memory_skill_binding_contract_contains_expected_routes() -> None:
    """AI router memory/skill binding should expose expected routes."""
    contract = build_ai_router_memory_skill_binding_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.route_request_id == "route_architecture_decision_001"
    assert first.requested_fact_class == "architecture_decision"
    assert first.selected_skill_id == "skill_simulation_simulation_analysis"
    assert first.selected_memory_tier_id == "memory_project_architecture"

    assert second.route_request_id == "route_platform_invariant_001"
    assert second.requested_fact_class == "platform_invariant"
    assert second.requested_language_code == "de"
    assert second.requested_script_name == "Latin"

    assert last.route_request_id == "route_roadmap_checkpoint_001"
    assert last.requested_fact_class == "roadmap_checkpoint"
    assert last.requested_language_code == "en"
    assert last.selected_panel_id == "panel_simulation_skill_overview"


def test_ai_router_memory_skill_binding_contract_preserves_binding_mode_and_status() -> None:
    """AI router memory/skill binding should preserve binding semantics."""
    contract = build_ai_router_memory_skill_binding_contract()

    for entry in contract.entries:
        assert entry.route_mode == "skill_plus_memory"
        assert entry.route_status == "bound"
        assert entry.policy_compatible is True
        assert entry.explanation_available is True
        assert entry.active is True
