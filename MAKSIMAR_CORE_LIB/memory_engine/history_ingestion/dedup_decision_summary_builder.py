from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_models import (
    DedupDecision,
)


def build_dedup_decision_summary(
    decision: DedupDecision,
) -> Dict[str, object]:
    return {
        "file_already_imported": decision.file_already_imported,
        "content_already_imported": decision.content_already_imported,
        "duplicate_unit_count": decision.duplicate_unit_count,
        "new_unit_count": decision.new_unit_count,
        "write_required": decision.write_required,
        "deterministic_output": decision.deterministic_output,
        "parallel_safe_by_design": decision.parallel_safe_by_design,
    }
