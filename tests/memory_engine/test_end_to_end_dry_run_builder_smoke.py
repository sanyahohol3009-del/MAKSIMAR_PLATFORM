from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_preview,
)


def test_end_to_end_dry_run_builder_smoke() -> None:
    preview = build_end_to_end_dry_run_preview()

    assert preview["source_type"] == "txt"
    assert preview["route_ready"] is True
    assert preview["dry_run_only"] is True
