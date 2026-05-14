from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_track_preview_builder import (
    build_regulatory_track_entry_preview,
)


def build_regulatory_track_entry_summary() -> Dict[str, object]:
    preview = build_regulatory_track_entry_preview()

    return {
        "summary_id": "regulatory_track_entry_summary_step_1_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": preview["roadmap_family"],
        "track_id": preview["track_id"],
        "current_step": preview["current_step"],
        "next_step": preview["next_step"],
        "stage_count": preview["stage_count"],
        "rule_count": preview["rule_count"],
        "total_required_surfaces": preview["surface_inventory"]["total_required_surfaces"],
        "missing_surfaces": preview["surface_inventory"]["missing_surfaces"],
        "memory_v5_1_closed_reference": preview["memory_v5_1_closed_reference"],
        "reopen_memory_v5_1_allowed": preview["reopen_memory_v5_1_allowed"],
        "no_second_memory_world": preview["no_second_memory_world"],
        "mempalace_source_of_truth_allowed": preview["mempalace_source_of_truth_allowed"],
        "cross_tenant_merge_allowed": preview["cross_tenant_merge_allowed"],
        "cross_jurisdiction_merge_allowed": preview["cross_jurisdiction_merge_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
        "direct_core_write_allowed": preview["direct_core_write_allowed"],
        "deployment_allowed_now": preview["deployment_allowed_now"],
    }
