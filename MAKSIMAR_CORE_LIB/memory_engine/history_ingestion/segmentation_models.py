from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SegmentKind = Literal[
    "chat_segment",
    "document_section",
    "message_unit",
]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True)
class ExtractedSegment:
    segment_id: str
    parent_document_id: str
    source_type: str
    segment_kind: SegmentKind
    ordinal: int
    text: str
    boundary_label: str
    stable_boundary: bool
    deterministic_output: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        segment_id = _ensure_non_empty_str(self.segment_id, "segment_id")
        parent_document_id = _ensure_non_empty_str(
            self.parent_document_id,
            "parent_document_id",
        )
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        boundary_label = _ensure_non_empty_str(self.boundary_label, "boundary_label")
        text = _ensure_non_empty_str(self.text, "text")
        ordinal = _ensure_non_negative_int(self.ordinal, "ordinal")

        if self.segment_kind not in ("chat_segment", "document_section", "message_unit"):
            raise ValueError(
                "segment_kind must be 'chat_segment', 'document_section', or 'message_unit'",
            )

        if not self.stable_boundary:
            raise ValueError("stable_boundary must be True")

        if not self.deterministic_output:
            raise ValueError("deterministic_output must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "segment_id", segment_id)
        object.__setattr__(self, "parent_document_id", parent_document_id)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "boundary_label", boundary_label)
        object.__setattr__(self, "text", text)
        object.__setattr__(self, "ordinal", ordinal)
