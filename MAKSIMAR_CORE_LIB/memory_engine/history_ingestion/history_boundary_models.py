from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class HistoryCanonicalTruthSplit:
    """
    Explicitly formalizes that imported history is not canonical truth.
    """

    archive_is_supporting_source: bool
    canonical_truth_write_allowed: bool
    auto_promotion_allowed: bool

    def __post_init__(self) -> None:
        if not self.archive_is_supporting_source:
            raise ValueError("archive_is_supporting_source must be True")

        if self.canonical_truth_write_allowed:
            raise ValueError("canonical_truth_write_allowed must be False")

        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")


@dataclass(frozen=True)
class HistoryStoragePortabilityRequirement:
    """
    Storage layer must be portable for future external volume / NAS relocation.
    """

    portable_storage_required: bool
    hardcoded_absolute_paths_forbidden: bool
    future_nas_compatibility_required: bool

    def __post_init__(self) -> None:
        if not self.portable_storage_required:
            raise ValueError("portable_storage_required must be True")

        if not self.hardcoded_absolute_paths_forbidden:
            raise ValueError("hardcoded_absolute_paths_forbidden must be True")

        if not self.future_nas_compatibility_required:
            raise ValueError("future_nas_compatibility_required must be True")


@dataclass(frozen=True)
class HistoryBoundaryContract:
    """
    Top-level H0 boundary contract for the history-ingestion track.
    """

    boundary_id: str
    title: str
    owning_package: str
    truth_split: HistoryCanonicalTruthSplit
    storage_portability: HistoryStoragePortabilityRequirement
    multi_format_required: bool
    dedup_required_before_real_import: bool

    def __post_init__(self) -> None:
        boundary_id = _ensure_non_empty_str(self.boundary_id, "boundary_id")
        title = _ensure_non_empty_str(self.title, "title")
        owning_package = _ensure_non_empty_str(self.owning_package, "owning_package")

        if not self.multi_format_required:
            raise ValueError("multi_format_required must be True")

        if not self.dedup_required_before_real_import:
            raise ValueError("dedup_required_before_real_import must be True")

        object.__setattr__(self, "boundary_id", boundary_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "owning_package", owning_package)

    @property
    def preview_ready(self) -> bool:
        return (
            self.truth_split.archive_is_supporting_source
            and not self.truth_split.canonical_truth_write_allowed
            and self.storage_portability.portable_storage_required
            and self.multi_format_required
            and self.dedup_required_before_real_import
        )
