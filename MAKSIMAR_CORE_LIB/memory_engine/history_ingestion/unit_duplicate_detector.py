from __future__ import annotations

from typing import Iterable, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_content_models import (
    ExtractedContent,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_fingerprint_builder import (
    build_unit_fingerprint,
)


def detect_unit_duplicates(
    contents: Tuple[ExtractedContent, ...],
    existing_unit_hashes: Iterable[str],
) -> tuple[int, int]:
    existing = set(existing_unit_hashes)
    duplicate_count = 0
    new_count = 0

    for content in contents:
        fingerprint = build_unit_fingerprint(content)
        if fingerprint.sha256_hex in existing:
            duplicate_count += 1
        else:
            new_count += 1

    return duplicate_count, new_count
