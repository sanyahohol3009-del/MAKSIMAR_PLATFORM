from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_metadata_models import (
    ArchiveSourceMetadata,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_validators import (
    validate_archive_source_read_ready,
)


def _build_source_id(source_type: str, source_path: str) -> str:
    digest = hashlib.sha256(f"{source_type}:{source_path}".encode("utf-8")).hexdigest()
    return f"HSOURCE-{digest[:12].upper()}"


def _hash_text_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_file_archive_source(
    *,
    source_type: str,
    source_path: str,
    text_payload: str | None,
    binary_available: bool,
) -> ArchiveSource:
    path_obj = Path(source_path)
    source_name = path_obj.name
    size_bytes = len(text_payload.encode("utf-8")) if text_payload is not None else 0
    content_hash = _hash_text_payload(text_payload) if text_payload is not None else None

    metadata = ArchiveSourceMetadata(
        source_id=_build_source_id(source_type, source_path),
        source_name=source_name,
        source_path=source_path,
        file_size_bytes=size_bytes,
        content_hash_sha256=content_hash,
        imported_from_user_export=True,
    )

    source = ArchiveSource(
        source_type=source_type,  # type: ignore[arg-type]
        metadata=metadata,
        text_payload=text_payload,
        binary_available=binary_available,
        previewable=True,
    )
    validate_archive_source_read_ready(source)
    return source


def build_archive_source_preview(source: ArchiveSource) -> Dict[str, object]:
    return {
        "source_id": source.metadata.source_id,
        "source_type": source.source_type,
        "source_name": source.metadata.source_name,
        "source_path": source.metadata.source_path,
        "file_size_bytes": source.metadata.file_size_bytes,
        "hash_available": source.metadata.hash_available,
        "binary_available": source.binary_available,
        "previewable": source.previewable,
        "supports_direct_text_read": source.supports_direct_text_read,
        "is_text_first_source": source.is_text_first_source,
    }


def build_archive_source_readiness_snapshot(source: ArchiveSource) -> Dict[str, object]:
    validate_archive_source_read_ready(source)
    return {
        "source_id": source.metadata.source_id,
        "source_type": source.source_type,
        "read_ready": True,
        "binary_available": source.binary_available,
        "supports_direct_text_read": source.supports_direct_text_read,
    }
