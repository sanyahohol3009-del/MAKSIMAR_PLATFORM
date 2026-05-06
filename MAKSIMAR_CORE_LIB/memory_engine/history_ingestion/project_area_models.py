from __future__ import annotations

from typing import Literal, Tuple


ProjectArea = Literal[
    "runtime",
    "oob_dashboard",
    "truth_feed",
    "testing",
    "roadmap",
    "memory",
    "history_ingestion",
    "storage",
]

SUPPORTED_PROJECT_AREAS: Tuple[ProjectArea, ...] = (
    "runtime",
    "oob_dashboard",
    "truth_feed",
    "testing",
    "roadmap",
    "memory",
    "history_ingestion",
    "storage",
)
