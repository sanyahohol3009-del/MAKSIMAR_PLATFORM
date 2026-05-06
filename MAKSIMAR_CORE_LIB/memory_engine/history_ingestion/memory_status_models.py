from __future__ import annotations

from typing import Literal, Tuple


MemoryStatus = Literal[
    "draft",
    "validated",
    "deprecated",
]

SUPPORTED_MEMORY_STATUSES: Tuple[MemoryStatus, ...] = (
    "draft",
    "validated",
    "deprecated",
)
