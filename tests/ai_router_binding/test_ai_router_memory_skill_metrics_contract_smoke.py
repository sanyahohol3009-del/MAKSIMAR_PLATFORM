from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)


def test_memory_skill_metrics_contract_builds() -> None:
    """Memory/skill metrics contract should build successfully."""
    contract = build_memory_skill_metrics_contract()

    assert contract.total_entries == 5
    assert contract.active_entries == 5
    assert contract.explanation_ready_entries == 5
    assert contract.policy_compatible_entries == 5
    assert contract.router_binding_entries == 3


def test_memory_skill_metrics_contract_contains_expected_registry_metrics() -> None:
    """Memory/skill metrics should expose registry-bound entries."""
    contract = build_memory_skill_metrics_contract()

    first = contract.entries[0]
    second = contract.entries[1]

    assert first.source_component == "memory_registry"
    assert first.module_slug == "project_architecture"
    assert first.linked_memory_tier_id == "memory_project_architecture"
    assert first.linked_panel_id == "panel_memory_project_architecture"

    assert second.source_component == "skill_adapter_registry"
    assert second.module_slug == "simulation_analysis"
    assert second.linked_skill_id == "skill_simulation_simulation_analysis"
    assert second.linked_worker_id == "worker_simulation_analysis_001"
    assert second.linked_panel_id == "panel_simulation_skill_overview"


def test_memory_skill_metrics_contract_contains_expected_router_metrics() -> None:
    """Memory/skill metrics should expose router binding entries."""
    contract = build_memory_skill_metrics_contract()

    third = contract.entries[2]
    last = contract.entries[-1]

    assert third.source_component == "ai_router_binding"
    assert third.route_request_id == "route_architecture_decision_001"
    assert third.linked_memory_tier_id == "memory_project_architecture"
    assert third.linked_skill_id == "skill_simulation_simulation_analysis"

    assert last.source_component == "ai_router_binding"
    assert last.route_request_id == "route_roadmap_checkpoint_001"
    assert last.linked_panel_id == "panel_simulation_skill_overview"
    assert last.multilingual_ready is True
