from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_routing_preview


def test_regulatory_routing_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/regulatory_memory_routing_no_cross_tenant_leak_v1.md")
    preview = build_regulatory_routing_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 8 — Regulatory Routing / No Cross-Tenant Leak"
    assert preview["next_step"] == "STEP 9 — Regulatory Memory Final Closure"
    assert preview["route_count"] >= 3
    assert preview["same_tenant_only"] is True
    assert preview["read_only"] is True
    assert preview["leak_detected"] is False
    assert preview["cross_tenant_retrieval_allowed"] is False
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["cross_jurisdiction_merge_allowed"] is False
    assert preview["auto_routing_merge_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False
