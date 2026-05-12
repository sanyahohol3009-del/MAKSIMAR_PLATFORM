from __future__ import annotations

import json
from pathlib import Path


NEXT_STEP = {
    "roadmap_family": "memory_roadmap_v5_1",
    "current_closed_phase": "PHASE 5.2",
    "next_step": "PHASE 6.0 — Product-Ready Hardening",
    "next_folder": "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/",
    "why": "PHASE 5.2 Final Dashboard Memory Map is closed; next primary v5.1 block is product-ready hardening.",
    "do_not_start_yet": [
        "Proposal / Audit / Approval Spine",
        "Controlled Codegen Context",
        "Sandbox / Simulation / Owner Review",
        "Self-expansion",
        "Productization",
    ],
    "required_first": [
        "memory acceptance gates",
        "memory write safety models",
        "operator review builder",
        "release candidate builder",
        "release preview builder",
    ],
}


def build_next_step_report() -> dict[str, object]:
    audit_doc = Path("docs/architecture/roadmap_index/four_roadmap_consolidated_audit_v1.md")
    phase_5_2_doc = Path("docs/architecture/foundation/phase_5_2_final_dashboard_memory_map_acceptance_v1.md")

    return {
        **NEXT_STEP,
        "audit_doc_exists": audit_doc.exists(),
        "phase_5_2_acceptance_exists": phase_5_2_doc.exists(),
        "next_step_ready": audit_doc.exists() and phase_5_2_doc.exists(),
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
