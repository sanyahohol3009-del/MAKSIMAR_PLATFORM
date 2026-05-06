from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_reader import (
    read_archive_source_from_path,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extraction_summary_builder import (
    build_extraction_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_extraction_summary_builder_smoke(tmp_path: Path) -> None:
    txt_path = tmp_path / "history.txt"
    txt_path.write_text("history body", encoding="utf-8")

    source = read_archive_source_from_path(
        source_path=str(txt_path),
        source_type="txt",
    )
    document = read_unified_extraction(source)
    summary = build_extraction_summary(document)

    assert summary["source_type"] == "txt"
    assert summary["has_structured_text"] is True
    assert summary["deterministic_output"] is True
    assert summary["parallel_safe_by_design"] is True
