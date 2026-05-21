from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


FoundationLayerId = Literal[
    "root_artifact_hygiene",
    "security_layer",
    "data_plane",
    "update_recovery_infra",
    "network_containerization",
    "ai_orchestration",
    "foundation_registry_enrollment",
]

FOUNDATION_LAYER_IDS: tuple[FoundationLayerId, ...] = (
    "root_artifact_hygiene",
    "security_layer",
    "data_plane",
    "update_recovery_infra",
    "network_containerization",
    "ai_orchestration",
    "foundation_registry_enrollment",
)

_LAYER_METADATA: dict[FoundationLayerId, tuple[str, str, str, int]] = {
    "root_artifact_hygiene": (
        "Root Artifact Hygiene",
        "MAKSIMAR_CORE_LIB/root_artifact_hygiene",
        "PHASE_0_ROOT_ARTIFACT_HYGIENE",
        0,
    ),
    "security_layer": (
        "Security Layer",
        "MAKSIMAR_CORE_LIB/security_layer",
        "PHASE_1_SECURITY_LAYER",
        1,
    ),
    "data_plane": (
        "Data Plane",
        "MAKSIMAR_CORE_LIB/data_plane",
        "PHASE_2_DATA_PLANE",
        2,
    ),
    "update_recovery_infra": (
        "Update Recovery Infrastructure",
        "MAKSIMAR_CORE_LIB/update_recovery",
        "PHASE_3_UPDATE_RECOVERY_INFRA",
        3,
    ),
    "network_containerization": (
        "Network Containerization",
        "MAKSIMAR_CORE_LIB/network_containerization",
        "PHASE_4_NETWORK_CONTAINERIZATION",
        4,
    ),
    "ai_orchestration": (
        "AI Orchestration",
        "MAKSIMAR_CORE_LIB/ai_orchestration",
        "PHASE_5_AI_ORCHESTRATION",
        5,
    ),
    "foundation_registry_enrollment": (
        "Foundation Registry Enrollment",
        "MAKSIMAR_CORE_LIB/foundation_registry_enrollment",
        "PHASE_6_FOUNDATION_REGISTRY_ENROLLMENT",
        6,
    ),
}


@dataclass(frozen=True, slots=True)
class FoundationLayerManifestModel:
    layer_id: FoundationLayerId
    title: str
    canonical_path: str
    phase_id: str
    foundation_sequence: int
    registry_enrollment_required: bool
    closed_before_registry_enrollment: bool
    runtime_mutation_allowed: bool
    registry_write_allowed: bool
    auto_enrollment_write_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.layer_id not in FOUNDATION_LAYER_IDS:
            raise ValueError(f"unknown foundation layer id: {self.layer_id}")
        _validate_non_empty("title", self.title)
        _validate_non_empty("canonical_path", self.canonical_path)
        _validate_non_empty("phase_id", self.phase_id)
        if not isinstance(self.foundation_sequence, int):
            raise TypeError("foundation_sequence must be an integer")
        if self.foundation_sequence < 0:
            raise ValueError("foundation_sequence must be non-negative")

        _validate_true("registry_enrollment_required", self.registry_enrollment_required)
        _validate_true("closed_before_registry_enrollment", self.closed_before_registry_enrollment)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("auto_enrollment_write_allowed", self.auto_enrollment_write_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "title": self.title,
            "canonical_path": self.canonical_path,
            "phase_id": self.phase_id,
            "foundation_sequence": self.foundation_sequence,
            "registry_enrollment_required": self.registry_enrollment_required,
            "closed_before_registry_enrollment": self.closed_before_registry_enrollment,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "registry_write_allowed": self.registry_write_allowed,
            "auto_enrollment_write_allowed": self.auto_enrollment_write_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_foundation_layer_manifest_model(
    layer_id: FoundationLayerId = "root_artifact_hygiene",
) -> FoundationLayerManifestModel:
    title, canonical_path, phase_id, foundation_sequence = _LAYER_METADATA[layer_id]
    return FoundationLayerManifestModel(
        layer_id=layer_id,
        title=title,
        canonical_path=canonical_path,
        phase_id=phase_id,
        foundation_sequence=foundation_sequence,
        registry_enrollment_required=True,
        closed_before_registry_enrollment=True,
        runtime_mutation_allowed=False,
        registry_write_allowed=False,
        auto_enrollment_write_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "foundation_layer_manifest_declared",
            "registry_enrollment_required",
            "read_model_only",
        ),
    )


def build_default_foundation_layer_manifests() -> tuple[FoundationLayerManifestModel, ...]:
    return tuple(build_foundation_layer_manifest_model(layer_id) for layer_id in FOUNDATION_LAYER_IDS)


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
