from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_memory_read_model import (
    build_media_artifact_memory_read_model,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_memory_summary_builder import (
    build_artifact_dedup_contract,
    build_media_memory_summary,
)


_MEDIA_MEMORY_FLOW = (
    "storage_registry",
    "artifact_routing",
    "media_artifact_memory",
    "generated_media_metadata",
    "model_weight_metadata",
    "dataset_metadata",
    "project_output_metadata",
    "dedup_decision",
    "dashboard_read_only_preview",
)


def build_media_memory_preview() -> Dict[str, object]:
    read_model = build_media_artifact_memory_read_model()
    summary = build_media_memory_summary()
    dedup = build_artifact_dedup_contract()

    return {
        "flow": _MEDIA_MEMORY_FLOW,
        "total_records": read_model.total_records,
        "dashboard_visible_records": read_model.dashboard_visible_records,
        "retrieval_visible_records": read_model.retrieval_visible_records,
        "binary_external_records": read_model.binary_external_records,
        "existing_artifacts": dedup.existing_artifacts,
        "new_artifact_candidates": dedup.new_artifact_candidates,
        "write_allowed_candidates": dedup.write_allowed_candidates,
        "rewrite_forbidden_existing": dedup.rewrite_forbidden_existing,
        "summary_ready": summary["media_memory_summary_ready"],
        "preview_ready": True,
        "media_memory_ready": (
            read_model.total_records >= 1
            and read_model.binary_external_records == read_model.total_records
            and read_model.provenance_required_records == read_model.total_records
            and read_model.traceability_required_records == read_model.total_records
            and dedup.rewrite_forbidden_existing == dedup.existing_artifacts
        ),
        "entries": tuple(
            {
                "artifact_id": record.artifact_id,
                "artifact_ref": record.artifact_ref,
                "artifact_kind": record.artifact_kind,
                "storage_registry_id": record.storage_registry_id,
                "binary_external": record.binary_external,
                "dashboard_visible": record.dashboard_visible,
                "retrieval_visible": record.retrieval_visible,
                "approval_required": record.approval_required,
            }
            for record in read_model.records
        ),
    }
