from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_tenant_country_scope_binding_preview


def test_tenant_country_scope_binding_smoke() -> None:
    preview = build_tenant_country_scope_binding_preview()

    assert preview["preview_ready"] is True
    assert preview["tenant_count"] >= 2
    assert preview["country_count"] >= 2
    assert preview["jurisdiction_count"] >= 2
    assert preview["tenant_bound"] is True
    assert preview["jurisdiction_bound"] is True
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
