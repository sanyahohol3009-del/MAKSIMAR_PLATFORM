from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    EvidenceSourceChainEntry,
)


def test_evidence_source_chain_models_smoke() -> None:
    entry = EvidenceSourceChainEntry(
        chain_id="evidence_chain_history_ingestion",
        evidence_id="evidence_history_ingestion",
        source_id="retrieval_source_history_ingestion",
        source_layer="history_ingestion",
        artifact_ref="artifact://retrieval/history_ingestion/preview",
        citation_required=True,
        conflict_marker="",
        source_bound=True,
        provenance_bound=True,
        trace_bound=True,
        dashboard_visible=True,
        chain_ready=True,
    )

    assert entry.chain_ready is True
    assert entry.citation_required is True
    assert entry.conflict_marker == ""
