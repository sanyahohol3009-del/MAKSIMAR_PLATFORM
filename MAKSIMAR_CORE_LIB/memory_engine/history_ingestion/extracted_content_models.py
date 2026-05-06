from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ExtractedContentKind = Literal[
    "structured_text",
    "binary_reference",
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
class ExtractedContent:
    content_id: str
    content_kind: ExtractedContentKind
    text: str | None
    byte_length_hint: int
    source_type: str
    extraction_stable: bool

    def __post_init__(self) -> None:
        content_id = _ensure_non_empty_str(self.content_id, "content_id")
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        byte_length_hint = _ensure_non_negative_int(
            self.byte_length_hint,
            "byte_length_hint",
        )

        if self.content_kind not in ("structured_text", "binary_reference"):
            raise ValueError(
                "content_kind must be 'structured_text' or 'binary_reference'",
            )

        text = self.text
        if text is not None:
            text = _ensure_non_empty_str(text, "text")

        if self.content_kind == "structured_text" and text is None:
            raise ValueError("structured_text content must include text")

        if self.content_kind == "binary_reference" and text is not None:
            raise ValueError("binary_reference content must not include text")

        if not self.extraction_stable:
            raise ValueError("extraction_stable must be True")

        object.__setattr__(self, "content_id", content_id)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "byte_length_hint", byte_length_hint)
        object.__setattr__(self, "text", text)

    @property
    def has_text(self) -> bool:
        return self.text is not None
