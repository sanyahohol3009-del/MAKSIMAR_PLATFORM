from __future__ import annotations

from pathlib import Path

from tools.roadmap_next_step import build_next_step_report


def test_four_roadmap_consolidated_audit_doc_exists() -> None:
    doc = Path("docs/architecture/roadmap_index/four_roadmap_consolidated_audit_v1.md")
    text = doc.read_text(encoding="utf-8")

    assert "official_master_roadmap_v5_1_corrected_full_printable" in text
    assert "master_roadmap_v5_memory_skill_rag_registry_display_self_evolution" in text
    assert "master_roadmap_v4_global_memory_registry_dashboard_product" in text
    assert "maksimar_jarvis_master_roadmap_print_version" in text
    assert "PHASE 6.0 — Product-Ready Hardening" in text


def test_roadmap_next_step_report_smoke() -> None:
    report = build_next_step_report()

    assert report["roadmap_family"] == "memory_roadmap_v5_1"
    assert report["next_step_ready"] is True

    if report["phase_6_2_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.2"
        assert report["next_step"] == "Controlled Codegen Context"
    elif report["phase_6_1_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.1"
        assert report["next_step"] == "Proposal / Audit / Approval Spine"
    elif report["phase_6_0_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.0"
        assert report["next_step"] == "Governance / Federation Gap Pass"
    else:
        assert report["current_closed_phase"] == "PHASE 5.2"
        assert report["next_step"] == "PHASE 6.0 — Product-Ready Hardening"
