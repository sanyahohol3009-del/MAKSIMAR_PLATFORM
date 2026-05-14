from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.PRODUCTIZATION.productization_preview_builder import build_productization_preview


def build_productization_summary() -> Dict[str, object]:
    preview = build_productization_preview()

    return {
        "summary_id": "productization_summary_phase_6_8_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": preview["roadmap_family"],
        "phase_id": preview["phase_id"],
        "track_scope": preview["track_scope"],
        "sale_ready_claim_allowed": preview["sale_ready_claim_allowed"],
        "operator_approval_required": preview["operator_approval_required"],
        "operator_approval_granted": preview["operator_approval_granted"],
        "hidden_autonomy_allowed": preview["hidden_autonomy_allowed"],
        "direct_core_write_allowed": preview["direct_core_write_allowed"],
        "auto_apply_allowed": preview["auto_apply_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
        "deployment_allowed_now": preview["deployment_allowed_now"],
        "external_release_allowed_now": preview["external_release_allowed_now"],
        "roadmap_v5_1_closure_allowed_next": preview["roadmap_v5_1_closure_allowed_next"],
    }
