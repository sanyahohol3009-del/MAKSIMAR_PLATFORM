from __future__ import annotations

from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def _split_document_sections(text: str) -> Tuple[str, ...]:
    normalized = text.strip()
    if not normalized:
        return ()

    lines = [line.strip() for line in normalized.splitlines()]
    sections = []
    current = []

    for line in lines:
        if not line:
            if current:
                sections.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    return tuple(section for section in sections if section)


def segment_document_sections(
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
        for section in _split_document_sections(content.text):
            segments.append(
                build_segment(
                    parent_document_id=document.document_id,
                    source_type=document.source_type,
                    segment_kind="document_section",
                    ordinal=ordinal,
                    text=section,
                    boundary_label="blank_line_section_boundary",
                ),
            )
            ordinal += 1

    return tuple(segments)
