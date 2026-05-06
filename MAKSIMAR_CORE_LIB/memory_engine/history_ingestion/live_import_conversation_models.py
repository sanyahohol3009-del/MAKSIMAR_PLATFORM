from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True)
class LiveImportConversation:
    conversation_id: str
    source_file_path: str
    message_count: int
    message_node_ids: Tuple[str, ...]
    primary_bucket_path: str
    live_import_ready: bool

    def __post_init__(self) -> None:
        conversation_id = _ensure_non_empty_str(
            self.conversation_id,
            "conversation_id",
        )
        source_file_path = _ensure_non_empty_str(
            self.source_file_path,
            "source_file_path",
        )
        primary_bucket_path = _ensure_non_empty_str(
            self.primary_bucket_path,
            "primary_bucket_path",
        )
        message_count = _ensure_non_negative_int(
            self.message_count,
            "message_count",
        )

        if message_count == 0:
            raise ValueError("message_count must be >= 1")

        if not self.message_node_ids:
            raise ValueError("message_node_ids must not be empty")

        if len(self.message_node_ids) != message_count:
            raise ValueError(
                "len(message_node_ids) must equal message_count",
            )

        for node_id in self.message_node_ids:
            _ensure_non_empty_str(node_id, "message_node_id")

        if not self.live_import_ready:
            raise ValueError("live_import_ready must be True")

        object.__setattr__(self, "conversation_id", conversation_id)
        object.__setattr__(self, "source_file_path", source_file_path)
        object.__setattr__(self, "primary_bucket_path", primary_bucket_path)
        object.__setattr__(self, "message_count", message_count)


@dataclass(frozen=True)
class LiveImportSession:
    session_id: str
    source_manifest_path: str
    source_conversations_path: str
    conversation_count: int
    attachment_roots: Tuple[str, ...]
    by_conversation_ready: bool
    whole_file_ready: bool

    def __post_init__(self) -> None:
        session_id = _ensure_non_empty_str(self.session_id, "session_id")
        source_manifest_path = _ensure_non_empty_str(
            self.source_manifest_path,
            "source_manifest_path",
        )
        source_conversations_path = _ensure_non_empty_str(
            self.source_conversations_path,
            "source_conversations_path",
        )
        conversation_count = _ensure_non_negative_int(
            self.conversation_count,
            "conversation_count",
        )

        if conversation_count == 0:
            raise ValueError("conversation_count must be >= 1")

        if not self.attachment_roots:
            raise ValueError("attachment_roots must not be empty")

        for path in self.attachment_roots:
            _ensure_non_empty_str(path, "attachment_root")

        if not self.by_conversation_ready:
            raise ValueError("by_conversation_ready must be True")

        if not self.whole_file_ready:
            raise ValueError("whole_file_ready must be True")

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "source_manifest_path", source_manifest_path)
        object.__setattr__(
            self,
            "source_conversations_path",
            source_conversations_path,
        )
        object.__setattr__(self, "conversation_count", conversation_count)
