from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_contract,
)


def test_registry_auto_enrollment_contract_builds() -> None:
    """Registry auto-enrollment contract should build successfully."""
    contract = build_registry_auto_enrollment_contract()

    assert contract.total_entries == 3
    assert contract.enrolled_entries == 3
    assert contract.skill_registry_entries == 1
    assert contract.memory_registry_entries == 1
    assert contract.dashboard_registry_entries == 1


def test_registry_auto_enrollment_contract_contains_expected_targets() -> None:
    """Registry auto-enrollment should expose expected registry targets."""
    contract = build_registry_auto_enrollment_contract()

    first = contract.entries[0]
    second = contract.entries[1]
    last = contract.entries[-1]

    assert first.module_slug == "simulation_analysis"
    assert first.enrollment_target == "skill_registry"
    assert first.skill_id == "skill_simulation_simulation_analysis"

    assert second.module_slug == "project_architecture"
    assert second.enrollment_target == "memory_registry"
    assert second.memory_tier_id == "memory_project_architecture"

    assert last.module_slug == "monitoring_panel"
    assert last.enrollment_target == "dashboard_registry"
    assert last.panel_ids == ("panel_monitoring_panel",)


def test_registry_auto_enrollment_contract_preserves_enrolled_status() -> None:
    """Registry auto-enrollment should keep active manifests enrolled."""
    contract = build_registry_auto_enrollment_contract()

    for entry in contract.entries:
        assert entry.active is True
        assert entry.enrollment_status == "enrolled"
