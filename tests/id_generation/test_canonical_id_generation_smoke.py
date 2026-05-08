from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    CanonicalIdAllocationEntry,
    build_canonical_id_generation_contract,
)


def _entries_by_slug() -> dict[str, CanonicalIdAllocationEntry]:
    contract = build_canonical_id_generation_contract()
    return {entry.module_slug: entry for entry in contract.entries}


def test_canonical_id_generation_contract_builds() -> None:
    """Canonical ID generation contract should build with consistent counts."""
    contract = build_canonical_id_generation_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.total_skill_ids == sum(
        1 for entry in contract.entries if entry.skill_id
    )
    assert contract.total_memory_tier_ids == sum(
        1 for entry in contract.entries if entry.memory_tier_id
    )
    assert contract.total_worker_ids == sum(
        1 for entry in contract.entries if entry.worker_id
    )
    assert contract.total_storage_node_ids == sum(
        1 for entry in contract.entries if entry.storage_node_id
    )
    assert contract.total_retrieval_source_ids == sum(
        1 for entry in contract.entries if entry.retrieval_source_id
    )
    assert contract.total_panel_ids == sum(
        len(entry.panel_ids) for entry in contract.entries
    )


def test_canonical_id_generation_contract_contains_expected_simulation_entry() -> None:
    """Canonical ID generation should preserve the accepted simulation entry."""
    entries = _entries_by_slug()
    first = entries["simulation_analysis"]

    assert first.module_id == "module_skill_simulation_analysis"
    assert first.skill_id == "skill_simulation_simulation_analysis"
    assert first.worker_id == "worker_simulation_analysis_001"
    assert first.storage_node_id == "storage_node_simulation_analysis"
    assert first.panel_ids == ("panel_simulation_skill_overview",)


def test_canonical_id_generation_contract_contains_expected_memory_entry() -> None:
    """Canonical ID generation should preserve the accepted memory tier entry."""
    entries = _entries_by_slug()
    memory_entry = entries["project_architecture"]

    assert memory_entry.module_id == "module_memory_tier_project_architecture"
    assert memory_entry.memory_tier_id == "memory_project_architecture"
    assert memory_entry.worker_id == ""
    assert memory_entry.storage_node_id == "storage_node_project_architecture"
    assert memory_entry.panel_ids == ("panel_memory_project_architecture",)


def test_canonical_id_generation_contract_contains_expected_cube_entry() -> None:
    """Canonical ID generation should preserve the accepted extension cube entry."""
    entries = _entries_by_slug()
    cube_entry = entries["monitoring_panel"]

    assert cube_entry.module_id == "module_extension_cube_monitoring_panel"
    assert cube_entry.skill_id == ""
    assert cube_entry.memory_tier_id == ""
    assert cube_entry.worker_id == ""
    assert cube_entry.storage_node_id == "storage_node_monitoring_panel"
    assert cube_entry.panel_ids == ("panel_monitoring_panel",)


def test_canonical_id_generation_contract_preserves_artifact_and_trace_prefixes() -> None:
    """Canonical ID generation should preserve artifact and trace prefixes."""
    contract = build_canonical_id_generation_contract()

    for entry in contract.entries:
        assert entry.artifact_ref_prefix == f"artifact://modules/{entry.module_slug}"
        assert entry.trace_id_prefix == f"trace_{entry.module_slug}"
        assert entry.collision_free is True
