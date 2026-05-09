from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE.memory_promotion_pipeline_contract import (
    build_memory_promotion_pipeline_contract,
)
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE.promotion_candidate_builder import (
    build_promotion_binding_contract,
)


def build_promotion_summary() -> Dict[str, object]:
    pipeline = build_memory_promotion_pipeline_contract()
    binding = build_promotion_binding_contract()

    summary_ready = (
        binding.ready_bindings == binding.total_bindings
        and binding.evidence_bound_bindings == binding.total_bindings
        and binding.governance_bound_bindings == binding.total_bindings
        and binding.approval_required_bindings == binding.total_bindings
        and binding.auto_promotion_allowed_bindings == 0
        and binding.controlled_promotion_bindings == binding.total_bindings
        and binding.read_only_bindings == binding.total_bindings
    )

    return {
        "pipeline_total_entries": pipeline.total_entries,
        "pipeline_promoted_entries": pipeline.promoted_entries,
        "pipeline_archived_entries": pipeline.archived_entries,
        "pipeline_evidence_bound_entries": pipeline.evidence_bound_entries,
        "promotion_binding_entries": binding.total_bindings,
        "promotion_ready_bindings": binding.ready_bindings,
        "evidence_bound_bindings": binding.evidence_bound_bindings,
        "governance_bound_bindings": binding.governance_bound_bindings,
        "approval_required_bindings": binding.approval_required_bindings,
        "auto_promotion_allowed_bindings": binding.auto_promotion_allowed_bindings,
        "controlled_promotion_bindings": binding.controlled_promotion_bindings,
        "read_only_bindings": binding.read_only_bindings,
        "promoted_entries": binding.promoted_entries,
        "archived_entries": binding.archived_entries,
        "summary_ready": summary_ready,
    }
