from __future__ import annotations

import tempfile

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_writer import (
    execute_live_import_write,
)


def test_live_import_message_units_written_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        result = execute_live_import_write(
            import_root_path="runtime_imports/chatgpt_export_01",
            write_root_path=tmpdir,
        )
        assert result.message_units_written >= 1
