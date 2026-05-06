from __future__ import annotations

from typing import Iterable

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_fingerprint_builder import (
    build_content_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)


def detect_content_duplicate(
    document: ExtractedDocument,
    existing_content_hashes: Iterable[str],
) -> bool:
    fingerprint = build_content_fingerprint(document)
    return fingerprint.sha256_hex in set(existing_content_hashes)
