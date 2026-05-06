from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_models import (
    ImportSession,
)


def validate_import_session_ready(
    session: ImportSession,
) -> None:
    if session.status not in ("prepared", "completed"):
        raise ValueError("Import session status is invalid")
    if not session.deterministic_output:
        raise ValueError("Import session must be deterministic")
    if not session.parallel_safe_by_design:
        raise ValueError("Import session must be parallel-safe by design")
