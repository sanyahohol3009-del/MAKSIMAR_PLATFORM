from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_preview,
)


def test_end_to_end_dry_run_preview_smoke() -> None:
    preview = build_end_to_end_dry_run_preview()

    assert preview["dedup_write_required"] is True
    assert preview["portable_relative_path"] == "normalized_history/HCHAT-0001.json"
