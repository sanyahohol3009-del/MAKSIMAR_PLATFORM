from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_models import (
    ImportSession,
)


def test_import_session_models_smoke() -> None:
    session = ImportSession(
        import_session_id="HIMPORT-0001",
        source_id="HSOURCE-0001",
        source_type="html",
        source_path="/tmp/history.html",
        status="prepared",
        segment_count=2,
        content_count=1,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )

    assert session.status == "prepared"
    assert session.segment_count == 2


def test_import_session_models_reject_invalid_status() -> None:
    with pytest.raises(ValueError, match="status must be 'prepared' or 'completed'"):
        ImportSession(
            import_session_id="HIMPORT-0002",
            source_id="HSOURCE-0002",
            source_type="txt",
            source_path="/tmp/history.txt",
            status="bad",
            segment_count=0,
            content_count=0,
            deterministic_output=True,
            parallel_safe_by_design=True,
        )
