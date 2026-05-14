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

    if report.get("regulatory_step_3_acceptance_exists") is True:
        assert report["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_STEP_3"
        assert report["next_step"] == "STEP 4 — Source Version / Effective Date / Precedence"
    elif report.get("regulatory_step_2_acceptance_exists") is True:
        assert report["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_STEP_2"
        assert report["next_step"] == "STEP 3 — Tenant Regulatory Scope & Isolation"
    elif report.get("regulatory_step_3_acceptance_exists") is True:
        assert report["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_STEP_3"
        assert report["next_step"] == "STEP 4 — Source Version / Effective Date / Precedence"
    elif report.get("regulatory_step_2_acceptance_exists") is True:
        assert report["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_STEP_2"
        assert report["next_step"] == "STEP 3 — Tenant Regulatory Scope & Isolation"
    elif report.get("regulatory_step_1_acceptance_exists") is True:
        assert report["current_closed_phase"] == "REGULATORY_MEMORY_FOUNDATION_STEP_1"
        assert report["next_step"] == "STEP 2 — Country / Jurisdiction Registry Binding"
    elif report.get("final_closure_exists") is True:
        assert report["current_closed_phase"] == "memory_roadmap_v5_1_FINAL_CLOSURE"
        assert report["next_step"] == "Next Roadmap Selection"
    elif report["phase_6_8_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.8"
        assert report["next_step"] == "Roadmap v5.1 Final Closure / Continuity Savepoint"
    elif report["phase_6_7_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.7"
        assert report["next_step"] == "Productization / Sale-Ready Sovereign AI"
    elif report["phase_6_6_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.6"
        assert report["next_step"] == "Polyglot / Model / Worker Bridge"
    elif report["phase_6_5_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.5"
        assert report["next_step"] == "Client Metrics / Learning Input"
    elif report["phase_6_4_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.4"
        assert report["next_step"] == "Bootstrapped Self-Expansion Gate"
    elif report["phase_6_3_acceptance_exists"] is True:
        assert report["current_closed_phase"] == "PHASE 6.3"
        assert report["next_step"] == "Sandbox / Simulation / Owner Review"
    elif report["phase_6_2_acceptance_exists"] is True:
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
