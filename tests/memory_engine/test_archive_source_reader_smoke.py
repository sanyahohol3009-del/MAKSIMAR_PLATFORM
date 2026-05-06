from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_reader import (
    read_archive_source_from_path,
)


def test_archive_source_reader_smoke_for_text_first_types(tmp_path: Path) -> None:
    html_path = tmp_path / "history.html"
    html_path.write_text("<html>history</html>", encoding="utf-8")

    source = read_archive_source_from_path(
        source_path=str(html_path),
        source_type="html",
    )

    assert source.source_type == "html"
    assert source.supports_direct_text_read is True
    assert source.text_payload == "<html>history</html>"
    assert source.binary_available is False


def test_archive_source_reader_smoke_for_pdf_contract(tmp_path: Path) -> None:
    pdf_path = tmp_path / "history.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 mock")

    source = read_archive_source_from_path(
        source_path=str(pdf_path),
        source_type="pdf",
    )

    assert source.source_type == "pdf"
    assert source.supports_direct_text_read is False
    assert source.binary_available is True
    assert source.text_payload is None


def test_archive_source_reader_reject_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError, match="Archive source not found"):
        read_archive_source_from_path(
            source_path=str(missing_path),
            source_type="json",
        )
