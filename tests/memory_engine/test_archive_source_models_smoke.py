from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_metadata_models import (
    ArchiveSourceMetadata,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)


def test_archive_source_models_smoke() -> None:
    metadata = ArchiveSourceMetadata(
        source_id="HSOURCE-0001",
        source_name="export.html",
        source_path="/tmp/export.html",
        file_size_bytes=128,
        content_hash_sha256="abc123",
    )
    source = ArchiveSource(
        source_type="html",
        metadata=metadata,
        text_payload="<html>ok</html>",
        binary_available=False,
        previewable=True,
    )

    assert source.source_type == "html"
    assert source.supports_direct_text_read is True
    assert source.is_text_first_source is True


def test_archive_source_models_reject_empty_text_payload_for_html() -> None:
    metadata = ArchiveSourceMetadata(
        source_id="HSOURCE-0002",
        source_name="export.html",
        source_path="/tmp/export.html",
        file_size_bytes=0,
        content_hash_sha256=None,
    )
    with pytest.raises(ValueError, match="text_payload must be present for source_type=html"):
        ArchiveSource(
            source_type="html",
            metadata=metadata,
            text_payload=None,
            binary_available=False,
            previewable=True,
        )
