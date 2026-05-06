from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)


def validate_unified_extraction_read_ready(
    document: ExtractedDocument,
) -> None:
    if document.source_type in ("html", "txt", "md", "json") and not document.has_structured_text:
        raise ValueError(
            f"source_type={document.source_type} must yield structured_text extraction",
        )

    if not document.deterministic_output:
        raise ValueError("Extraction document must be deterministic")

    if not document.parallel_safe_by_design:
        raise ValueError("Extraction document must be parallel-safe by design")


def validate_extraction_stability(
    document: ExtractedDocument,
) -> None:
    validate_unified_extraction_read_ready(document)

    for content in document.contents:
        if not content.extraction_stable:
            raise ValueError("All extracted content must be stable")
