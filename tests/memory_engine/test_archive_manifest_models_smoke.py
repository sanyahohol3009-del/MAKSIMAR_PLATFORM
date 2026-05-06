from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_models import (
    ArchiveManifest,
)


def test_archive_manifest_models_smoke() -> None:
    manifest = ArchiveManifest(
        manifest_id="HMANIFEST-0001",
        import_session_id="HIMPORT-0001",
        source_id="HSOURCE-0001",
        source_type="html",
        document_id="HDOC-0001",
        segment_count=2,
        content_count=1,
        extraction_path="direct_text_read",
        deterministic_output=True,
        parallel_safe_by_design=True,
    )

    assert manifest.segment_count == 2
    assert manifest.extraction_path == "direct_text_read"


def test_archive_manifest_models_reject_negative_segment_count() -> None:
    with pytest.raises(ValueError, match="segment_count must be >= 0"):
        ArchiveManifest(
            manifest_id="HMANIFEST-0002",
            import_session_id="HIMPORT-0002",
            source_id="HSOURCE-0002",
            source_type="pdf",
            document_id="HDOC-0002",
            segment_count=-1,
            content_count=0,
            extraction_path="binary_reference_capture",
            deterministic_output=True,
            parallel_safe_by_design=True,
        )
