from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ProjectOutputKind = Literal[
    "cad_file",
    "stl_file",
    "step_file",
    "cnc_toolpath",
    "robotics_artifact",
    "simulation_output",
    "image_to_3d_proposal",
]


_OUTPUT_ID_PATTERN = re.compile(r"^project_output_[a-z][a-z0-9_]*$")


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
class ProjectOutputArtifactMemory:
    """Metadata reference for CAD/3D/CNC/robotics/simulation outputs."""

    project_output_id: str
    output_kind: ProjectOutputKind
    artifact_ref: str
    source_ref: str
    validation_ref: str
    geometry_validation_required: bool
    simulation_recommended: bool
    manufacturing_authority_granted: bool

    def __post_init__(self) -> None:
        project_output_id = _ensure_non_empty_str(
            self.project_output_id,
            "project_output_id",
        )
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")
        source_ref = _ensure_non_empty_str(self.source_ref, "source_ref")
        validation_ref = _ensure_non_empty_str(self.validation_ref, "validation_ref")

        if not _OUTPUT_ID_PATTERN.fullmatch(project_output_id):
            raise ValueError(f"Invalid project_output_id: {project_output_id}")

        for field_name in (
            "geometry_validation_required",
            "simulation_recommended",
            "manufacturing_authority_granted",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.geometry_validation_required:
            raise ValueError("geometry_validation_required must be True")
        if self.manufacturing_authority_granted:
            raise ValueError(
                "media memory cannot grant manufacturing authority"
            )

        object.__setattr__(self, "project_output_id", project_output_id)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "validation_ref", validation_ref)
