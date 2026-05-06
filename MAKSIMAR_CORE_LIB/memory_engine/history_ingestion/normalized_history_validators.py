from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_models import (
    NormalizedHistoryRecord,
)


def validate_normalized_history_read_ready(
    record: NormalizedHistoryRecord,
) -> None:
    if not record.readable_by_jarvis:
        raise ValueError("Normalized history record must be readable_by_jarvis")
    if record.canonical_truth:
        raise ValueError("Normalized history record must not be canonical truth")
    if not record.deterministic_output:
        raise ValueError("Normalized history record must be deterministic")


def validate_normalized_history_write_ready(
    record: NormalizedHistoryRecord,
) -> None:
    validate_normalized_history_read_ready(record)
    if not record.parallel_safe_by_design:
        raise ValueError("Normalized history record must be parallel-safe by design")
