from __future__ import annotations

import hashlib
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_models import (
    ArchiveManifest,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_models import (
    ImportSession,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)


def _manifest_id(import_session_id: str, document_id: str) -> str:
    payload = f"{import_session_id}|{document_id}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"HMANIFEST-{digest[:12].upper()}"


def build_archive_manifest(
    *,
    session: ImportSession,
    document: ExtractedDocument,
    segments: Tuple[ExtractedSegment, ...],
) -> ArchiveManifest:
    return ArchiveManifest(
        manifest_id=_manifest_id(session.import_session_id, document.document_id),
        import_session_id=session.import_session_id,
        source_id=session.source_id,
        source_type=session.source_type,
        document_id=document.document_id,
        segment_count=len(segments),
        content_count=document.content_count,
        extraction_path=document.extraction_path,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )


def build_archive_manifest_preview(
    manifest: ArchiveManifest,
) -> Dict[str, object]:
    return {
        "manifest_id": manifest.manifest_id,
        "import_session_id": manifest.import_session_id,
        "source_id": manifest.source_id,
        "source_type": manifest.source_type,
        "document_id": manifest.document_id,
        "segment_count": manifest.segment_count,
        "content_count": manifest.content_count,
        "extraction_path": manifest.extraction_path,
        "deterministic_output": manifest.deterministic_output,
        "parallel_safe_by_design": manifest.parallel_safe_by_design,
    }
