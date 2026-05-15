from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_cross_tenant_leak_guard_preview


def test_cross_tenant_leak_guard_smoke() -> None:
    preview = build_cross_tenant_leak_guard_preview()

    assert preview["preview_ready"] is True
    assert preview["checked_route_count"] >= 3
    assert preview["tenant_count"] >= 2
    assert preview["leak_detected"] is False
    assert "deny_cross_tenant" in preview["blocked_decisions"]
    assert preview["cross_tenant_retrieval_allowed"] is False
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["auto_routing_merge_allowed"] is False
