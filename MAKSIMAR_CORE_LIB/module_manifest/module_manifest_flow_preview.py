from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.module_manifest.module_manifest_schema import (
    ModuleManifestEntry,
    ModuleManifestSchemaContract,
    build_module_manifest_schema_contract,
)


_MANIFEST_FLOW: Tuple[str, ...] = (
    "manifest_schema",
    "canonical_id_generation",
    "registry_auto_enrollment",
    "dashboard_read_only_exposure",
)


def _entry_to_preview(entry: ModuleManifestEntry) -> Dict[str, object]:
    """Build deterministic read-only preview for one manifest entry."""
    return {
        "module_kind": entry.module_kind,
        "module_slug": entry.module_slug,
        "display_name": entry.display_name,
        "domain_class": entry.domain_class,
        "storage_profile": entry.storage_profile,
        "retrieval_profile": entry.retrieval_profile,
        "required_memory_tier_ids": entry.required_memory_tier_ids,
        "required_skill_ids": entry.required_skill_ids,
        "enrollment_allowed": entry.enrollment_allowed,
        "dashboard_exposure_allowed": entry.dashboard_exposure_allowed,
        "dashboard_view_ids": entry.dashboard_view_ids,
        "supported_display_roles": entry.supported_display_roles,
        "explanation_available": entry.explanation_available,
        "manifest_flow": _MANIFEST_FLOW,
    }


def build_module_manifest_flow_preview(
    contract: ModuleManifestSchemaContract | None = None,
) -> Dict[str, object]:
    """Build read-only flow preview for manifest-driven enrollment.

    This preview does not write manifests, does not enroll modules and does not
    mutate registry state. It only shows the expected connection path.
    """
    selected_contract = contract or build_module_manifest_schema_contract()

    return {
        "schema_version": selected_contract.schema_version,
        "total_manifests": selected_contract.total_manifests,
        "flow": _MANIFEST_FLOW,
        "entries": tuple(_entry_to_preview(entry) for entry in selected_contract.manifests),
        "preview_ready": True,
    }
