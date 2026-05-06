from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_builder import (
    build_archive_manifest,
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


def test_import_traceability_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/history.html",
        text_payload="part1\n\npart2",
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

    assert manifest.import_session_id == session.import_session_id
    assert manifest.source_id == source.metadata.source_id
    assert manifest.document_id == document.document_id
