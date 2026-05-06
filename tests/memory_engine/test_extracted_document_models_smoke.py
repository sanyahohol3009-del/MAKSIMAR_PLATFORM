from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_content_models import (
    ExtractedContent,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)


def test_extracted_document_models_smoke() -> None:
    content = ExtractedContent(
        content_id="HCONTENT-0001",
        content_kind="structured_text",
        text="hello",
        byte_length_hint=5,
        source_type="txt",
        extraction_stable=True,
    )
    document = ExtractedDocument(
        document_id="HDOC-0001",
        source_id="HSOURCE-0001",
        source_type="txt",
        contents=(content,),
        extraction_path="direct_text_read",
        deterministic_output=True,
        parallel_safe_by_design=True,
    )

    assert document.content_count == 1
    assert document.has_structured_text is True


def test_extracted_document_rejects_empty_contents() -> None:
    with pytest.raises(ValueError, match="contents must not be empty"):
        ExtractedDocument(
            document_id="HDOC-0002",
            source_id="HSOURCE-0002",
            source_type="pdf",
            contents=(),
            extraction_path="binary_reference_capture",
            deterministic_output=True,
            parallel_safe_by_design=True,
        )
