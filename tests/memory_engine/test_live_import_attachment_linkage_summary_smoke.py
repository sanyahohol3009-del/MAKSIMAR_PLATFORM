from __future__ import annotations

import tempfile
from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_writer import (
    execute_live_import_write,
)


def test_live_import_attachment_linkage_summary_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        execute_live_import_write(
            import_root_path="runtime_imports/chatgpt_export_01",
            write_root_path=tmpdir,
        )
        path = Path(tmpdir) / "registry" / "attachment_links" / "LIVE-IMPORT-CHATGPT-0001.json"
        assert path.exists()
