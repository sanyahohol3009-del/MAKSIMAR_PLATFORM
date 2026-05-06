from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_boundary_models import (
    HistoryBoundaryContract,
    HistoryCanonicalTruthSplit,
    HistoryStoragePortabilityRequirement,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_ingestion_validators import (
    validate_history_boundary_contract,
    validate_history_track_freeze,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_scope_models import (
    HistoryIngestionScope,
    HistoryIngestionTrackFreeze,
)


def build_default_history_ingestion_scope() -> HistoryIngestionScope:
    return HistoryIngestionScope(
        track_name="project_history_ingestion_track",
        owning_domain="memory_engine",
        package_path="MAKSIMAR_CORE_LIB/memory_engine/history_ingestion",
        supported_source_types=("html", "pdf", "txt", "md", "json"),
        required_capabilities=(
            "multi_format_source_contract",
            "dedup_before_real_import",
            "supporting_source_only",
            "portable_storage",
            "jarvis_read_target",
            "preview_traceability",
        ),
        supporting_source_only=True,
        canonical_truth_write_allowed=False,
        real_data_import_allowed=False,
    )


def build_default_history_track_freeze() -> HistoryIngestionTrackFreeze:
    freeze = HistoryIngestionTrackFreeze(
        scope=build_default_history_ingestion_scope(),
        freeze_phase_id="PHASE-H0",
        freeze_reason=(
            "Freeze placement, truth split, multi-format requirement, and "
            "dedup-first rule before real data import"
        ),
    )
    validate_history_track_freeze(freeze)
    return freeze


def build_default_history_boundary_contract() -> HistoryBoundaryContract:
    contract = HistoryBoundaryContract(
        boundary_id="HBOUNDARY-0001",
        title="Project History Ingestion Boundary Contract",
        owning_package="MAKSIMAR_CORE_LIB/memory_engine/history_ingestion",
        truth_split=HistoryCanonicalTruthSplit(
            archive_is_supporting_source=True,
            canonical_truth_write_allowed=False,
            auto_promotion_allowed=False,
        ),
        storage_portability=HistoryStoragePortabilityRequirement(
            portable_storage_required=True,
            hardcoded_absolute_paths_forbidden=True,
            future_nas_compatibility_required=True,
        ),
        multi_format_required=True,
        dedup_required_before_real_import=True,
    )
    validate_history_boundary_contract(contract)
    return contract


def build_history_boundary_preview() -> Dict[str, object]:
    freeze = build_default_history_track_freeze()
    boundary = build_default_history_boundary_contract()

    preview: Dict[str, object] = {
        "phase": freeze.freeze_phase_id,
        "track_name": freeze.scope.track_name,
        "package_path": freeze.scope.package_path,
        "supported_source_types": freeze.scope.supported_source_types,
        "required_capabilities": freeze.scope.required_capabilities,
        "supporting_source_only": freeze.scope.supporting_source_only,
        "canonical_truth_write_allowed": freeze.scope.canonical_truth_write_allowed,
        "real_data_import_allowed": freeze.scope.real_data_import_allowed,
        "boundary_id": boundary.boundary_id,
        "boundary_title": boundary.title,
        "multi_format_required": boundary.multi_format_required,
        "dedup_required_before_real_import": boundary.dedup_required_before_real_import,
        "portable_storage_required": (
            boundary.storage_portability.portable_storage_required
        ),
        "future_nas_compatibility_required": (
            boundary.storage_portability.future_nas_compatibility_required
        ),
        "preview_ready": boundary.preview_ready,
    }
    return preview
