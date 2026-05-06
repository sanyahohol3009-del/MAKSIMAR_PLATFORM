from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_models import (
    EndToEndDryRunProof,
)


def build_end_to_end_dry_run_summary(
    proof: EndToEndDryRunProof,
) -> Dict[str, object]:
    return {
        "source_id": proof.source.metadata.source_id,
        "source_type": proof.source.source_type,
        "import_session_id": proof.import_session.import_session_id,
        "manifest_id": proof.manifest.manifest_id,
        "memory_id": proof.normalized_record.memory_object.memory_id,
        "storage_node_id": proof.normalized_record.storage_node_id,
        "dedup_new_unit_count": proof.dedup_decision.new_unit_count,
        "portable_root_id": proof.portable_reference.root_id,
        "portable_relative_path": proof.portable_reference.relative_path,
        "non_canonical": proof.non_canonical,
        "route_ready": proof.route_ready,
        "dry_run_only": proof.dry_run_only,
    }
