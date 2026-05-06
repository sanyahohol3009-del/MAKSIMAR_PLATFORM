from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True)
class IncrementalLiveImportResult:
    total_conversations_in_source: int
    existing_conversations: int
    new_conversations: int
    new_conversation_writes_required: int
    repeat_safe: bool
    incremental_ready: bool

    def __post_init__(self) -> None:
        total_conversations_in_source = _ensure_non_negative_int(
            self.total_conversations_in_source,
            "total_conversations_in_source",
        )
        existing_conversations = _ensure_non_negative_int(
            self.existing_conversations,
            "existing_conversations",
        )
        new_conversations = _ensure_non_negative_int(
            self.new_conversations,
            "new_conversations",
        )
        new_conversation_writes_required = _ensure_non_negative_int(
            self.new_conversation_writes_required,
            "new_conversation_writes_required",
        )

        if existing_conversations + new_conversations != total_conversations_in_source:
            raise ValueError(
                "existing_conversations + new_conversations must equal total_conversations_in_source",
            )

        if new_conversation_writes_required != new_conversations:
            raise ValueError(
                "new_conversation_writes_required must equal new_conversations",
            )

        if not self.repeat_safe:
            raise ValueError("repeat_safe must be True")

        if not self.incremental_ready:
            raise ValueError("incremental_ready must be True")
