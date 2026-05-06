from __future__ import annotations

from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def _split_chat_text(text: str) -> Tuple[str, ...]:
    normalized = text.strip()
    if not normalized:
        return ()

    parts = [part.strip() for part in normalized.split("\n\n") if part.strip()]
    if parts:
        return tuple(parts)

    return (normalized,)


def segment_chat_document(
    document: ExtractedDocument,
) -> Tuple:
    if not document.has_structured_text:
        return ()

    segments = []
    ordinal = 0
    for content in document.contents:
        if not content.has_text:
            continue
        assert content.text is not None
        for part in _split_chat_text(content.text):
            segments.append(
                build_segment(
                    parent_document_id=document.document_id,
                    source_type=document.source_type,
                    segment_kind="chat_segment",
                    ordinal=ordinal,
                    text=part,
                    boundary_label="double_newline_boundary",
                ),
            )
            ordinal += 1

    return tuple(segments)
