from __future__ import annotations

import hashlib

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_models import (
    FileFingerprint,
)


def _fingerprint_id(prefix: str, payload: str) -> str:
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{prefix}-{digest[:12].upper()}"


def build_file_fingerprint(source: ArchiveSource) -> FileFingerprint:
    source_path = source.metadata.source_path
    file_size = source.metadata.file_size_bytes
    source_type = source.source_type

    payload = f"{source_type}|{source_path}|{file_size}"
    sha256_hex = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return FileFingerprint(
        fingerprint_id=_fingerprint_id("HFILEFP", payload),
        fingerprint_kind="file_fingerprint",
        source_id=source.metadata.source_id,
        sha256_hex=sha256_hex,
        deterministic=True,
        parallel_safe_by_design=True,
    )
