from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MediaArtifactKind = Literal[
    "generated_image",
    "generated_video",
    "generated_audio",
    "thumbnail",
    "mask",
    "render_output",
    "dataset_asset",
    "model_weight",
    "cad_file",
    "stl_file",
    "step_file",
    "cnc_toolpath",
    "robotics_artifact",
    "simulation_output",
]


_ARTIFACT_ID_PATTERN = re.compile(r"^media_artifact_[a-z][a-z0-9_]*$")
_ARTIFACT_REF_PATTERN = re.compile(r"^artifact://[a-zA-Z0-9_./:-]+$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class MediaArtifactMemoryRecord:
    """Canonical metadata record for media/model/artifact memory.

    This record never stores binary payloads. It stores references, provenance,
    routing metadata and read-only dashboard/retrieval visibility.
    """

    artifact_id: str
    artifact_ref: str
    artifact_kind: MediaArtifactKind
    title: str
    source_ref: str
    storage_registry_id: str
    storage_node_id: str
    provenance_required: bool
    traceability_required: bool
    approval_required: bool
    binary_external: bool
    dashboard_visible: bool
    retrieval_visible: bool

    def __post_init__(self) -> None:
        artifact_id = _ensure_non_empty_str(self.artifact_id, "artifact_id")
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")
        title = _ensure_non_empty_str(self.title, "title")
        source_ref = _ensure_non_empty_str(self.source_ref, "source_ref")
        storage_registry_id = _ensure_non_empty_str(
            self.storage_registry_id,
            "storage_registry_id",
        )
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")

        if not _ARTIFACT_ID_PATTERN.fullmatch(artifact_id):
            raise ValueError(f"Invalid artifact_id: {artifact_id}")
        if not _ARTIFACT_REF_PATTERN.fullmatch(artifact_ref):
            raise ValueError(f"Invalid artifact_ref: {artifact_ref}")

        for field_name in (
            "provenance_required",
            "traceability_required",
            "approval_required",
            "binary_external",
            "dashboard_visible",
            "retrieval_visible",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.binary_external:
            raise ValueError("binary_external must be True for media memory records")

        object.__setattr__(self, "artifact_id", artifact_id)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "storage_registry_id", storage_registry_id)
        object.__setattr__(self, "storage_node_id", storage_node_id)
