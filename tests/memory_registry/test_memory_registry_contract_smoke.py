from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)


def test_memory_registry_contract_builds() -> None:
    """Memory registry contract should build successfully."""
    contract = build_memory_registry_contract()

    assert contract.total_entries == 1
    assert contract.active_entries == 1
    assert contract.foundational_entries == 1
    assert contract.approval_required_entries == 1


def test_memory_registry_contract_contains_expected_entry() -> None:
    """Memory registry contract should expose expected memory tier."""
    contract = build_memory_registry_contract()
    entry = contract.entries[0]

    assert entry.module_slug == "project_architecture"
    assert entry.module_id == "module_memory_tier_project_architecture"
    assert entry.memory_tier_id == "memory_project_architecture"
    assert entry.retention_class == "foundational"
    assert entry.write_policy == "approval_required"
    assert entry.read_policy == "scoped_read"


def test_memory_registry_contract_preserves_multilingual_and_panel_metadata() -> None:
    """Memory registry contract should preserve multilingual and panel metadata."""
    contract = build_memory_registry_contract()
    entry = contract.entries[0]

    assert entry.evidence_required is True
    assert entry.conflict_resolution_required is True
    assert entry.explanation_available is True
    assert entry.panel_ids == ("panel_memory_project_architecture",)
    assert entry.supported_languages == ("en", "ru", "uk", "de")
    assert entry.supported_scripts == ("Latin", "Cyrillic")
