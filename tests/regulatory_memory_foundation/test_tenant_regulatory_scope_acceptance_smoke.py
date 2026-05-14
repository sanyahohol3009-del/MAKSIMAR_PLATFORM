from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_tenant_regulatory_scope_preview


def test_tenant_regulatory_scope_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/tenant_regulatory_scope_isolation_v1.md")
    preview = build_tenant_regulatory_scope_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 3 — Tenant Regulatory Scope & Isolation"
    assert preview["next_step"] == "STEP 4 — Source Version / Effective Date / Precedence"
    assert preview["tenant_id_required"] is True
    assert preview["tenant_isolation_required"] is True
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["cross_tenant_read_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False
