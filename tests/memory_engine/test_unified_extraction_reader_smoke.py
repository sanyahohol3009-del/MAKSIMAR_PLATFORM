from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_reader import (
    read_archive_source_from_path,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_unified_extraction_reader_smoke_for_html(tmp_path: Path) -> None:
    html_path = tmp_path / "history.html"
    html_path.write_text("<html>history</html>", encoding="utf-8")

    source = read_archive_source_from_path(
        source_path=str(html_path),
        source_type="html",
    )
    document = read_unified_extraction(source)

    assert document.source_type == "html"
    assert document.has_structured_text is True
    assert document.extraction_path == "direct_text_read"


def test_unified_extraction_reader_smoke_for_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "history.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 mock")

    source = read_archive_source_from_path(
        source_path=str(pdf_path),
        source_type="pdf",
    )
    document = read_unified_extraction(source)

    assert document.source_type == "pdf"
    assert document.has_structured_text is False
    assert document.extraction_path == "binary_reference_capture"
