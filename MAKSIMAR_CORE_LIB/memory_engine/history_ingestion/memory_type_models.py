from __future__ import annotations

from typing import Literal, Tuple


MemoryType = Literal[
    "architecture_decision",
    "incident",
    "roadmap_checkpoint",
    "history_chat_unit",
    "history_message_unit",
    "import_session",
    "storage_node",
    "relation_edge",
]

SUPPORTED_MEMORY_TYPES: Tuple[MemoryType, ...] = (
    "architecture_decision",
    "incident",
    "roadmap_checkpoint",
    "history_chat_unit",
    "history_message_unit",
    "import_session",
    "storage_node",
    "relation_edge",
)
