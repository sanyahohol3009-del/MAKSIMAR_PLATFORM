from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extraction_builders import (
    build_extracted_document_from_source,
)


def read_unified_extraction(
    source: ArchiveSource,
) -> ExtractedDocument:
    return build_extracted_document_from_source(source)
