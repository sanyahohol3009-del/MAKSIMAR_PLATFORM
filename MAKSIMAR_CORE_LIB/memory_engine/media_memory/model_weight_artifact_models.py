from __future__ import annotations

import re
from dataclasses import dataclass


_MODEL_ARTIFACT_ID_PATTERN = re.compile(r"^model_weight_[a-z][a-z0-9_]*$")


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
class ModelWeightArtifactMemory:
    """Metadata reference for model weights/checkpoints."""

    model_weight_id: str
    model_family: str
    model_role: str
    weight_artifact_ref: str
    model_store_id: str
    binary_external: bool
    checksum_required: bool
    license_review_required: bool

    def __post_init__(self) -> None:
        model_weight_id = _ensure_non_empty_str(
            self.model_weight_id,
            "model_weight_id",
        )
        model_family = _ensure_non_empty_str(self.model_family, "model_family")
        model_role = _ensure_non_empty_str(self.model_role, "model_role")
        weight_artifact_ref = _ensure_non_empty_str(
            self.weight_artifact_ref,
            "weight_artifact_ref",
        )
        model_store_id = _ensure_non_empty_str(self.model_store_id, "model_store_id")

        if not _MODEL_ARTIFACT_ID_PATTERN.fullmatch(model_weight_id):
            raise ValueError(f"Invalid model_weight_id: {model_weight_id}")

        for field_name in (
            "binary_external",
            "checksum_required",
            "license_review_required",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.binary_external:
            raise ValueError("binary_external must be True for model weights")
        if not self.checksum_required:
            raise ValueError("checksum_required must be True")

        object.__setattr__(self, "model_weight_id", model_weight_id)
        object.__setattr__(self, "model_family", model_family)
        object.__setattr__(self, "model_role", model_role)
        object.__setattr__(self, "weight_artifact_ref", weight_artifact_ref)
        object.__setattr__(self, "model_store_id", model_store_id)
