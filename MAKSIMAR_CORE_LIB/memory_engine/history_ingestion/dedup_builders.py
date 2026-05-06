from __future__ import annotations

from typing import Dict, Iterable

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_decision_summary_builder import (
    build_dedup_decision_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)


def build_dedup_preview(
    *,
    source: ArchiveSource,
    existing_file_hashes: Iterable[str],
    existing_content_hashes: Iterable[str],
    existing_unit_hashes: Iterable[str],
) -> Dict[str, object]:
    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=existing_file_hashes,
        existing_content_hashes=existing_content_hashes,
        existing_unit_hashes=existing_unit_hashes,
    )
    return build_dedup_decision_summary(decision)


def build_incremental_import_preview(
    *,
    source: ArchiveSource,
    existing_file_hashes: Iterable[str],
    existing_content_hashes: Iterable[str],
    existing_unit_hashes: Iterable[str],
) -> Dict[str, object]:
    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=existing_file_hashes,
        existing_content_hashes=existing_content_hashes,
        existing_unit_hashes=existing_unit_hashes,
    )
    return {
        "incremental_import_ready": True,
        "write_required": decision.write_required,
        "new_unit_count": decision.new_unit_count,
        "duplicate_unit_count": decision.duplicate_unit_count,
    }


def build_only_new_content_preview(
    *,
    source: ArchiveSource,
    existing_file_hashes: Iterable[str],
    existing_content_hashes: Iterable[str],
    existing_unit_hashes: Iterable[str],
) -> Dict[str, object]:
    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=existing_file_hashes,
        existing_content_hashes=existing_content_hashes,
        existing_unit_hashes=existing_unit_hashes,
    )
    return {
        "only_new_content_would_be_added": decision.new_unit_count > 0,
        "write_required": decision.write_required,
        "file_already_imported": decision.file_already_imported,
        "content_already_imported": decision.content_already_imported,
    }
