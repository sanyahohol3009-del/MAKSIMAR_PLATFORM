from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_owner_review_preview_builder import (
    build_sandbox_owner_review_preview,
)


def build_sandbox_owner_review_summary() -> Dict[str, object]:
    preview = build_sandbox_owner_review_preview()

    return {
        "summary_id": "sandbox_owner_review_summary_phase_6_4_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": "memory_roadmap_v5_1",
        "phase_id": "PHASE 6.4",
        "track_scope": "sandbox_simulation_owner_review",
        "sandbox_binding_ready": preview["sandbox_binding"]["sandbox_binding_ready"],
        "sandbox_result_reader_ready": preview["sandbox_result"]["sandbox_result_reader_ready"],
        "simulation_result_reader_ready": preview["simulation_result"]["simulation_result_reader_ready"],
        "evaluation_result_reader_ready": preview["evaluation_result"]["evaluation_result_reader_ready"],
        "owner_review_package_ready": preview["owner_review"]["owner_review_package_ready"],
        "owner_review_required": preview["owner_review"]["owner_review_required"],
        "owner_approval_required": preview["owner_review"]["owner_approval_required"],
        "owner_approval_granted": preview["owner_review"]["owner_approval_granted"],
        "direct_core_write_allowed": preview["direct_core_write_allowed"],
        "deployment_allowed": preview["deployment_allowed"],
        "auto_apply_allowed": preview["auto_apply_allowed"],
        "self_expansion_allowed_now": preview["self_expansion_allowed_now"],
        "productization_allowed_now": preview["productization_allowed_now"],
        "self_expansion_allowed_next": preview["self_expansion_allowed_next"],
    }
