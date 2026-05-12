from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_acceptance_gates import (
    build_memory_acceptance_gate_report,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_acceptance_models import (
    build_memory_acceptance_contract,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_write_safety_models import (
    build_memory_write_safety_policy,
)


def build_memory_readiness_summary() -> Dict[str, object]:
    contract = build_memory_acceptance_contract()
    gates = build_memory_acceptance_gate_report()
    write_policy = build_memory_write_safety_policy()

    readiness_ready = (
        contract.acceptance_ready
        and gates.acceptance_gates_ready
        and write_policy.policy_ready
        and gates.failed_gates == 0
        and contract.canonical_write_allowed is False
        and contract.runtime_mutation_allowed is False
    )

    return {
        "summary_id": "memory_readiness_summary_phase_6_0_001",
        "roadmap_family": contract.roadmap_family,
        "phase_id": contract.phase_id,
        "track_scope": contract.track_scope,
        "readiness_ready": readiness_ready,
        "criteria_count": len(contract.criteria),
        "total_gates": gates.total_gates,
        "passed_gates": gates.passed_gates,
        "failed_gates": gates.failed_gates,
        "write_policy_ready": write_policy.policy_ready,
        "dashboard_read_only": contract.dashboard_read_only,
        "duplicate_write_allowed": contract.duplicate_write_allowed,
        "canonical_write_allowed": contract.canonical_write_allowed,
        "runtime_mutation_allowed": contract.runtime_mutation_allowed,
        "operator_review_required": contract.operator_review_required,
        "release_preview_required": contract.release_preview_required,
    }
