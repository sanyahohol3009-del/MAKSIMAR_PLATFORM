from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.source_type_models import (
    SUPPORTED_ARCHIVE_SOURCE_TYPES,
)


def test_source_type_models_smoke() -> None:
    assert SUPPORTED_ARCHIVE_SOURCE_TYPES == ("html", "pdf", "txt", "md", "json")
    assert "html" in SUPPORTED_ARCHIVE_SOURCE_TYPES
    assert "pdf" in SUPPORTED_ARCHIVE_SOURCE_TYPES
    assert "json" in SUPPORTED_ARCHIVE_SOURCE_TYPES
