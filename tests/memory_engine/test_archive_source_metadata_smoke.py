from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_metadata_models import (
    ArchiveSourceMetadata,
)


def test_archive_source_metadata_smoke() -> None:
    metadata = ArchiveSourceMetadata(
        source_id="HSOURCE-0003",
        source_name="history.pdf",
        source_path="/tmp/history.pdf",
        file_size_bytes=2048,
        content_hash_sha256=None,
    )

    assert metadata.source_id == "HSOURCE-0003"
    assert metadata.file_size_bytes == 2048
    assert metadata.hash_available is False


def test_archive_source_metadata_reject_negative_size() -> None:
    with pytest.raises(ValueError, match="file_size_bytes must be >= 0"):
        ArchiveSourceMetadata(
            source_id="HSOURCE-0004",
            source_name="bad.txt",
            source_path="/tmp/bad.txt",
            file_size_bytes=-1,
            content_hash_sha256=None,
        )
