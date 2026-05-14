from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.ROADMAP_CLOSURE.final_closure_preview_builder import (
    build_final_closure_preview,
)


def build_final_roadmap_closure_summary() -> Dict[str, object]:
    preview = build_final_closure_preview()

    return {
        "summary_id": "final_roadmap_closure_summary_memory_roadmap_v5_1_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": preview["roadmap_family"],
        "closed_phase": preview["closed_phase"],
        "next_step": preview["next_step"],
        "acceptance_doc_count": preview["acceptance"]["acceptance_doc_count"],
        "closed_block_count": preview["continuity"]["closed_block_count"],
        "recommended_next_entrypoint": preview["entrypoint"]["recommended_first"],
        "direct_core_write_allowed": preview["direct_core_write_allowed"],
        "auto_apply_allowed": preview["auto_apply_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
        "deployment_allowed_now": preview["deployment_allowed_now"],
        "external_release_allowed_now": preview["external_release_allowed_now"],
        "final_closure_ready": preview["final_closure_ready"],
    }
