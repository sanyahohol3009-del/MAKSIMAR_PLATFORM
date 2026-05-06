from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)


def build_extraction_summary(
    document: ExtractedDocument,
) -> Dict[str, object]:
    return {
        "document_id": document.document_id,
        "source_id": document.source_id,
        "source_type": document.source_type,
        "content_count": document.content_count,
        "has_structured_text": document.has_structured_text,
        "extraction_path": document.extraction_path,
        "deterministic_output": document.deterministic_output,
        "parallel_safe_by_design": document.parallel_safe_by_design,
    }
