from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


DisplayTargetId = Literal[
    "display_primary_operator",
    "display_secondary_diagnostics",
    "display_tertiary_expansion",
]

DisplayRole = Literal[
    "primary_operator",
    "diagnostics",
    "expansion",
]

DisplayZone = Literal[
    "left",
    "center",
    "right",
    "overlay",
]

DisplayTargetType = Literal[
    "physical_monitor",
    "logical_surface",
]


@dataclass(frozen=True, slots=True)
class DisplayTargetVocabularyEntry:
    """Canonical display target vocabulary entry."""

    display_target_id: DisplayTargetId
    display_role: DisplayRole
    display_zone: DisplayZone
    display_target_type: DisplayTargetType
    display_title: str
    description: str


@dataclass(frozen=True, slots=True)
class DisplayTargetVocabularyContract:
    """Canonical display target vocabulary / role contract."""

    total_entries: int
    physical_monitor_entries: int
    logical_surface_entries: int
    entries: tuple[DisplayTargetVocabularyEntry, ...]


def build_display_target_vocabulary_contract() -> DisplayTargetVocabularyContract:
    """Build canonical display target vocabulary / role contract."""
    entries = (
        DisplayTargetVocabularyEntry(
            display_target_id="display_primary_operator",
            display_role="primary_operator",
            display_zone="center",
            display_target_type="physical_monitor",
            display_title="Primary Operator Display",
            description="Canonical primary operator display target.",
        ),
        DisplayTargetVocabularyEntry(
            display_target_id="display_secondary_diagnostics",
            display_role="diagnostics",
            display_zone="right",
            display_target_type="physical_monitor",
            display_title="Secondary Diagnostics Display",
            description="Canonical diagnostics display target.",
        ),
        DisplayTargetVocabularyEntry(
            display_target_id="display_tertiary_expansion",
            display_role="expansion",
            display_zone="left",
            display_target_type="logical_surface",
            display_title="Tertiary Expansion Display",
            description="Canonical expandable logical display target.",
        ),
    )

    return DisplayTargetVocabularyContract(
        total_entries=len(entries),
        physical_monitor_entries=sum(
            1 for entry in entries if entry.display_target_type == "physical_monitor"
        ),
        logical_surface_entries=sum(
            1 for entry in entries if entry.display_target_type == "logical_surface"
        ),
        entries=entries,
    )
