from __future__ import annotations

import tempfile

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_summary_builder import (
    build_live_import_write_summary,
)


def test_live_import_write_summary_builder_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        summary = build_live_import_write_summary(
            import_root_path="runtime_imports/chatgpt_export_01",
            write_root_path=tmpdir,
        )
    assert summary["write_ready"] is True
