from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_memory_classification_policy_contract,
)
from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE.memory_promotion_pipeline_models import (
    MemoryPromotionPipelineContract,
    MemoryPromotionPipelineEntry,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)


def build_memory_promotion_pipeline_contract() -> MemoryPromotionPipelineContract:
    """Build canonical memory promotion pipeline contract."""
    classification_policy = build_memory_classification_policy_contract()
    memory_registry = build_memory_registry_contract()

    policy_by_tier = {
        entry.memory_tier_id: entry for entry in classification_policy.entries
    }
    registry_by_tier = {
        entry.memory_tier_id: entry for entry in memory_registry.entries
    }

    entries = []

    promoted_tier_id = "memory_project_architecture"
    promoted_policy = policy_by_tier[promoted_tier_id]
    promoted_registry = registry_by_tier[promoted_tier_id]

    if "architecture_decision" not in promoted_policy.accepted_fact_classes:
        raise ValueError("architecture_decision must be accepted by foundational tier")

    if "roadmap_checkpoint" not in promoted_policy.accepted_fact_classes:
        raise ValueError("roadmap_checkpoint must be accepted by foundational tier")

    if "ru" not in promoted_registry.supported_languages:
        raise ValueError("ru must be supported by memory registry")

    if "en" not in promoted_registry.supported_languages:
        raise ValueError("en must be supported by memory registry")

    if "Cyrillic" not in promoted_registry.supported_scripts:
        raise ValueError("Cyrillic must be supported by memory registry")

    if "Latin" not in promoted_registry.supported_scripts:
        raise ValueError("Latin must be supported by memory registry")

    entries.append(
        MemoryPromotionPipelineEntry(
            module_slug="project_architecture",
            memory_tier_id="memory_project_architecture",
            input_event_id="event_architecture_decision_001",
            fact_class="architecture_decision",
            language_code="ru",
            script_name="Cyrillic",
            provenance_ref="prov_architecture_decision_001",
            classification_passed=True,
            summarization_performed=True,
            evidence_bound=True,
            deduplication_passed=True,
            conflict_check_performed=True,
            conflict_check_passed=True,
            final_disposition="promoted",
            archive_reason="",
            promoted_record_id="memrec_architecture_decision_001",
            archived_record_id="",
            description=(
                "Memory promotion pipeline promoted foundational architecture decision "
                "after classification, summarization, deduplication, and conflict check."
            ),
        )
    )

    entries.append(
        MemoryPromotionPipelineEntry(
            module_slug="project_architecture",
            memory_tier_id="memory_project_architecture",
            input_event_id="event_roadmap_checkpoint_001",
            fact_class="roadmap_checkpoint",
            language_code="en",
            script_name="Latin",
            provenance_ref="prov_roadmap_checkpoint_001",
            classification_passed=True,
            summarization_performed=True,
            evidence_bound=True,
            deduplication_passed=False,
            conflict_check_performed=False,
            conflict_check_passed=False,
            final_disposition="archived",
            archive_reason="duplicate_candidate",
            promoted_record_id="",
            archived_record_id="archive_roadmap_checkpoint_001",
            description=(
                "Memory promotion pipeline archived duplicate roadmap checkpoint before "
                "conflict check after deduplication failure."
            ),
        )
    )

    promoted_entries = sum(
        1 for entry in entries if entry.final_disposition == "promoted"
    )
    archived_entries = sum(
        1 for entry in entries if entry.final_disposition == "archived"
    )
    evidence_bound_entries = sum(
        1 for entry in entries if entry.evidence_bound
    )

    return MemoryPromotionPipelineContract(
        total_entries=len(entries),
        promoted_entries=promoted_entries,
        archived_entries=archived_entries,
        evidence_bound_entries=evidence_bound_entries,
        entries=tuple(entries),
    )
