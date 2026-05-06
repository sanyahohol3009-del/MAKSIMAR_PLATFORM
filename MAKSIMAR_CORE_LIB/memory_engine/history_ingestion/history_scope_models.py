from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Tuple


HistoryAllowedSourceType = Literal[
    "html",
    "pdf",
    "txt",
    "md",
    "json",
]

HistoryRequiredCapability = Literal[
    "multi_format_source_contract",
    "dedup_before_real_import",
    "supporting_source_only",
    "portable_storage",
    "jarvis_read_target",
    "preview_traceability",
]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_unique_sorted_tuple(
    values: Tuple[str, ...],
    field_name: str,
) -> Tuple[str, ...]:
    if not values:
        raise ValueError(f"{field_name} must not be empty")

    normalized = tuple(v.strip() for v in values)
    if any(not v for v in normalized):
        raise ValueError(f"{field_name} must not contain empty values")

    unique_values = tuple(dict.fromkeys(normalized))
    if len(unique_values) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")

    return unique_values


@dataclass(frozen=True)
class HistoryIngestionScope:
    """
    Defines the allowed scope of the project-history ingestion track.

    This scope is intentionally strict:
    - history archive is not canonical truth
    - ingestion is a supporting source for future inspector/drift use
    - multi-format import support is required
    - dedup must happen before real imports are considered safe
    """

    track_name: str
    owning_domain: str
    package_path: str
    supported_source_types: Tuple[HistoryAllowedSourceType, ...]
    required_capabilities: Tuple[HistoryRequiredCapability, ...]
    supporting_source_only: bool
    canonical_truth_write_allowed: bool
    real_data_import_allowed: bool

    def __post_init__(self) -> None:
        track_name = _ensure_non_empty_str(self.track_name, "track_name")
        owning_domain = _ensure_non_empty_str(self.owning_domain, "owning_domain")
        package_path = _ensure_non_empty_str(self.package_path, "package_path")

        source_types = _ensure_unique_sorted_tuple(
            self.supported_source_types,
            "supported_source_types",
        )
        capabilities = _ensure_unique_sorted_tuple(
            self.required_capabilities,
            "required_capabilities",
        )

        if not self.supporting_source_only:
            raise ValueError("supporting_source_only must be True for history ingestion")

        if self.canonical_truth_write_allowed:
            raise ValueError(
                "canonical_truth_write_allowed must be False for history ingestion",
            )

        if self.real_data_import_allowed:
            raise ValueError(
                "real_data_import_allowed must be False during H0 freeze phase",
            )

        object.__setattr__(self, "track_name", track_name)
        object.__setattr__(self, "owning_domain", owning_domain)
        object.__setattr__(self, "package_path", package_path)
        object.__setattr__(self, "supported_source_types", source_types)
        object.__setattr__(self, "required_capabilities", capabilities)

    @property
    def supports_pdf(self) -> bool:
        return "pdf" in self.supported_source_types

    @property
    def supports_html(self) -> bool:
        return "html" in self.supported_source_types

    @property
    def dedup_required(self) -> bool:
        return "dedup_before_real_import" in self.required_capabilities


@dataclass(frozen=True)
class HistoryIngestionTrackFreeze:
    """
    Represents the frozen H0 state of the history-ingestion track.
    """

    scope: HistoryIngestionScope
    freeze_phase_id: str
    freeze_reason: str
    duplicate_memory_world_allowed: bool = field(default=False)
    archive_equals_canonical_truth: bool = field(default=False)

    def __post_init__(self) -> None:
        freeze_phase_id = _ensure_non_empty_str(self.freeze_phase_id, "freeze_phase_id")
        freeze_reason = _ensure_non_empty_str(self.freeze_reason, "freeze_reason")

        if self.duplicate_memory_world_allowed:
            raise ValueError("duplicate_memory_world_allowed must remain False")

        if self.archive_equals_canonical_truth:
            raise ValueError("archive_equals_canonical_truth must remain False")

        object.__setattr__(self, "freeze_phase_id", freeze_phase_id)
        object.__setattr__(self, "freeze_reason", freeze_reason)

    @property
    def freeze_confirmed(self) -> bool:
        return (
            self.scope.supporting_source_only
            and not self.scope.canonical_truth_write_allowed
            and not self.duplicate_memory_world_allowed
            and not self.archive_equals_canonical_truth
        )
