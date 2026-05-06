from __future__ import annotations

import hashlib
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_models import (
    ImportSession,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_validators import (
    validate_import_session_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)


def _import_session_id(source_id: str, source_path: str) -> str:
    payload = f"{source_id}|{source_path}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"HIMPORT-{digest[:12].upper()}"


def build_import_session_write_payload(
    *,
    source: ArchiveSource,
    document: ExtractedDocument,
    segments: Tuple[ExtractedSegment, ...],
) -> ImportSession:
    session = ImportSession(
        import_session_id=_import_session_id(
            source.metadata.source_id,
            source.metadata.source_path,
        ),
        source_id=source.metadata.source_id,
        source_type=source.source_type,
        source_path=source.metadata.source_path,
        status="prepared",
        segment_count=len(segments),
        content_count=document.content_count,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )
    validate_import_session_ready(session)
    return session


def build_import_session_preview(
    session: ImportSession,
) -> Dict[str, object]:
    validate_import_session_ready(session)
    return {
        "import_session_id": session.import_session_id,
        "source_id": session.source_id,
        "source_type": session.source_type,
        "status": session.status,
        "segment_count": session.segment_count,
        "content_count": session.content_count,
        "deterministic_output": session.deterministic_output,
        "parallel_safe_by_design": session.parallel_safe_by_design,
    }
