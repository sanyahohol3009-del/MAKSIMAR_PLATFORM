from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_models import (
    DisplayTargetEntry,
    DisplayTargetVocabularyContract,
)


def build_display_target_vocabulary_contract() -> DisplayTargetVocabularyContract:
    """Build the canonical display target vocabulary contract."""
    entries = (
        DisplayTargetEntry(
            display_target_id="display_foundation_primary",
            display_role="foundation_primary_display",
            display_zone="foundation_main_zone",
            description="Primary display target for foundation monitoring panels.",
        ),
        DisplayTargetEntry(
            display_target_id="display_foundation_secondary",
            display_role="foundation_secondary_display",
            display_zone="foundation_secondary_zone",
            description="Secondary display target for foundation observability panels.",
        ),
        DisplayTargetEntry(
            display_target_id="display_operator_interaction",
            display_role="operator_interaction_display",
            display_zone="operator_interaction_zone",
            description="Display target for operator interaction panels.",
        ),
    )

    return DisplayTargetVocabularyContract(entries=entries)
