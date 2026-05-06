from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_content_models import (
    ExtractedContent,
)


def test_extracted_content_models_smoke() -> None:
    content = ExtractedContent(
        content_id="HCONTENT-0003",
        content_kind="structured_text",
        text="body",
        byte_length_hint=4,
        source_type="html",
        extraction_stable=True,
    )

    assert content.has_text is True
    assert content.content_kind == "structured_text"


def test_extracted_content_rejects_text_for_binary_reference() -> None:
    with pytest.raises(ValueError, match="binary_reference content must not include text"):
        ExtractedContent(
            content_id="HCONTENT-0004",
            content_kind="binary_reference",
            text="not allowed",
            byte_length_hint=12,
            source_type="pdf",
            extraction_stable=True,
        )
