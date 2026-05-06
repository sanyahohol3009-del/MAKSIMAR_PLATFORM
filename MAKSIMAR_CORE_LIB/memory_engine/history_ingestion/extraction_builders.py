from __future__ import annotations

import hashlib
from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_content_models import (
    ExtractedContent,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extraction_validators import (
    validate_extraction_stability,
)


def _hash_id(prefix: str, payload: str) -> str:
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{prefix}-{digest[:12].upper()}"


def build_extracted_document_from_source(
    source: ArchiveSource,
) -> ExtractedDocument:
    if source.supports_direct_text_read:
        text_payload = source.text_payload
        assert text_payload is not None

        content = ExtractedContent(
            content_id=_hash_id("HCONTENT", f"{source.metadata.source_id}:text"),
            content_kind="structured_text",
            text=text_payload,
            byte_length_hint=len(text_payload.encode("utf-8")),
            source_type=source.source_type,
            extraction_stable=True,
        )
        extraction_path = "direct_text_read"
    else:
        content = ExtractedContent(
            content_id=_hash_id("HCONTENT", f"{source.metadata.source_id}:binary"),
            content_kind="binary_reference",
            text=None,
            byte_length_hint=source.metadata.file_size_bytes,
            source_type=source.source_type,
            extraction_stable=True,
        )
        extraction_path = "binary_reference_capture"

    document = ExtractedDocument(
        document_id=_hash_id("HDOC", source.metadata.source_id),
        source_id=source.metadata.source_id,
        source_type=source.source_type,
        contents=(content,),
        extraction_path=extraction_path,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )
    validate_extraction_stability(document)
    return document


def build_unified_extraction_preview(
    source: ArchiveSource,
) -> Dict[str, object]:
    document = build_extracted_document_from_source(source)
    return {
        "source_id": document.source_id,
        "source_type": document.source_type,
        "document_id": document.document_id,
        "content_count": document.content_count,
        "has_structured_text": document.has_structured_text,
        "extraction_path": document.extraction_path,
        "deterministic_output": document.deterministic_output,
        "parallel_safe_by_design": document.parallel_safe_by_design,
    }
