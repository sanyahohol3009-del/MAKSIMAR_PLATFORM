from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_generation_contract,
)
from MAKSIMAR_CORE_LIB.module_manifest import (
    build_module_manifest_schema_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.registry_auto_enrollment_models import (
    RegistryAutoEnrollmentContract,
    RegistryAutoEnrollmentEntry,
)


def build_registry_auto_enrollment_contract() -> RegistryAutoEnrollmentContract:
    """Build registry auto-enrollment contract from manifest and canonical IDs."""
    manifest_contract = build_module_manifest_schema_contract()
    id_contract = build_canonical_id_generation_contract()

    manifest_by_slug = {
        entry.module_slug: entry for entry in manifest_contract.manifests
    }

    entries = []
    for id_entry in id_contract.entries:
        manifest_entry = manifest_by_slug[id_entry.module_slug]

        if manifest_entry.module_kind == "skill":
            enrollment_target = "skill_registry"
        elif manifest_entry.module_kind == "memory_tier":
            enrollment_target = "memory_registry"
        else:
            enrollment_target = "dashboard_registry"

        enrollment_status = "enrolled" if manifest_entry.active else "skipped_inactive"

        entries.append(
            RegistryAutoEnrollmentEntry(
                module_kind=manifest_entry.module_kind,
                module_slug=manifest_entry.module_slug,
                module_id=id_entry.module_id,
                enrollment_target=enrollment_target,  # type: ignore[arg-type]
                enrollment_status=enrollment_status,  # type: ignore[arg-type]
                skill_id=id_entry.skill_id,
                memory_tier_id=id_entry.memory_tier_id,
                panel_ids=id_entry.panel_ids,
                active=manifest_entry.active,
                description=(
                    f"Registry auto-enrollment for module_slug={manifest_entry.module_slug} "
                    f"into target={enrollment_target}."
                ),
            )
        )

    enrolled_entries = sum(
        1 for entry in entries if entry.enrollment_status == "enrolled"
    )
    skill_registry_entries = sum(
        1 for entry in entries if entry.enrollment_target == "skill_registry"
    )
    memory_registry_entries = sum(
        1 for entry in entries if entry.enrollment_target == "memory_registry"
    )
    dashboard_registry_entries = sum(
        1 for entry in entries if entry.enrollment_target == "dashboard_registry"
    )

    return RegistryAutoEnrollmentContract(
        total_entries=len(entries),
        enrolled_entries=enrolled_entries,
        skill_registry_entries=skill_registry_entries,
        memory_registry_entries=memory_registry_entries,
        dashboard_registry_entries=dashboard_registry_entries,
        entries=tuple(entries),
    )
