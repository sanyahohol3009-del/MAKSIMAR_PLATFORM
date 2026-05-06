from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_builder import (
    build_end_to_end_dry_run_proof,
)


def test_end_to_end_route_order_smoke() -> None:
    proof = build_end_to_end_dry_run_proof()

    assert proof.import_session.source_id == proof.source.metadata.source_id
    assert proof.manifest.import_session_id == proof.import_session.import_session_id
    assert proof.normalized_record.storage_node_id == proof.portable_reference.storage_node_id
