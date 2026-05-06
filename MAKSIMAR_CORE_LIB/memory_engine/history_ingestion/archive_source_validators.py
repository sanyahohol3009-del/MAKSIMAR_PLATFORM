from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)


def validate_archive_source_supported(source: ArchiveSource) -> None:
    if source.source_type not in ("html", "pdf", "txt", "md", "json"):
        raise ValueError("Unsupported archive source type")


def validate_archive_source_read_ready(source: ArchiveSource) -> None:
    validate_archive_source_supported(source)

    if source.source_type in ("html", "txt", "md", "json") and not source.supports_direct_text_read:
        raise ValueError(
            f"Text-first source {source.source_type} must expose text_payload",
        )

    if source.source_type == "pdf" and not source.binary_available:
        raise ValueError("PDF source must have binary_available=True")
