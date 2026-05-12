from __future__ import annotations

import json
from pathlib import Path


PHASE_5_2_ACCEPTANCE = Path("docs/architecture/foundation/phase_5_2_final_dashboard_memory_map_acceptance_v1.md")
PHASE_6_0_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_0_product_ready_hardening_acceptance_v1.md")
PHASE_6_1_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_1_governance_federation_gap_pass_acceptance_v1.md")
PHASE_6_2_ACCEPTANCE = Path("docs/architecture/foundation/phase_6_2_proposal_audit_approval_spine_acceptance_v1.md")
CONSOLIDATED_AUDIT = Path("docs/architecture/roadmap_index/four_roadmap_consolidated_audit_v1.md")


def build_next_step_report() -> dict[str, object]:
    phase_6_2_closed = PHASE_6_2_ACCEPTANCE.exists()
    phase_6_1_closed = PHASE_6_1_ACCEPTANCE.exists()
    phase_6_0_closed = PHASE_6_0_ACCEPTANCE.exists()

    if phase_6_2_closed:
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
        do_not_start_yet = [
            "Sandbox / Simulation / Owner Review",
            "Self-expansion",
            "Productization",
        ]
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
        do_not_start_yet = [
            "Controlled Codegen Context",
            "Sandbox / Simulation / Owner Review",
            "Self-expansion",
            "Productization",
        ]
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
        do_not_start_yet = [
            "Proposal / Audit / Approval Spine",
            "Controlled Codegen Context",
            "Sandbox / Simulation / Owner Review",
            "Self-expansion",
            "Productization",
        ]
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
        do_not_start_yet = [
            "Proposal / Audit / Approval Spine",
            "Controlled Codegen Context",
            "Sandbox / Simulation / Owner Review",
            "Self-expansion",
            "Productization",
        ]

    report = {
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
        "next_step_ready": CONSOLIDATED_AUDIT.exists() and PHASE_5_2_ACCEPTANCE.exists(),
    }

    return report


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
