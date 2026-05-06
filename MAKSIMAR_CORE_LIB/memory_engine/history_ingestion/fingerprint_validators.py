from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_models import (
    ContentFingerprint,
    FileFingerprint,
    UnitFingerprint,
)


def validate_file_fingerprint_ready(fingerprint: FileFingerprint) -> None:
    if not fingerprint.deterministic:
        raise ValueError("File fingerprint must be deterministic")
    if not fingerprint.parallel_safe_by_design:
        raise ValueError("File fingerprint must be parallel-safe by design")


def validate_content_fingerprint_ready(fingerprint: ContentFingerprint) -> None:
    if not fingerprint.deterministic:
        raise ValueError("Content fingerprint must be deterministic")
    if not fingerprint.parallel_safe_by_design:
        raise ValueError("Content fingerprint must be parallel-safe by design")


def validate_unit_fingerprint_ready(fingerprint: UnitFingerprint) -> None:
    if not fingerprint.deterministic:
        raise ValueError("Unit fingerprint must be deterministic")
    if not fingerprint.parallel_safe_by_design:
        raise ValueError("Unit fingerprint must be parallel-safe by design")
