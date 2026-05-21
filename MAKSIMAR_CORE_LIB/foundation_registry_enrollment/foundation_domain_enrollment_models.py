from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
    FoundationLayerId,
    FoundationLayerManifestModel,
    build_foundation_layer_manifest_model,
)


_EXISTING_REGISTRY_REFS: dict[FoundationLayerId, tuple[str, ...]] = {
    "root_artifact_hygiene": (
        "MAKSIMAR_CORE_LIB/root_artifact_hygiene",
        "docs/architecture/foundation",
    ),
    "security_layer": (
        "MAKSIMAR_CORE_LIB/security_layer",
        "MAKSIMAR_SERVER/SECURITY_LAYER",
    ),
    "data_plane": (
        "MAKSIMAR_CORE_LIB/data_plane",
        "MAKSIMAR_SERVER/DATA_PLANE",
    ),
    "update_recovery_infra": (
        "MAKSIMAR_CORE_LIB/update_recovery",
        "MAKSIMAR_SERVER/UPDATE_RECOVERY",
    ),
    "network_containerization": (
        "MAKSIMAR_CORE_LIB/network_containerization",
        "NETWORK_SEGMENTATION",
        "CONTAINER_DEPLOYMENT",
    ),
    "ai_orchestration": (
        "MAKSIMAR_CORE_LIB/ai_orchestration",
        "AI_ORCHESTRATION",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION",
    ),
    "foundation_registry_enrollment": (
        "MAKSIMAR_CORE_LIB/foundation_registry_enrollment",
        "MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT",
    ),
}


@dataclass(frozen=True, slots=True)
class FoundationDomainEnrollmentModel:
    enrollment_id: str
    layer_manifest: FoundationLayerManifestModel
    registry_domain_id: FoundationLayerId
    registry_domain_title: str
    existing_registry_refs: tuple[str, ...]
    existing_registry_accounted: bool
    replaces_existing_registry: bool
    migrates_existing_registry: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("enrollment_id", self.enrollment_id)
        if not isinstance(self.layer_manifest, FoundationLayerManifestModel):
            raise TypeError("layer_manifest must be FoundationLayerManifestModel")
        if self.registry_domain_id not in FOUNDATION_LAYER_IDS:
            raise ValueError(f"unknown registry domain id: {self.registry_domain_id}")
        if self.registry_domain_id != self.layer_manifest.layer_id:
            raise ValueError("registry_domain_id must match layer_manifest.layer_id")
        _validate_non_empty("registry_domain_title", self.registry_domain_title)
        _validate_non_empty_tuple("existing_registry_refs", self.existing_registry_refs)

        _validate_true("existing_registry_accounted", self.existing_registry_accounted)
        _validate_false("replaces_existing_registry", self.replaces_existing_registry)
        _validate_false("migrates_existing_registry", self.migrates_existing_registry)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enrollment_id": self.enrollment_id,
            "layer_manifest": self.layer_manifest.to_dict(),
            "registry_domain_id": self.registry_domain_id,
            "registry_domain_title": self.registry_domain_title,
            "existing_registry_refs": self.existing_registry_refs,
            "existing_registry_accounted": self.existing_registry_accounted,
            "replaces_existing_registry": self.replaces_existing_registry,
            "migrates_existing_registry": self.migrates_existing_registry,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_foundation_domain_enrollment_model(
    layer_id: FoundationLayerId = "root_artifact_hygiene",
) -> FoundationDomainEnrollmentModel:
    layer_manifest = build_foundation_layer_manifest_model(layer_id)
    return FoundationDomainEnrollmentModel(
        enrollment_id=f"{layer_id}_domain_enrollment_v1",
        layer_manifest=layer_manifest,
        registry_domain_id=layer_id,
        registry_domain_title=layer_manifest.title,
        existing_registry_refs=_EXISTING_REGISTRY_REFS[layer_id],
        existing_registry_accounted=True,
        replaces_existing_registry=False,
        migrates_existing_registry=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "foundation_domain_enrollment_declared",
            "existing_registry_accounted",
            "no_registry_replacement",
        ),
    )


def build_default_foundation_domain_enrollments() -> tuple[FoundationDomainEnrollmentModel, ...]:
    return tuple(build_foundation_domain_enrollment_model(layer_id) for layer_id in FOUNDATION_LAYER_IDS)


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
