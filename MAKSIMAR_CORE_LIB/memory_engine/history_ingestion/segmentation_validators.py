from __future__ import annotations

from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)


def validate_segment_sequence(
    segments: Tuple[ExtractedSegment, ...],
) -> None:
    if not segments:
        raise ValueError("segments must not be empty")

    expected = list(range(len(segments)))
    actual = [segment.ordinal for segment in segments]
    if actual != expected:
        raise ValueError("segment ordinals must be contiguous and start at 0")


def validate_segmentation_read_ready(
    segments: Tuple[ExtractedSegment, ...],
) -> None:
    validate_segment_sequence(segments)

    for segment in segments:
        if not segment.deterministic_output:
            raise ValueError("all segments must be deterministic")
        if not segment.parallel_safe_by_design:
            raise ValueError("all segments must be parallel-safe by design")
        if not segment.stable_boundary:
            raise ValueError("all segments must have stable boundaries")
