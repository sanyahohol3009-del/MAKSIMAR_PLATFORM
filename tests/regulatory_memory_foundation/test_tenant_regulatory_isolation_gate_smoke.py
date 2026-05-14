from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_tenant_regulatory_isolation_preview


def test_tenant_regulatory_isolation_gate_smoke() -> None:
    preview = build_tenant_regulatory_isolation_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_surfaces"] == ()
    assert preview["tenant_isolation_required"] is True
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["cross_tenant_read_allowed"] is False
    assert preview["cross_jurisdiction_merge_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
