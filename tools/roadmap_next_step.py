from __future__ import annotations

import json
from pathlib import Path


PHASE_5_2_ACCEPTANCE = Path("docs/architecture/foundation/phase_5_2_final_dashboard_memory_map_acceptance_v1.md")
PHASE_6_0_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_0_product_ready_hardening_acceptance_v1.md")
PHASE_6_1_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_1_governance_federation_gap_pass_acceptance_v1.md")
PHASE_6_2_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_2_proposal_audit_approval_spine_acceptance_v1.md")
PHASE_6_3_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_3_controlled_codegen_context_acceptance_v1.md")
PHASE_6_4_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_4_sandbox_simulation_owner_review_acceptance_v1.md")
PHASE_6_5_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_5_bootstrapped_self_expansion_gate_acceptance_v1.md")
PHASE_6_6_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_6_client_metrics_learning_input_acceptance_v1.md")
PHASE_6_7_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_7_polyglot_model_worker_bridge_acceptance_v1.md")
PHASE_6_8_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_8_productization_sale_ready_sovereign_ai_acceptance_v1.md")
FINAL_CLOSURE = Path("docs/architecture/roadmap_index/memory_roadmap_v5_1_final_closure_v1.md")
REGULATORY_STEP_1_ACCEPTANCE = Path("docs/architecture/foundation/regulatory_track_entry_surface_inventory_v1.md")
REGULATORY_STEP_2_ACCEPTANCE = Path("docs/architecture/foundation/country_jurisdiction_registry_binding_v1.md")
REGULATORY_STEP_3_ACCEPTANCE = Path("docs/architecture/foundation/tenant_regulatory_scope_isolation_v1.md")
CONSOLIDATED_AUDIT = Path("docs/architecture/roadmap_index/four_roadmap_consolidated_audit_v1.md")


def build_next_step_report() -> dict[str, object]:
    regulatory_step_3_closed = REGULATORY_STEP_3_ACCEPTANCE.exists()
    regulatory_step_2_closed = REGULATORY_STEP_2_ACCEPTANCE.exists()
    regulatory_step_1_closed = REGULATORY_STEP_1_ACCEPTANCE.exists()
    final_closure_closed = FINAL_CLOSURE.exists()
    phase_6_8_closed = PHASE_6_8_ACCEPTANCE.exists()
    phase_6_7_closed = PHASE_6_7_ACCEPTANCE.exists()
    phase_6_6_closed = PHASE_6_6_ACCEPTANCE.exists()
    phase_6_5_closed = PHASE_6_5_ACCEPTANCE.exists()
    phase_6_4_closed = PHASE_6_4_ACCEPTANCE.exists()
    phase_6_3_closed = PHASE_6_3_ACCEPTANCE.exists()
    phase_6_2_closed = PHASE_6_2_ACCEPTANCE.exists()
    phase_6_1_closed = PHASE_6_1_ACCEPTANCE.exists()
    phase_6_0_closed = PHASE_6_0_ACCEPTANCE.exists()

    if regulatory_step_3_closed:
        current_closed_phase = "REGULATORY_MEMORY_FOUNDATION_STEP_3"
        next_step = "STEP 4 — Source Version / Effective Date / Precedence"
        next_folder = "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION/"
        why = "Tenant Regulatory Scope & Isolation is present; next step binds source version, effective date and legal precedence."
        required_first = [
            "regulatory source version models",
            "effective date precedence models",
            "legal precedence resolver",
            "source version precedence preview",
            "no regulatory source without version/effective_date",
        ]
        do_not_start_yet = [
            "Regulatory Conflict / Drift / Supersession",
            "Regulatory Update Approval Gate",
            "Final Closure",
        ]
    elif regulatory_step_2_closed:
        current_closed_phase = "REGULATORY_MEMORY_FOUNDATION_STEP_2"
        next_step = "STEP 3 — Tenant Regulatory Scope & Isolation"
        next_folder = "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION/"
        why = "Country / Jurisdiction Registry Binding is present; next step isolates tenant regulatory scopes."
        required_first = [
            "tenant regulatory scope models",
            "tenant isolation gate",
            "tenant country scope binding",
            "tenant regulatory preview",
            "no cross-tenant merge",
        ]
        do_not_start_yet = [
            "Source Version / Effective Date / Precedence",
            "Regulatory Update Approval Gate",
            "Final Closure",
        ]
    elif regulatory_step_3_closed:
        current_closed_phase = "REGULATORY_MEMORY_FOUNDATION_STEP_3"
        next_step = "STEP 4 — Source Version / Effective Date / Precedence"
        next_folder = "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION/"
        why = "Tenant Regulatory Scope & Isolation is present; next step binds source version, effective date and legal precedence."
        required_first = [
            "regulatory source version models",
            "effective date precedence models",
            "legal precedence resolver",
            "source version precedence preview",
            "no regulatory source without version/effective_date",
        ]
        do_not_start_yet = [
            "Regulatory Conflict / Drift / Supersession",
            "Regulatory Update Approval Gate",
            "Final Closure",
        ]
    elif regulatory_step_2_closed:
        current_closed_phase = "REGULATORY_MEMORY_FOUNDATION_STEP_2"
        next_step = "STEP 3 — Tenant Regulatory Scope & Isolation"
        next_folder = "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION/"
        why = "Country / Jurisdiction Registry Binding is present; next step isolates tenant regulatory scopes."
        required_first = [
            "tenant regulatory scope models",
            "tenant isolation gate",
            "tenant country scope binding",
            "tenant regulatory preview",
            "no cross-tenant merge",
        ]
        do_not_start_yet = [
            "Source Version / Effective Date / Precedence",
            "Regulatory Update Approval Gate",
            "Final Closure",
        ]
    elif regulatory_step_1_closed:
        current_closed_phase = "REGULATORY_MEMORY_FOUNDATION_STEP_1"
        next_step = "STEP 2 — Country / Jurisdiction Registry Binding"
        next_folder = "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION/"
        why = "Regulatory track entry and surface inventory are present; next step binds countries, jurisdictions and applicability."
        required_first = [
            "country registry models",
            "jurisdiction binding",
            "applicability builder",
            "jurisdiction preview",
            "no cross-jurisdiction merge",
        ]
        do_not_start_yet = [
            "Tenant Regulatory Scope & Isolation",
            "Source Version / Effective Date / Precedence",
            "Regulatory Update Approval Gate",
            "Final Closure",
        ]
    elif final_closure_closed:
        current_closed_phase = "memory_roadmap_v5_1_FINAL_CLOSURE"
        next_step = "Next Roadmap Selection"
        next_folder = "recommended: multi-tenant / multi-country regulatory memory foundation"
        why = "Memory roadmap v5.1 is closed; select the next roadmap entrypoint."
        required_first = [
            "choose next roadmap track",
            "run pre-step drift check",
            "keep memory_roadmap_v5_1 as closed reference",
            "do not reopen closed phases without explicit correction pass",
        ]
        do_not_start_yet = []
    elif phase_6_8_closed:
        current_closed_phase = "PHASE 6.8"
        next_step = "Roadmap v5.1 Final Closure / Continuity Savepoint"
        next_folder = "docs/architecture/roadmap_index/ + final closure summary"
        why = "Productization / Sale-Ready Sovereign AI is present; next step is final roadmap closure and continuity savepoint."
        required_first = [
            "final acceptance index",
            "final continuity summary",
            "current state handoff",
            "next roadmap entrypoint",
            "project memory savepoint after full roadmap",
        ]
        do_not_start_yet = []
    elif phase_6_7_closed:
        current_closed_phase = "PHASE 6.7"
        next_step = "Productization / Sale-Ready Sovereign AI"
        next_folder = "productization package over accepted roadmap v5.1 memory/governance/self-evolution surfaces"
        why = "Polyglot / Model / Worker Bridge is present; next roadmap block is sale-ready productization."
        required_first = [
            "product readiness model",
            "sale-ready package model",
            "deployment boundary review",
            "operator acceptance package",
            "no hidden autonomy",
        ]
        do_not_start_yet = []
    elif phase_6_6_closed:
        current_closed_phase = "PHASE 6.6"
        next_step = "Polyglot / Model / Worker Bridge"
        next_folder = "bridge package over model routing, language artifacts and worker boundaries"
        why = "Client Metrics / Learning Input is present; next roadmap block is polyglot/model/worker bridge before productization."
        required_first = [
            "artifact language models",
            "language bridge models",
            "model worker bridge models",
            "build/test bridge read model",
            "no productization yet",
        ]
        do_not_start_yet = ["Productization"]
    elif phase_6_5_closed:
        current_closed_phase = "PHASE 6.5"
        next_step = "Client Metrics / Learning Input"
        next_folder = "governed learning input over client metrics and accepted proposal/review surfaces"
        why = "Bootstrapped Self-Expansion Gate is present; next roadmap block is privacy-safe client metrics to learning input."
        required_first = [
            "client metrics filter models",
            "learning input pack models",
            "privacy and tenant boundary checks",
            "no automatic training mutation",
            "no productization yet",
        ]
        do_not_start_yet = ["Polyglot / Model / Worker Bridge", "Productization"]
    elif phase_6_4_closed:
        current_closed_phase = "PHASE 6.4"
        next_step = "Bootstrapped Self-Expansion Gate"
        next_folder = "controlled gate over proposal/audit/codegen/sandbox review surfaces"
        why = "Sandbox / Simulation / Owner Review is present; next roadmap block allows gap detection and proposal preparation only, still no productization."
        required_first = [
            "self-expansion readiness models",
            "self-expansion gate",
            "gap detection to proposal only",
            "no direct core write",
            "no productization",
        ]
        do_not_start_yet = ["Productization"]
    elif phase_6_3_closed:
        current_closed_phase = "PHASE 6.3"
        next_step = "Sandbox / Simulation / Owner Review"
        next_folder = "integration package over evolution_debug sandbox models and owner review package"
        why = "Controlled Codegen Context is present; next roadmap block validates generated artifacts through sandbox/simulation/owner review."
        required_first = [
            "sandbox binding models",
            "sandbox result reader",
            "simulation result reader",
            "owner review package builder",
            "still no self-expansion",
        ]
        do_not_start_yet = ["Self-expansion", "Productization"]
    elif phase_6_2_closed:
        current_closed_phase = "PHASE 6.2"
        next_step = "Controlled Codegen Context"
        next_folder = "integration package over proposal/audit spine and future codegen context surfaces"
        why = "Proposal / Audit / Approval Spine is present; next roadmap block is controlled codegen context, still without direct deploy."
        required_first = [
            "codegen intent models",
            "codegen boundary models",
            "codegen proposal builder",
            "codegen read summary",
            "no direct write to core",
        ]
        do_not_start_yet = ["Sandbox / Simulation / Owner Review", "Self-expansion", "Productization"]
    elif phase_6_1_closed:
        current_closed_phase = "PHASE 6.1"
        next_step = "Proposal / Audit / Approval Spine"
        next_folder = "integration package over existing evolution/proposal/audit surfaces"
        why = "Governance / Federation Gap Pass is present; next roadmap block is proposal/audit/approval visibility before controlled codegen."
        required_first = [
            "proposal inspector binding",
            "audit inspector binding",
            "approval read model",
            "proposal audit summary builder",
            "no code writing yet",
        ]
        do_not_start_yet = ["Controlled Codegen Context", "Sandbox / Simulation / Owner Review", "Self-expansion", "Productization"]
    elif phase_6_0_closed:
        current_closed_phase = "PHASE 6.0"
        next_step = "Governance / Federation Gap Pass"
        next_folder = "MAKSIMAR_CORE_LIB/memory_policy/ + existing memory governance surfaces"
        why = "PHASE 6.0 Product-Ready Hardening is present; next roadmap block is governance/federation gap verification before Proposal/Audit."
        required_first = [
            "trust scope gap check",
            "source priority gap check",
            "federation policy gap check",
            "tenant/personal separation gap check",
            "reuse existing governance bindings before creating anything new",
        ]
        do_not_start_yet = ["Proposal / Audit / Approval Spine", "Controlled Codegen Context", "Sandbox / Simulation / Owner Review", "Self-expansion", "Productization"]
    else:
        current_closed_phase = "PHASE 5.2"
        next_step = "PHASE 6.0 — Product-Ready Hardening"
        next_folder = "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/"
        why = "PHASE 5.2 Final Dashboard Memory Map is closed; next primary v5.1 block is product-ready hardening."
        required_first = [
            "memory acceptance gates",
            "memory write safety models",
            "operator review builder",
            "release candidate builder",
            "release preview builder",
        ]
        do_not_start_yet = ["Proposal / Audit / Approval Spine", "Controlled Codegen Context", "Sandbox / Simulation / Owner Review", "Self-expansion", "Productization"]

    return {
        "roadmap_family": "memory_roadmap_v5_1",
        "current_closed_phase": current_closed_phase,
        "next_step": next_step,
        "next_folder": next_folder,
        "why": why,
        "do_not_start_yet": do_not_start_yet,
        "required_first": required_first,
        "audit_doc_exists": CONSOLIDATED_AUDIT.exists(),
        "phase_5_2_acceptance_exists": PHASE_5_2_ACCEPTANCE.exists(),
        "phase_6_0_acceptance_exists": PHASE_6_0_ACCEPTANCE.exists(),
        "phase_6_1_acceptance_exists": PHASE_6_1_ACCEPTANCE.exists(),
        "phase_6_2_acceptance_exists": PHASE_6_2_ACCEPTANCE.exists(),
        "phase_6_3_acceptance_exists": PHASE_6_3_ACCEPTANCE.exists(),
        "phase_6_4_acceptance_exists": PHASE_6_4_ACCEPTANCE.exists(),
        "phase_6_5_acceptance_exists": PHASE_6_5_ACCEPTANCE.exists(),
        "phase_6_6_acceptance_exists": PHASE_6_6_ACCEPTANCE.exists(),
        "phase_6_7_acceptance_exists": PHASE_6_7_ACCEPTANCE.exists(),
        "phase_6_8_acceptance_exists": PHASE_6_8_ACCEPTANCE.exists(),
        "final_closure_exists": FINAL_CLOSURE.exists(),
        "regulatory_step_1_acceptance_exists": REGULATORY_STEP_1_ACCEPTANCE.exists(),
        "regulatory_step_2_acceptance_exists": REGULATORY_STEP_2_ACCEPTANCE.exists(),
        "regulatory_step_3_acceptance_exists": REGULATORY_STEP_3_ACCEPTANCE.exists(),
        "next_step_ready": CONSOLIDATED_AUDIT.exists() and PHASE_5_2_ACCEPTANCE.exists(),
    }


def main() -> int:
    report = build_next_step_report()

    print("===== MAKSIMAR ROADMAP NEXT STEP =====")
    print(f"roadmap_family: {report['roadmap_family']}")
    print(f"current_closed_phase: {report['current_closed_phase']}")
    print(f"next_step: {report['next_step']}")
    print(f"next_folder: {report['next_folder']}")
    print(f"why: {report['why']}")
    print("do_not_start_yet:")
    for item in report["do_not_start_yet"]:
        print(f"  - {item}")

    print("required_first:")
    for item in report["required_first"]:
        print(f"  - {item}")

    print("json:")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0 if report["next_step_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
