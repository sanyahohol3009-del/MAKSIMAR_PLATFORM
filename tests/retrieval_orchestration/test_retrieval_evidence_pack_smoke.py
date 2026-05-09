from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_default_retrieval_request,
    build_default_retrieval_source_bindings,
    build_retrieval_evidence_pack,
)


def test_retrieval_evidence_pack_smoke() -> None:
    request = build_default_retrieval_request()
    sources = build_default_retrieval_source_bindings()
    evidence_pack = build_retrieval_evidence_pack(request, sources)

    assert evidence_pack.total_items == len(evidence_pack.evidence_items)
    assert evidence_pack.citation_required_items == evidence_pack.total_items
    assert evidence_pack.total_items <= request.max_results
