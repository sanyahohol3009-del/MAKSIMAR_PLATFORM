from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.existing_domain_inventory import (
    ExistingDomainInventoryContract,
    build_existing_domain_inventory,
)


ExistingDomainManifestKind = Literal["extension_cube"]
ExistingDomainStorageProfile = Literal["portable_storage"]
ExistingDomainRetrievalProfile = Literal["metadata_retrieval"]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class ExistingDomainMinimalManifestPreview:
    """Read-only minimal manifest preview for an existing domain."""

    module_kind: ExistingDomainManifestKind
    module_slug: str
    source_path: str
    storage_profile: ExistingDomainStorageProfile
    retrieval_profile: ExistingDomainRetrievalProfile
    storage_node_id: str
    retrieval_source_id: str
    dashboard_exposure_id: str
    observability_binding_id: str
    manifest_ready: bool

    def __post_init__(self) -> None:
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        retrieval_source_id = _ensure_non_empty_str(
            self.retrieval_source_id,
            "retrieval_source_id",
        )
        dashboard_exposure_id = _ensure_non_empty_str(
            self.dashboard_exposure_id,
            "dashboard_exposure_id",
        )
        observability_binding_id = _ensure_non_empty_str(
            self.observability_binding_id,
            "observability_binding_id",
        )

        if not isinstance(self.manifest_ready, bool):
            raise ValueError("manifest_ready must be bool")
        if not self.manifest_ready:
            raise ValueError("manifest_ready must be True")

        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "retrieval_source_id", retrieval_source_id)
        object.__setattr__(self, "dashboard_exposure_id", dashboard_exposure_id)
        object.__setattr__(self, "observability_binding_id", observability_binding_id)


@dataclass(frozen=True, slots=True)
class ExistingDomainMinimalManifestContract:
    """Contract for read-only existing-domain manifest previews."""

    total_entries: int
    entries: tuple[ExistingDomainMinimalManifestPreview, ...]

    def __post_init__(self) -> None:
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")
        slugs = tuple(entry.module_slug for entry in self.entries)
        if len(set(slugs)) != len(slugs):
            raise ValueError("Duplicate module_slug values detected")


def build_existing_domain_minimal_manifest_contract(
    inventory: ExistingDomainInventoryContract | None = None,
) -> ExistingDomainMinimalManifestContract:
    """Build minimal manifest previews for existing domains without writing files."""
    selected_inventory = inventory or build_existing_domain_inventory()

    entries = tuple(
        ExistingDomainMinimalManifestPreview(
            module_kind="extension_cube",
            module_slug=entry.domain_slug,
            source_path=entry.source_path,
            storage_profile="portable_storage",
            retrieval_profile="metadata_retrieval",
            storage_node_id=entry.storage_node_id,
            retrieval_source_id=entry.retrieval_source_id,
            dashboard_exposure_id=entry.dashboard_exposure_id,
            observability_binding_id=entry.observability_binding_id,
            manifest_ready=True,
        )
        for entry in selected_inventory.entries
    )

    return ExistingDomainMinimalManifestContract(
        total_entries=len(entries),
        entries=entries,
    )
