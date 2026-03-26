from __future__ import annotations

from MAKSIMAR_CORE_LIB.module_manifest import (
    build_module_manifest_schema_contract,
)


def test_module_manifest_schema_contract_builds() -> None:
    """Module manifest schema contract should build successfully."""
    contract = build_module_manifest_schema_contract()

    assert contract.schema_version == "1.0.0"
    assert contract.total_manifests == 3
    assert len(contract.manifests) == 3


def test_module_manifest_schema_contract_contains_expected_module_kinds() -> None:
    """Module manifest schema contract should expose expected module kinds."""
    contract = build_module_manifest_schema_contract()

    assert contract.manifests[0].module_kind == "skill"
    assert contract.manifests[1].module_kind == "memory_tier"
    assert contract.manifests[2].module_kind == "extension_cube"

    assert contract.manifests[0].module_slug == "simulation_analysis"
    assert contract.manifests[1].module_slug == "project_architecture"
    assert contract.manifests[2].module_slug == "monitoring_panel"


def test_module_manifest_schema_contract_preserves_extensibility_fields() -> None:
    """Module manifest schema should preserve multilingual and display metadata."""
    contract = build_module_manifest_schema_contract()

    skill = contract.manifests[0]
    memory_tier = contract.manifests[1]
    cube = contract.manifests[2]

    assert skill.engine_adapter_required is True
    assert skill.explanation_available is True
    assert skill.multi_display_allowed is True
    assert skill.supported_languages == ("en", "ru", "uk", "de")
    assert skill.supported_scripts == ("Latin", "Cyrillic")

    assert memory_tier.module_kind == "memory_tier"
    assert memory_tier.domain_class == "memory"
    assert memory_tier.engine_adapter_required is False
    assert memory_tier.policy_profile == "approval_required"

    assert cube.module_kind == "extension_cube"
    assert cube.policy_profile == "read_only"
    assert cube.engine_adapter_required is False
    assert cube.dashboard_view_ids == ("view_monitoring_panel",)
