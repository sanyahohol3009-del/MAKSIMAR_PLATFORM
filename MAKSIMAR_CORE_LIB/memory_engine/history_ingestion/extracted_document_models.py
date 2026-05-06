from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_content_models import (
    ExtractedContent,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class ExtractedDocument:
    document_id: str
    source_id: str
    source_type: str
    contents: Tuple[ExtractedContent, ...]
    extraction_path: str
    deterministic_output: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        document_id = _ensure_non_empty_str(self.document_id, "document_id")
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        extraction_path = _ensure_non_empty_str(
            self.extraction_path,
            "extraction_path",
        )

        if not self.contents:
            raise ValueError("contents must not be empty")

        if not self.deterministic_output:
            raise ValueError("deterministic_output must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "document_id", document_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "extraction_path", extraction_path)

    @property
    def content_count(self) -> int:
        return len(self.contents)

    @property
    def has_structured_text(self) -> bool:
        return any(content.content_kind == "structured_text" for content in self.contents)
