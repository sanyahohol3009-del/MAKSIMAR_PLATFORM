from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_operator_review_builder import (
    build_memory_operator_review_package,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_readiness_summary_builder import (
    build_memory_readiness_summary,
)
from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE.memory_release_candidate_builder import (
    build_memory_release_candidate,
)


def build_memory_release_preview() -> Dict[str, object]:
    summary = build_memory_readiness_summary()
    review = build_memory_operator_review_package()
    candidate = build_memory_release_candidate()

    preview_path = (
        "phase_5_2_final_memory_map",
        "phase_6_0_acceptance_gates",
        "phase_6_0_write_safety",
        "phase_6_0_operator_review",
        "phase_6_0_release_candidate",
        "phase_6_0_release_preview",
    )

    release_preview_ready = (
        candidate["release_candidate_ready"] is True
        and review["review_ready"] is True
        and summary["readiness_ready"] is True
        and candidate["release_preview_required"] is True
        and candidate["release_allowed_without_operator_approval"] is False
        and candidate["canonical_promotion_allowed"] is False
    )

    return {
        "release_preview_id": "memory_release_preview_phase_6_0_001",
        "release_preview_ready": release_preview_ready,
        "memory_product_ready": release_preview_ready,
        "preview_path": preview_path,
        "release_candidate_id": candidate["release_candidate_id"],
        "operator_review_package_id": review["review_package_id"],
        "release_allowed_without_operator_approval": candidate["release_allowed_without_operator_approval"],
        "canonical_promotion_allowed": candidate["canonical_promotion_allowed"],
        "rollback_reference_required": candidate["rollback_reference_required"],
        "dashboard_read_only": summary["dashboard_read_only"],
        "duplicate_write_allowed": summary["duplicate_write_allowed"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
    }
