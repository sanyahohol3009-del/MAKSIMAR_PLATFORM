from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_manifest_builder import (
    build_archive_manifest,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_models import (
    EndToEndDryRunProof,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_validators import (
    validate_end_to_end_dry_run_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.import_session_registry_writer import (
    build_import_session_write_payload,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def build_end_to_end_dry_run_proof() -> EndToEndDryRunProof:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history_export.txt",
        text_payload="user: hello\n\nassistant: hi",
        binary_available=False,
    )

    document = read_unified_extraction(source)

    segment = build_segment(
        parent_document_id=document.document_id,
        source_type=source.source_type,
        segment_kind="chat_segment",
        ordinal=0,
        text="user: hello\n\nassistant: hi",
        boundary_label="double_newline_boundary",
    )
    segments = (segment,)

    import_session = build_import_session_write_payload(
        source=source,
        document=document,
        segments=segments,
    )

    manifest = build_archive_manifest(
        session=import_session,
        document=document,
        segments=segments,
    )

    normalized_record = build_normalized_history_record(segment, 1)

    dedup_decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )

    root = StorageRoot(
        root_id="ROOT-LOCAL-001",
        root_type="local_ssd",
        root_path="/mnt/data/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    portable_reference = build_portable_storage_reference(
        storage_node_id=normalized_record.storage_node_id,
        root=root,
        relative_path=normalized_record.write_path,
    )

    proof = EndToEndDryRunProof(
        source=source,
        import_session=import_session,
        manifest=manifest,
        normalized_record=normalized_record,
        dedup_decision=dedup_decision,
        portable_reference=portable_reference,
        non_canonical=True,
        route_ready=True,
        dry_run_only=True,
    )
    validate_end_to_end_dry_run_ready(proof)
    return proof


def build_end_to_end_dry_run_preview() -> Dict[str, object]:
    proof = build_end_to_end_dry_run_proof()
    return {
        "source_type": proof.source.source_type,
        "import_session_id": proof.import_session.import_session_id,
        "manifest_id": proof.manifest.manifest_id,
        "memory_id": proof.normalized_record.memory_object.memory_id,
        "dedup_write_required": proof.dedup_decision.write_required,
        "portable_relative_path": proof.portable_reference.relative_path,
        "route_ready": proof.route_ready,
        "dry_run_only": proof.dry_run_only,
    }
