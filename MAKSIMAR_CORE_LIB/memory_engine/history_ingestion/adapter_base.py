from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.source_type_models import (
    SUPPORTED_ARCHIVE_SOURCE_TYPES,
    ArchiveSourceType,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_empty_unique_tuple(
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
class ArchiveAdapterCapability:
    adapter_id: str
    source_type: ArchiveSourceType
    text_first_input: bool
    binary_input_supported: bool
    deterministic_output_required: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        adapter_id = _ensure_non_empty_str(self.adapter_id, "adapter_id")
        if self.source_type not in SUPPORTED_ARCHIVE_SOURCE_TYPES:
            raise ValueError(
                f"source_type must be one of {SUPPORTED_ARCHIVE_SOURCE_TYPES}",
            )

        if not self.deterministic_output_required:
            raise ValueError("deterministic_output_required must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "adapter_id", adapter_id)


@dataclass(frozen=True)
class ArchiveAdapterProtocolContract:
    adapter_name: str
    supported_source_type: ArchiveSourceType
    required_output_kinds: Tuple[str, ...]
    stateless_adapter_required: bool
    side_effect_free_selection_required: bool

    def __post_init__(self) -> None:
        adapter_name = _ensure_non_empty_str(self.adapter_name, "adapter_name")

        if self.supported_source_type not in SUPPORTED_ARCHIVE_SOURCE_TYPES:
            raise ValueError(
                f"supported_source_type must be one of {SUPPORTED_ARCHIVE_SOURCE_TYPES}",
            )

        required_output_kinds = _ensure_non_empty_unique_tuple(
            self.required_output_kinds,
            "required_output_kinds",
        )

        if not self.stateless_adapter_required:
            raise ValueError("stateless_adapter_required must be True")

        if not self.side_effect_free_selection_required:
            raise ValueError("side_effect_free_selection_required must be True")

        object.__setattr__(self, "adapter_name", adapter_name)
        object.__setattr__(self, "required_output_kinds", required_output_kinds)


@dataclass(frozen=True)
class ArchiveAdapterPreview:
    adapter_id: str
    source_type: ArchiveSourceType
    selection_ready: bool
    deterministic_output_required: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        adapter_id = _ensure_non_empty_str(self.adapter_id, "adapter_id")

        if self.source_type not in SUPPORTED_ARCHIVE_SOURCE_TYPES:
            raise ValueError(
                f"source_type must be one of {SUPPORTED_ARCHIVE_SOURCE_TYPES}",
            )

        object.__setattr__(self, "adapter_id", adapter_id)
