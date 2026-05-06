from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_models import (
    LiveImportWriteResult,
)


def test_live_import_write_models_smoke() -> None:
    result = LiveImportWriteResult(
        session_manifest_written=True,
        conversation_manifests_written=1,
        normalized_records_written=1,
        message_units_written=1,
        attachment_root_count=1,
        repeat_write_safe=True,
        write_ready=True,
    )
    assert result.write_ready is True
