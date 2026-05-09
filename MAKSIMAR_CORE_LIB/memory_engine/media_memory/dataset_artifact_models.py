from __future__ import annotations

import re
from dataclasses import dataclass


_DATASET_ID_PATTERN = re.compile(r"^dataset_artifact_[a-z][a-z0-9_]*$")


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
class DatasetArtifactMemory:
    """Metadata reference for imported datasets."""

    dataset_artifact_id: str
    dataset_ref: str
    source_type: str
    provenance_ref: str
    imported_dataset: bool
    review_required_before_trust: bool
    retrieval_index_allowed: bool

    def __post_init__(self) -> None:
        dataset_artifact_id = _ensure_non_empty_str(
            self.dataset_artifact_id,
            "dataset_artifact_id",
        )
        dataset_ref = _ensure_non_empty_str(self.dataset_ref, "dataset_ref")
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        provenance_ref = _ensure_non_empty_str(self.provenance_ref, "provenance_ref")

        if not _DATASET_ID_PATTERN.fullmatch(dataset_artifact_id):
            raise ValueError(f"Invalid dataset_artifact_id: {dataset_artifact_id}")

        for field_name in (
            "imported_dataset",
            "review_required_before_trust",
            "retrieval_index_allowed",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.imported_dataset and not self.review_required_before_trust:
            raise ValueError(
                "imported datasets require review before becoming trusted examples"
            )

        object.__setattr__(self, "dataset_artifact_id", dataset_artifact_id)
        object.__setattr__(self, "dataset_ref", dataset_ref)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "provenance_ref", provenance_ref)
