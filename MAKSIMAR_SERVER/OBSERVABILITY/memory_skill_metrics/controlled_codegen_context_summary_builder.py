from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_preview_builder import build_codegen_preview


def build_controlled_codegen_context_summary() -> Dict[str, object]:
    preview = build_codegen_preview()
    summary = preview["summary"]

    return {
        "summary_id": "controlled_codegen_context_summary_phase_6_3_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": summary["roadmap_family"],
        "phase_id": summary["phase_id"],
        "track_scope": summary["track_scope"],
        "existing_surfaces_reused": summary["existing_surfaces_reused"],
        "intent_models_ready": summary["intent_models_ready"],
        "boundary_models_ready": summary["boundary_models_ready"],
        "artifact_context_ready": summary["artifact_context_ready"],
        "proposal_package_ready": summary["proposal_package_ready"],
        "operator_preview_required": summary["operator_preview_required"],
        "direct_core_write_allowed": summary["direct_core_write_allowed"],
        "deployment_allowed": summary["deployment_allowed"],
        "sandbox_execution_allowed_now": summary["sandbox_execution_allowed_now"],
        "sandbox_owner_review_allowed_next": summary["sandbox_owner_review_allowed_next"],
        "self_expansion_allowed_now": summary["self_expansion_allowed_now"],
        "productization_allowed_now": summary["productization_allowed_now"],
    }
