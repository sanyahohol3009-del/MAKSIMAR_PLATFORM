from __future__ import annotations

from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


MESSAGE_PREFIXES = (
    "user:",
    "assistant:",
    "system:",
    "tool:",
)


def _split_message_units(text: str) -> Tuple[str, ...]:
    normalized = text.strip()
    if not normalized:
        return ()

    lines = [line.strip() for line in normalized.splitlines() if line.strip()]
    if not lines:
        return ()

    units = []
    current = []

    for line in lines:
        lower_line = line.lower()
        if any(lower_line.startswith(prefix) for prefix in MESSAGE_PREFIXES):
            if current:
                units.append("\n".join(current).strip())
                current = []
        current.append(line)

    if current:
        units.append("\n".join(current).strip())

    return tuple(unit for unit in units if unit)


def extract_message_units(
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
        for unit in _split_message_units(content.text):
            segments.append(
                build_segment(
                    parent_document_id=document.document_id,
                    source_type=document.source_type,
                    segment_kind="message_unit",
                    ordinal=ordinal,
                    text=unit,
                    boundary_label="message_prefix_boundary",
                ),
            )
            ordinal += 1

    return tuple(segments)
