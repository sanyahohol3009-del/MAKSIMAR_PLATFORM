from __future__ import annotations

from MAKSIMAR_CORE_LIB.module_manifest import (
    ModuleManifestEntry,
)


def test_module_manifest_extension_fields_smoke() -> None:
    entry = ModuleManifestEntry(
        module_kind="skill",
        module_slug="robotics_motion",
        display_name="Robotics Motion",
        domain_class="robotics",
        input_contract_ids=("robotics_motion_request",),
        output_contract_ids=("robotics_motion_result",),
        policy_profile="sandbox_required",
        observability_profile="extended",
        dashboard_view_ids=("view_robotics_motion",),
        supported_display_roles=("engineering_display", "primary_dashboard_display"),
        explanation_available=True,
        multi_display_allowed=True,
        engine_adapter_required=True,
        supported_languages=("en", "de"),
        supported_scripts=("Latin",),
        active=True,
        storage_profile="artifact_reference",
        retrieval_profile="hybrid_retrieval",
        required_memory_tier_ids=("memory_project_architecture",),
        required_skill_ids=("skill_simulation_analysis",),
        enrollment_allowed=True,
        dashboard_exposure_allowed=True,
    )

    assert entry.storage_profile == "artifact_reference"
    assert entry.retrieval_profile == "hybrid_retrieval"
    assert entry.required_memory_tier_ids == ("memory_project_architecture",)
    assert entry.required_skill_ids == ("skill_simulation_analysis",)
    assert entry.enrollment_allowed is True
    assert entry.dashboard_exposure_allowed is True
