from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract
from MAKSIMAR_CORE_LIB.memory_policy import build_governance_binding_contract
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE.memory_promotion_pipeline_contract import (
    build_memory_promotion_pipeline_contract,
)
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE.promotion_binding_models import (
    PromotionBindingContract,
    PromotionBindingEntry,
    safe_id_suffix,
)


def build_promotion_binding_contract() -> PromotionBindingContract:
    pipeline = build_memory_promotion_pipeline_contract()
    governance = build_governance_binding_contract()
    evidence = build_evidence_memory_contract()

    governance_by_module = {
        entry.module_slug: entry
        for entry in governance.entries
    }

    entries = tuple(
        PromotionBindingEntry(
            promotion_binding_id=(
                "promotion_binding_"
                f"{safe_id_suffix(entry.module_slug)}_"
                f"{safe_id_suffix(entry.input_event_id)}_"
                f"{safe_id_suffix('promoted' if entry.promoted_record_id else 'archived' if entry.archived_record_id else 'candidate')}"
            ),
            module_slug=entry.module_slug,
            memory_tier_id=entry.memory_tier_id,
            input_event_id=entry.input_event_id,
            evidence_records=evidence.total_records,
            promoted_entries=1 if entry.promoted_record_id else 0,
            archived_entries=1 if entry.archived_record_id else 0,
            evidence_bound=entry.evidence_bound
            and evidence.ready_records == evidence.total_records,
            classification_passed=entry.classification_passed,
            deduplication_passed=entry.deduplication_passed,
            conflict_check_passed=entry.conflict_check_passed,
            governance_bound=entry.module_slug in governance_by_module
            and governance_by_module[entry.module_slug].binding_ready,
            approval_required=(
                entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].approval_required
            ),
            auto_promotion_allowed=(
                entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].auto_promotion_allowed
            ),
            controlled_promotion_allowed=(
                entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].controlled_promotion_allowed
            ),
            read_only=(
                entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].read_only
            ),
            binding_status="ready_for_review",
            binding_ready=(
                entry.evidence_bound
                and entry.classification_passed
                and (entry.deduplication_passed or bool(entry.archived_record_id))
                and (entry.conflict_check_passed or bool(entry.archived_record_id))
                and entry.module_slug in governance_by_module
                and governance_by_module[entry.module_slug].binding_ready
                and governance_by_module[entry.module_slug].approval_required
                and not governance_by_module[entry.module_slug].auto_promotion_allowed
                and governance_by_module[entry.module_slug].controlled_promotion_allowed
                and governance_by_module[entry.module_slug].read_only
                and evidence.ready_records == evidence.total_records
                and evidence.conflict_detected_records == 0
            ),
            description=f"Promotion binding for {entry.module_slug}.",
        )
        for entry in pipeline.entries
    )

    return PromotionBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        evidence_bound_bindings=sum(1 for entry in entries if entry.evidence_bound),
        governance_bound_bindings=sum(1 for entry in entries if entry.governance_bound),
        approval_required_bindings=sum(1 for entry in entries if entry.approval_required),
        auto_promotion_allowed_bindings=sum(
            1 for entry in entries if entry.auto_promotion_allowed
        ),
        controlled_promotion_bindings=sum(
            1 for entry in entries if entry.controlled_promotion_allowed
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        promoted_entries=sum(entry.promoted_entries for entry in entries),
        archived_entries=sum(entry.archived_entries for entry in entries),
        entries=entries,
    )
