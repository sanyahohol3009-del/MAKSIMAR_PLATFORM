from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_generation_contract,
)


def test_canonical_id_generation_contract_builds() -> None:
    """Canonical ID generation contract should build successfully."""
    contract = build_canonical_id_generation_contract()

    assert contract.total_entries == 3
    assert contract.total_skill_ids == 1
    assert contract.total_memory_tier_ids == 1
    assert contract.total_worker_ids == 1
    assert contract.total_panel_ids == 3


def test_canonical_id_generation_contract_contains_expected_ids() -> None:
    """Canonical ID generation contract should expose expected IDs."""
    contract = build_canonical_id_generation_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.module_id == "module_skill_simulation_analysis"
    assert first.skill_id == "skill_simulation_simulation_analysis"
    assert first.worker_id == "worker_simulation_analysis_001"
    assert first.panel_ids == ("panel_simulation_skill_overview",)

    assert second.module_id == "module_memory_tier_project_architecture"
    assert second.memory_tier_id == "memory_project_architecture"
    assert second.worker_id == ""
    assert second.panel_ids == ("panel_memory_project_architecture",)

    assert last.module_id == "module_extension_cube_monitoring_panel"
    assert last.skill_id == ""
    assert last.memory_tier_id == ""
    assert last.worker_id == ""
    assert last.panel_ids == ("panel_monitoring_panel",)


def test_canonical_id_generation_contract_preserves_artifact_and_trace_prefixes() -> None:
    """Canonical ID generation contract should preserve artifact and trace prefixes."""
    contract = build_canonical_id_generation_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.artifact_ref_prefix == "artifact://modules/simulation_analysis"
    assert first.trace_id_prefix == "trace_simulation_analysis"
    assert first.collision_free is True

    assert second.artifact_ref_prefix == "artifact://modules/project_architecture"
    assert second.trace_id_prefix == "trace_project_architecture"
    assert second.collision_free is True

    assert last.artifact_ref_prefix == "artifact://modules/monitoring_panel"
    assert last.trace_id_prefix == "trace_monitoring_panel"
    assert last.collision_free is True
