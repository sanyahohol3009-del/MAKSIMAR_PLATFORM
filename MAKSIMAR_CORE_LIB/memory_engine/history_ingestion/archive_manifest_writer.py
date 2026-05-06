from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_models import (
    ArchiveManifest,
)


def build_archive_manifest_write_payload(
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
