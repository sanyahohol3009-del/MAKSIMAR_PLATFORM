from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import (
    build_canonical_id_generation_contract,
)
from MAKSIMAR_CORE_LIB.module_manifest import (
    build_module_manifest_schema_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_contract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.skill_adapter_registry_models import (
    SkillAdapterRegistryContract,
    SkillAdapterRegistryEntry,
)


def _resolve_adapter_execution_mode(*, policy_profile: str) -> str:
    """Resolve adapter execution mode from policy profile."""
    if policy_profile == "sandbox_required":
        return "sandboxed"
    if policy_profile in ("approval_required", "execution_guarded"):
        return "guarded"
    return "read_only"


def build_skill_adapter_registry_contract() -> SkillAdapterRegistryContract:
    """Build canonical skill adapter registry contract."""
    manifest_contract = build_module_manifest_schema_contract()
    id_contract = build_canonical_id_generation_contract()
    enrollment_contract = build_registry_auto_enrollment_contract()

    manifest_by_slug = {
        entry.module_slug: entry
        for entry in manifest_contract.manifests
        if entry.module_kind == "skill"
    }
    id_by_slug = {
        entry.module_slug: entry
        for entry in id_contract.entries
        if entry.skill_id != ""
    }
    enrolled_skill_slugs = {
        entry.module_slug
        for entry in enrollment_contract.entries
        if entry.enrollment_target == "skill_registry"
        and entry.enrollment_status == "enrolled"
    }

    entries = []
    for module_slug in sorted(enrolled_skill_slugs):
        manifest_entry = manifest_by_slug[module_slug]
        id_entry = id_by_slug[module_slug]

        adapter_execution_mode = _resolve_adapter_execution_mode(
            policy_profile=manifest_entry.policy_profile
        )

        entries.append(
            SkillAdapterRegistryEntry(
                module_slug=module_slug,
                module_id=id_entry.module_id,
                skill_id=id_entry.skill_id,
                worker_id=id_entry.worker_id,
                domain_class=manifest_entry.domain_class,
                input_contract_ids=manifest_entry.input_contract_ids,
                output_contract_ids=manifest_entry.output_contract_ids,
                policy_profile=manifest_entry.policy_profile,
                observability_profile=manifest_entry.observability_profile,
                panel_ids=id_entry.panel_ids,
                supported_languages=manifest_entry.supported_languages,
                supported_scripts=manifest_entry.supported_scripts,
                engine_adapter_required=manifest_entry.engine_adapter_required,
                adapter_execution_mode=adapter_execution_mode,  # type: ignore[arg-type]
                registration_status="registered",
                active=manifest_entry.active,
                description=(
                    f"Skill adapter registry entry for module_slug={module_slug} "
                    f"with execution_mode={adapter_execution_mode}."
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.active)
    sandboxed_entries = sum(
        1 for entry in entries if entry.adapter_execution_mode == "sandboxed"
    )
    engine_adapter_entries = sum(
        1 for entry in entries if entry.engine_adapter_required
    )

    return SkillAdapterRegistryContract(
        total_entries=len(entries),
        active_entries=active_entries,
        sandboxed_entries=sandboxed_entries,
        engine_adapter_entries=engine_adapter_entries,
        entries=tuple(entries),
    )
