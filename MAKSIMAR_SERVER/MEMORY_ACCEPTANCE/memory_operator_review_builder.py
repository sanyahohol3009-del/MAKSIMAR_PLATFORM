from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_acceptance_gates import (
    build_memory_acceptance_gate_report,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_readiness_summary_builder import (
    build_memory_readiness_summary,
)


def build_memory_operator_review_package() -> Dict[str, object]:
    summary = build_memory_readiness_summary()
    gates = build_memory_acceptance_gate_report()

    review_items: Tuple[Dict[str, object], ...] = tuple(
        {
            "gate_id": gate.gate_id,
            "gate_name": gate.gate_name,
            "passed": gate.passed,
            "blocking": gate.blocking,
            "evidence_ref": gate.evidence_ref,
        }
        for gate in gates.gates
    )

    review_ready = (
        summary["readiness_ready"] is True
        and summary["operator_review_required"] is True
        and len(review_items) == gates.total_gates
    )

    return {
        "review_package_id": "memory_operator_review_package_phase_6_0_001",
        "review_ready": review_ready,
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "review_items": review_items,
        "risk_summary_required": True,
        "diff_preview_required": True,
        "dashboard_read_only": summary["dashboard_read_only"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
    }
