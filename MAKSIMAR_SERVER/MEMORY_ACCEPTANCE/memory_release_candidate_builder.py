from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_operator_review_builder import (
    build_memory_operator_review_package,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_readiness_summary_builder import (
    build_memory_readiness_summary,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_write_safety_models import (
    build_memory_write_safety_policy,
)


def build_memory_release_candidate() -> Dict[str, object]:
    summary = build_memory_readiness_summary()
    review = build_memory_operator_review_package()
    write_policy = build_memory_write_safety_policy()

    release_candidate_ready = (
        summary["readiness_ready"] is True
        and review["review_ready"] is True
        and write_policy.policy_ready
        and review["operator_approval_required"] is True
        and review["operator_approval_granted"] is False
    )

    return {
        "release_candidate_id": "memory_release_candidate_phase_6_0_001",
        "release_candidate_ready": release_candidate_ready,
        "release_type": "memory_product_ready_candidate",
        "source_summary_id": summary["summary_id"],
        "operator_review_package_id": review["review_package_id"],
        "write_policy_id": write_policy.policy_id,
        "release_allowed_without_operator_approval": False,
        "canonical_promotion_allowed": False,
        "release_preview_required": True,
        "rollback_reference_required": True,
        "dashboard_read_only": summary["dashboard_read_only"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
    }
