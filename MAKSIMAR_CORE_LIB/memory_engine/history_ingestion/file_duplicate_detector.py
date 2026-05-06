from __future__ import annotations

from typing import Iterable

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_fingerprint_builder import (
    build_file_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)


def detect_file_duplicate(
    source: ArchiveSource,
    existing_file_hashes: Iterable[str],
) -> bool:
    fingerprint = build_file_fingerprint(source)
    return fingerprint.sha256_hex in set(existing_file_hashes)
