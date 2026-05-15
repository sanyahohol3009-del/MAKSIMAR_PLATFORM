from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_memory_final_closure_preview


def test_regulatory_memory_final_closure_builder_smoke() -> None:
    preview = build_regulatory_memory_final_closure_preview()

    assert preview["preview_ready"] is True
    assert preview["closure_ready"] is True
    assert preview["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_FINAL_CLOSURE"
    assert preview["next_step"] == "Memory Foundation Complete / Next Roadmap Selection"
    assert preview["memory_foundation_domain_count"] == 9
    assert "regulatory_memory" in preview["memory_foundation_domains"]
    assert "audit_approval_memory" in preview["memory_foundation_domains"]
