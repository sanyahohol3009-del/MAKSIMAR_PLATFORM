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
class AttachmentLinkageResult:
    session_id: str
    conversation_count: int
    audio_attachment_root_count: int
    image_attachment_root_count: int
    attachment_linkage_ready: bool

    def __post_init__(self) -> None:
        session_id = _ensure_non_empty_str(self.session_id, "session_id")
        conversation_count = _ensure_non_negative_int(
            self.conversation_count,
            "conversation_count",
        )
        audio_attachment_root_count = _ensure_non_negative_int(
            self.audio_attachment_root_count,
            "audio_attachment_root_count",
        )
        image_attachment_root_count = _ensure_non_negative_int(
            self.image_attachment_root_count,
            "image_attachment_root_count",
        )

        if conversation_count == 0:
            raise ValueError("conversation_count must be >= 1")

        if audio_attachment_root_count + image_attachment_root_count == 0:
            raise ValueError(
                "At least one attachment root must be present",
            )

        if not self.attachment_linkage_ready:
            raise ValueError("attachment_linkage_ready must be True")

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "conversation_count", conversation_count)
        object.__setattr__(
            self,
            "audio_attachment_root_count",
            audio_attachment_root_count,
        )
        object.__setattr__(
            self,
            "image_attachment_root_count",
            image_attachment_root_count,
        )
