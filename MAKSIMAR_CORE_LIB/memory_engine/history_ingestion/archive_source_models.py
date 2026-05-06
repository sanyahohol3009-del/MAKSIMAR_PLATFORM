from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_metadata_models import (
    ArchiveSourceMetadata,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.source_type_models import (
    SUPPORTED_ARCHIVE_SOURCE_TYPES,
    ArchiveSourceType,
)


TEXT_FIRST_SOURCE_TYPES = ("html", "txt", "md", "json")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class ArchiveSource:
    source_type: ArchiveSourceType
    metadata: ArchiveSourceMetadata
    text_payload: Optional[str]
    binary_available: bool
    previewable: bool

    def __post_init__(self) -> None:
        if self.source_type not in SUPPORTED_ARCHIVE_SOURCE_TYPES:
            raise ValueError(
                f"source_type must be one of {SUPPORTED_ARCHIVE_SOURCE_TYPES}",
            )

        text_payload = self.text_payload
        if text_payload is not None:
            text_payload = _ensure_non_empty_str(text_payload, "text_payload")

        # Specific rules for text-first archive sources must be checked
        # before the generic fallback validation so test expectations and
        # operator diagnostics stay precise.
        if self.source_type in TEXT_FIRST_SOURCE_TYPES and text_payload is None:
            raise ValueError(
                f"text_payload must be present for source_type={self.source_type}",
            )

        if not self.binary_available and text_payload is None:
            raise ValueError(
                "At least one of binary_available or text_payload must be present",
            )

        object.__setattr__(self, "text_payload", text_payload)

    @property
    def is_text_first_source(self) -> bool:
        return self.source_type in TEXT_FIRST_SOURCE_TYPES

    @property
    def supports_direct_text_read(self) -> bool:
        return self.text_payload is not None
