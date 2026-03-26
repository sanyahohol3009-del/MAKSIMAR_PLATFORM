from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_memory_classification_policy_contract,
)
from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION.memory_conflict_resolution_models import (
    MemoryConflictResolutionContract,
    MemoryConflictResolutionEntry,
)
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_memory_promotion_pipeline_contract,
)


def build_memory_conflict_resolution_contract() -> MemoryConflictResolutionContract:
    """Build canonical memory conflict resolution contract."""
    classification_policy = build_memory_classification_policy_contract()
    promotion_pipeline = build_memory_promotion_pipeline_contract()

    policy_by_tier = {
        entry.memory_tier_id: entry for entry in classification_policy.entries
    }
    promoted_by_record_id = {
        entry.promoted_record_id: entry
        for entry in promotion_pipeline.entries
        if entry.promoted_record_id != ""
    }

    foundational_tier_id = "memory_project_architecture"
    foundational_policy = policy_by_tier[foundational_tier_id]

    if foundational_policy.conflict_mode != "conflict_check_required":
        raise ValueError("Foundational memory tier must require conflict checks")

    if "architecture_decision" not in foundational_policy.accepted_fact_classes:
        raise ValueError(
            "Foundational memory tier must accept architecture_decision fact class"
        )

    if "roadmap_checkpoint" not in foundational_policy.accepted_fact_classes:
        raise ValueError(
            "Foundational memory tier must accept roadmap_checkpoint fact class"
        )

    base_record = promoted_by_record_id["memrec_architecture_decision_001"]

    entries = (
        MemoryConflictResolutionEntry(
            module_slug="project_architecture",
            memory_tier_id="memory_project_architecture",
            conflict_case_id="conflict_architecture_decision_002",
            incoming_event_id="event_architecture_decision_002",
            existing_record_id=base_record.promoted_record_id,
            fact_class="architecture_decision",
            conflict_kind="revision_conflict",
            incoming_evidence_rank=9,
            existing_evidence_rank=7,
            proposal_generated=True,
            approval_required=True,
            approval_ticket_id="approval_architecture_decision_002",
            approval_granted=True,
            conflict_marker_id="conflictmark_architecture_decision_002",
            version_incremented=True,
            resolution_strategy="promote_new_version",
            resolution_status="resolved",
            resolved_record_id="memrec_architecture_decision_002",
            archived_record_id="archive_architecture_decision_001",
            description=(
                "Conflict resolution promoted a stronger architecture decision as a new "
                "version after proposal generation and explicit approval."
            ),
        ),
        MemoryConflictResolutionEntry(
            module_slug="project_architecture",
            memory_tier_id="memory_project_architecture",
            conflict_case_id="conflict_architecture_decision_003",
            incoming_event_id="event_architecture_decision_003",
            existing_record_id="memrec_architecture_decision_002",
            fact_class="architecture_decision",
            conflict_kind="evidence_conflict",
            incoming_evidence_rank=6,
            existing_evidence_rank=9,
            proposal_generated=True,
            approval_required=True,
            approval_ticket_id="approval_architecture_decision_003",
            approval_granted=True,
            conflict_marker_id="conflictmark_architecture_decision_003",
            version_incremented=False,
            resolution_strategy="keep_existing_record",
            resolution_status="resolved",
            resolved_record_id="memrec_architecture_decision_002",
            archived_record_id="archive_architecture_decision_003",
            description=(
                "Conflict resolution kept the stronger existing architecture decision "
                "and archived the weaker incoming candidate after approval."
            ),
        ),
    )

    promote_new_version_entries = sum(
        1 for entry in entries if entry.resolution_strategy == "promote_new_version"
    )
    keep_existing_entries = sum(
        1 for entry in entries if entry.resolution_strategy == "keep_existing_record"
    )
    approval_required_entries = sum(
        1 for entry in entries if entry.approval_required
    )

    return MemoryConflictResolutionContract(
        total_entries=len(entries),
        promote_new_version_entries=promote_new_version_entries,
        keep_existing_entries=keep_existing_entries,
        approval_required_entries=approval_required_entries,
        entries=entries,
    )
