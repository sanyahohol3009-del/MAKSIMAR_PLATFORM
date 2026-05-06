from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)


TEXT_FIRST_TYPES = {"html", "txt", "md", "json"}


def _normalize_source_type(source_type: str) -> str:
    normalized = source_type.strip().lower()
    if normalized not in {"html", "pdf", "txt", "md", "json"}:
        raise ValueError("Unsupported source_type")
    return normalized


def read_archive_source_from_path(
    *,
    source_path: str,
    source_type: str,
) -> ArchiveSource:
    normalized_type = _normalize_source_type(source_type)
    path_obj = Path(source_path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Archive source not found: {source_path}")

    if not path_obj.is_file():
        raise ValueError(f"Archive source must be a file: {source_path}")

    if normalized_type in TEXT_FIRST_TYPES:
        text_payload = path_obj.read_text(encoding="utf-8")
        binary_available = False
    else:
        text_payload = None
        binary_available = True

    return build_file_archive_source(
        source_type=normalized_type,
        source_path=str(path_obj),
        text_payload=text_payload,
        binary_available=binary_available,
    )
