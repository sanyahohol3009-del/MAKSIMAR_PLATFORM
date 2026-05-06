from __future__ import annotations

from typing import Literal, Tuple


TruthLevel = Literal[
    "raw_archive_fact",
    "validated_project_fact",
    "canonical_rule",
]

SUPPORTED_TRUTH_LEVELS: Tuple[TruthLevel, ...] = (
    "raw_archive_fact",
    "validated_project_fact",
    "canonical_rule",
)
