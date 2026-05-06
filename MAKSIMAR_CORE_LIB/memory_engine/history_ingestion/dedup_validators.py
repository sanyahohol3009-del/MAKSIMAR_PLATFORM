from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_models import (
    DedupDecision,
)


def validate_dedup_ready(decision: DedupDecision) -> None:
    if not decision.deterministic_output:
        raise ValueError("Dedup decision must be deterministic")
    if not decision.parallel_safe_by_design:
        raise ValueError("Dedup decision must be parallel-safe by design")
