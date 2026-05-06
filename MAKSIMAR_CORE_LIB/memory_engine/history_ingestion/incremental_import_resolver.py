from __future__ import annotations

from typing import Iterable

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_duplicate_detector import (
    detect_content_duplicate,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_models import (
    DedupDecision,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_validators import (
    validate_dedup_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_duplicate_detector import (
    detect_file_duplicate,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_duplicate_detector import (
    detect_unit_duplicates,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def resolve_incremental_import(
    *,
    source: ArchiveSource,
    existing_file_hashes: Iterable[str],
    existing_content_hashes: Iterable[str],
    existing_unit_hashes: Iterable[str],
) -> DedupDecision:
    document = read_unified_extraction(source)

    file_duplicate = detect_file_duplicate(source, existing_file_hashes)
    content_duplicate = detect_content_duplicate(document, existing_content_hashes)

    if file_duplicate:
        duplicate_unit_count = len(document.contents)
        new_unit_count = 0
        write_required = False
    else:
        duplicate_unit_count, new_unit_count = detect_unit_duplicates(
            document.contents,
            existing_unit_hashes,
        )
        write_required = new_unit_count > 0

    decision = DedupDecision(
        file_already_imported=file_duplicate,
        content_already_imported=content_duplicate,
        duplicate_unit_count=duplicate_unit_count,
        new_unit_count=new_unit_count,
        write_required=write_required,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )
    validate_dedup_ready(decision)
    return decision
