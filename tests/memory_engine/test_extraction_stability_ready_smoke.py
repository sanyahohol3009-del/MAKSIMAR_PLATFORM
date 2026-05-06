from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extraction_validators import (
    validate_extraction_stability,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_extraction_stability_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="stable history",
        binary_available=False,
    )

    document = read_unified_extraction(source)
    validate_extraction_stability(document)

    assert document.deterministic_output is True
    assert document.parallel_safe_by_design is True
