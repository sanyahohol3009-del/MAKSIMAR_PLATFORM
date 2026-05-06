from __future__ import annotations

import hashlib
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_validators import (
    validate_segmentation_read_ready,
)


def _segment_id(
    parent_document_id: str,
    ordinal: int,
    segment_kind: str,
    text: str,
) -> str:
    payload = f"{parent_document_id}|{ordinal}|{segment_kind}|{text}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"HSEG-{digest[:12].upper()}"


def build_segment(
    *,
    parent_document_id: str,
    source_type: str,
    segment_kind: str,
    ordinal: int,
    text: str,
    boundary_label: str,
) -> ExtractedSegment:
    return ExtractedSegment(
        segment_id=_segment_id(parent_document_id, ordinal, segment_kind, text),
        parent_document_id=parent_document_id,
        source_type=source_type,
        segment_kind=segment_kind,  # type: ignore[arg-type]
        ordinal=ordinal,
        text=text,
        boundary_label=boundary_label,
        stable_boundary=True,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )


def build_segmentation_preview(
    segments: Tuple[ExtractedSegment, ...],
) -> Dict[str, object]:
    validate_segmentation_read_ready(segments)
    return {
        "segment_count": len(segments),
        "first_segment_kind": segments[0].segment_kind,
        "first_boundary_label": segments[0].boundary_label,
        "last_ordinal": segments[-1].ordinal,
        "read_ready": True,
    }
