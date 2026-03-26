from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_generation_contract,
)
from MAKSIMAR_CORE_LIB.module_manifest import (
    build_module_manifest_schema_contract,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY.memory_registry_models import (
    MemoryRegistryContract,
    MemoryRegistryEntry,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_contract,
)


def _resolve_retention_class(*, module_slug: str) -> str:
    """Resolve retention class for canonical memory tiers."""
    if module_slug == "project_architecture":
        return "foundational"
    return "operational"


def build_memory_registry_contract() -> MemoryRegistryContract:
    """Build canonical memory registry contract."""
    manifest_contract = build_module_manifest_schema_contract()
    id_contract = build_canonical_id_generation_contract()
    enrollment_contract = build_registry_auto_enrollment_contract()

    manifest_by_slug = {
        entry.module_slug: entry
        for entry in manifest_contract.manifests
        if entry.module_kind == "memory_tier"
    }
    id_by_slug = {
        entry.module_slug: entry
        for entry in id_contract.entries
        if entry.memory_tier_id != ""
    }
    enrolled_memory_slugs = {
        entry.module_slug
        for entry in enrollment_contract.entries
        if entry.enrollment_target == "memory_registry"
        and entry.enrollment_status == "enrolled"
    }

    entries = []
    for module_slug in sorted(enrolled_memory_slugs):
        manifest_entry = manifest_by_slug[module_slug]
        id_entry = id_by_slug[module_slug]

        entries.append(
            MemoryRegistryEntry(
                module_slug=module_slug,
                module_id=id_entry.module_id,
                memory_tier_id=id_entry.memory_tier_id,
                retention_class=_resolve_retention_class(module_slug=module_slug),  # type: ignore[arg-type]
                write_policy="approval_required",
                read_policy="scoped_read",
                evidence_required=True,
                conflict_resolution_required=True,
                explanation_available=manifest_entry.explanation_available,
                panel_ids=id_entry.panel_ids,
                supported_languages=manifest_entry.supported_languages,
                supported_scripts=manifest_entry.supported_scripts,
                active=manifest_entry.active,
                description=(
                    f"Memory registry entry for memory_tier={module_slug} "
                    f"with retention_class={_resolve_retention_class(module_slug=module_slug)}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    foundational_entries = sum(
        1 for entry in entries if entry.retention_class == "foundational"
    )
    approval_required_entries = sum(
        1 for entry in entries if entry.write_policy == "approval_required"
    )

    return MemoryRegistryContract(
        total_entries=len(entries),
        active_entries=active_entries,
        foundational_entries=foundational_entries,
        approval_required_entries=approval_required_entries,
        entries=tuple(entries),
    )
