from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_builder import (
    build_archive_manifest,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_writer import (
    build_archive_manifest_write_payload,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.chat_segmenter import (
    segment_chat_document,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_registry_writer import (
    build_import_session_write_payload,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_archive_manifest_writer_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"x": 1}',
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = segment_chat_document(document)
    session = build_import_session_write_payload(
        source=source,
        document=document,
        segments=segments,
    )
    manifest = build_archive_manifest(
        session=session,
        document=document,
        segments=segments,
    )
    payload = build_archive_manifest_write_payload(manifest)

    assert payload["manifest_id"] == manifest.manifest_id
    assert payload["source_type"] == "json"
