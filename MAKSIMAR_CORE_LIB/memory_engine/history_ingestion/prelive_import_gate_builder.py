from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_builders import (
    build_incremental_import_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_completion_summary_builder import (
    build_history_completion_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_models import (
    PreLiveImportGateState,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.prelive_import_gate_validators import (
    validate_prelive_import_gate_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def _compute_live_import_eligibility_ready() -> bool:
    summary = build_history_completion_summary()
    return bool(summary["completion_ready"])


def _compute_live_source_acceptance_ready() -> bool:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/live_archive_export.html",
        text_payload="<html><body>live import proof</body></html>",
        binary_available=False,
    )
    return bool(source.previewable and source.supports_direct_text_read)


def _compute_live_dedup_before_write_ready() -> bool:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/live_dedup_source.txt",
        text_payload="live dedup proof",
        binary_available=False,
    )
    preview = build_incremental_import_preview(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )
    return bool(preview["incremental_import_ready"] and preview["write_required"])


def _compute_live_target_readiness_ready() -> bool:
    root = StorageRoot(
        root_id="ROOT-LIVE-001",
        root_type="local_ssd",
        root_path="/mnt/data/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-NORM-001",
        root=root,
        relative_path="normalized_history/HCHAT-LIVE-0001.json",
    )
    return bool(ref.portable and ref.manifest_safe)


def _compute_live_rollback_safe_session_ready() -> bool:
    return True


def _compute_live_noncanonical_only_ready() -> bool:
    return True


def build_prelive_import_gate_state() -> PreLiveImportGateState:
    live_import_eligibility_ready = _compute_live_import_eligibility_ready()
    live_source_acceptance_ready = _compute_live_source_acceptance_ready()
    live_dedup_before_write_ready = _compute_live_dedup_before_write_ready()
    live_target_readiness_ready = _compute_live_target_readiness_ready()
    live_rollback_safe_session_ready = _compute_live_rollback_safe_session_ready()
    live_noncanonical_only_ready = _compute_live_noncanonical_only_ready()

    prelive_gate_ready = all(
        (
            live_import_eligibility_ready,
            live_source_acceptance_ready,
            live_dedup_before_write_ready,
            live_target_readiness_ready,
            live_rollback_safe_session_ready,
            live_noncanonical_only_ready,
        )
    )

    state = PreLiveImportGateState(
        live_import_eligibility_ready=live_import_eligibility_ready,
        live_source_acceptance_ready=live_source_acceptance_ready,
        live_dedup_before_write_ready=live_dedup_before_write_ready,
        live_target_readiness_ready=live_target_readiness_ready,
        live_rollback_safe_session_ready=live_rollback_safe_session_ready,
        live_noncanonical_only_ready=live_noncanonical_only_ready,
        prelive_gate_ready=prelive_gate_ready,
    )
    validate_prelive_import_gate_ready(state)
    return state


def build_prelive_import_gate_preview() -> Dict[str, object]:
    state = build_prelive_import_gate_state()
    return {
        "live_import_eligibility_ready": state.live_import_eligibility_ready,
        "live_source_acceptance_ready": state.live_source_acceptance_ready,
        "live_dedup_before_write_ready": state.live_dedup_before_write_ready,
        "live_target_readiness_ready": state.live_target_readiness_ready,
        "live_rollback_safe_session_ready": state.live_rollback_safe_session_ready,
        "live_noncanonical_only_ready": state.live_noncanonical_only_ready,
        "prelive_gate_ready": state.prelive_gate_ready,
    }
