from __future__ import annotations

import tempfile

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_writer import (
    execute_live_import_write,
)


def test_live_import_repeat_write_safe_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        first = execute_live_import_write(
            import_root_path="runtime_imports/chatgpt_export_01",
            write_root_path=tmpdir,
        )
        second = execute_live_import_write(
            import_root_path="runtime_imports/chatgpt_export_01",
            write_root_path=tmpdir,
        )

        assert first.repeat_write_safe is True
        assert second.repeat_write_safe is True

        assert first.conversation_manifests_written >= 1
        assert first.normalized_records_written >= 1
        assert first.message_units_written >= 1

        assert second.conversation_manifests_written == 0
        assert second.normalized_records_written == 0
        assert second.message_units_written == 0
