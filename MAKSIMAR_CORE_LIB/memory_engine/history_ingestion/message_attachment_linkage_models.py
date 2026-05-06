from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
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
class MessageAttachmentLinkageResult:
    session_id: str
    conversation_count: int
    message_unit_count: int
    audio_candidate_count: int
    image_candidate_count: int
    message_attachment_linkage_ready: bool

    def __post_init__(self) -> None:
        session_id = _ensure_non_empty_str(self.session_id, "session_id")
        conversation_count = _ensure_non_negative_int(
            self.conversation_count,
            "conversation_count",
        )
        message_unit_count = _ensure_non_negative_int(
            self.message_unit_count,
            "message_unit_count",
        )
        audio_candidate_count = _ensure_non_negative_int(
            self.audio_candidate_count,
            "audio_candidate_count",
        )
        image_candidate_count = _ensure_non_negative_int(
            self.image_candidate_count,
            "image_candidate_count",
        )

        if conversation_count == 0:
            raise ValueError("conversation_count must be >= 1")
        if message_unit_count == 0:
            raise ValueError("message_unit_count must be >= 1")
        if audio_candidate_count + image_candidate_count == 0:
            raise ValueError(
                "At least one attachment candidate must be present",
            )
        if not self.message_attachment_linkage_ready:
            raise ValueError("message_attachment_linkage_ready must be True")

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "conversation_count", conversation_count)
        object.__setattr__(self, "message_unit_count", message_unit_count)
        object.__setattr__(self, "audio_candidate_count", audio_candidate_count)
        object.__setattr__(self, "image_candidate_count", image_candidate_count)
