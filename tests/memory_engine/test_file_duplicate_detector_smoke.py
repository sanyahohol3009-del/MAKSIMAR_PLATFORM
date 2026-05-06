from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_duplicate_detector import (
    detect_file_duplicate,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_fingerprint_builder import (
    build_file_fingerprint,
)


def test_file_duplicate_detector_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="alpha",
        binary_available=False,
    )
    file_hash = build_file_fingerprint(source).sha256_hex

    assert detect_file_duplicate(source, [file_hash]) is True
