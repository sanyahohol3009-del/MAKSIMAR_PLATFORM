from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_retrieval_scope_gate_preview


def test_regulatory_retrieval_scope_gate_smoke() -> None:
    preview = build_regulatory_retrieval_scope_gate_preview()

    assert preview["preview_ready"] is True
    assert preview["route_count"] >= 3
    assert preview["tenant_scope_required"] is True
    assert preview["business_scope_required"] is True
    assert preview["jurisdiction_scope_required"] is True
    assert preview["source_scope_required"] is True
    assert preview["same_tenant_only"] is True
    assert preview["read_only"] is True
    assert preview["cross_tenant_retrieval_allowed"] is False
