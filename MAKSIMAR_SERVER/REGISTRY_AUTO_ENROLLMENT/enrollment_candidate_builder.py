from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.existing_domain_inventory import (
    ExistingDomainInventoryContract,
    build_existing_domain_inventory,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.manifest_discovery import (
    ManifestDiscoveryContract,
    build_manifest_discovery_contract,
)


EnrollmentAction = Literal[
    "reuse_existing_manifest",
    "create_minimal_manifest_preview",
]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class EnrollmentCandidate:
    """Read-only candidate for registry auto-enrollment."""

    module_slug: str
    source_path: str
    manifest_path: str
    manifest_exists: bool
    enrollment_action: EnrollmentAction
    storage_node_id: str
    retrieval_source_id: str
    dashboard_exposure_id: str
    observability_binding_id: str
    candidate_ready: bool

    def __post_init__(self) -> None:
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        manifest_path = _ensure_non_empty_str(self.manifest_path, "manifest_path")
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

        if not isinstance(self.manifest_exists, bool):
            raise ValueError("manifest_exists must be bool")
        if not isinstance(self.candidate_ready, bool):
            raise ValueError("candidate_ready must be bool")
        if not self.candidate_ready:
            raise ValueError("candidate_ready must be True")
        if self.manifest_exists and self.enrollment_action != "reuse_existing_manifest":
            raise ValueError("existing manifest must use reuse_existing_manifest action")
        if (
            not self.manifest_exists
            and self.enrollment_action != "create_minimal_manifest_preview"
        ):
            raise ValueError(
                "missing manifest must use create_minimal_manifest_preview action"
            )

        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "manifest_path", manifest_path)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "retrieval_source_id", retrieval_source_id)
        object.__setattr__(self, "dashboard_exposure_id", dashboard_exposure_id)
        object.__setattr__(self, "observability_binding_id", observability_binding_id)


@dataclass(frozen=True, slots=True)
class EnrollmentCandidateContract:
    """Read-only enrollment candidate contract."""

    total_candidates: int
    reuse_existing_manifest_candidates: int
    create_minimal_manifest_preview_candidates: int
    candidates: tuple[EnrollmentCandidate, ...]

    def __post_init__(self) -> None:
        total_candidates = _ensure_non_negative_int(
            self.total_candidates,
            "total_candidates",
        )
        reuse_existing_manifest_candidates = _ensure_non_negative_int(
            self.reuse_existing_manifest_candidates,
            "reuse_existing_manifest_candidates",
        )
        create_minimal_manifest_preview_candidates = _ensure_non_negative_int(
            self.create_minimal_manifest_preview_candidates,
            "create_minimal_manifest_preview_candidates",
        )

        if total_candidates != len(self.candidates):
            raise ValueError("total_candidates must match candidates length")

        computed_reuse = sum(
            1
            for candidate in self.candidates
            if candidate.enrollment_action == "reuse_existing_manifest"
        )
        computed_create = sum(
            1
            for candidate in self.candidates
            if candidate.enrollment_action == "create_minimal_manifest_preview"
        )

        if reuse_existing_manifest_candidates != computed_reuse:
            raise ValueError(
                "reuse_existing_manifest_candidates must match computed count"
            )
        if create_minimal_manifest_preview_candidates != computed_create:
            raise ValueError(
                "create_minimal_manifest_preview_candidates must match computed count"
            )
        if total_candidates != computed_reuse + computed_create:
            raise ValueError("candidate counts must balance")

        slugs = tuple(candidate.module_slug for candidate in self.candidates)
        if len(set(slugs)) != len(slugs):
            raise ValueError("Duplicate module_slug values detected")

        object.__setattr__(self, "total_candidates", total_candidates)
        object.__setattr__(
            self,
            "reuse_existing_manifest_candidates",
            reuse_existing_manifest_candidates,
        )
        object.__setattr__(
            self,
            "create_minimal_manifest_preview_candidates",
            create_minimal_manifest_preview_candidates,
        )


def build_enrollment_candidate_contract(
    project_root: Path | None = None,
    inventory: ExistingDomainInventoryContract | None = None,
    discovery: ManifestDiscoveryContract | None = None,
) -> EnrollmentCandidateContract:
    """Build read-only enrollment candidates from inventory and discovery."""
    root = project_root or Path.cwd()
    selected_inventory = inventory or build_existing_domain_inventory(root)
    selected_discovery = discovery or build_manifest_discovery_contract(
        root,
        selected_inventory,
    )

    inventory_by_slug = {
        entry.domain_slug: entry
        for entry in selected_inventory.entries
    }

    candidates = tuple(
        EnrollmentCandidate(
            module_slug=discovery_entry.module_slug,
            source_path=discovery_entry.source_path,
            manifest_path=discovery_entry.manifest_path,
            manifest_exists=discovery_entry.manifest_exists,
            enrollment_action=(
                "reuse_existing_manifest"
                if discovery_entry.manifest_exists
                else "create_minimal_manifest_preview"
            ),
            storage_node_id=inventory_by_slug[discovery_entry.module_slug].storage_node_id,
            retrieval_source_id=inventory_by_slug[
                discovery_entry.module_slug
            ].retrieval_source_id,
            dashboard_exposure_id=inventory_by_slug[
                discovery_entry.module_slug
            ].dashboard_exposure_id,
            observability_binding_id=inventory_by_slug[
                discovery_entry.module_slug
            ].observability_binding_id,
            candidate_ready=True,
        )
        for discovery_entry in selected_discovery.entries
    )

    return EnrollmentCandidateContract(
        total_candidates=len(candidates),
        reuse_existing_manifest_candidates=sum(
            1
            for candidate in candidates
            if candidate.enrollment_action == "reuse_existing_manifest"
        ),
        create_minimal_manifest_preview_candidates=sum(
            1
            for candidate in candidates
            if candidate.enrollment_action == "create_minimal_manifest_preview"
        ),
        candidates=candidates,
    )
