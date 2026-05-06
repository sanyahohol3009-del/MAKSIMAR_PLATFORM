from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_models import (
    ArchiveManifest,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_models import (
    DedupDecision,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_models import (
    ImportSession,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_models import (
    NormalizedHistoryRecord,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)


@dataclass(frozen=True)
class EndToEndDryRunProof:
    source: ArchiveSource
    import_session: ImportSession
    manifest: ArchiveManifest
    normalized_record: NormalizedHistoryRecord
    dedup_decision: DedupDecision
    portable_reference: PortableStorageReference
    non_canonical: bool
    route_ready: bool
    dry_run_only: bool

    def __post_init__(self) -> None:
        if not self.non_canonical:
            raise ValueError("non_canonical must be True")

        if not self.route_ready:
            raise ValueError("route_ready must be True")

        if not self.dry_run_only:
            raise ValueError("dry_run_only must be True")
