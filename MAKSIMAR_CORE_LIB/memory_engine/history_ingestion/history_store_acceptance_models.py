from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True)
class HistoryStoreAcceptanceResult:
    session_manifest_count: int
    attachment_summary_count: int
    conversation_manifest_count: int
    normalized_record_count: int
    message_unit_count: int
    store_acceptance_ready: bool

    def __post_init__(self) -> None:
        session_manifest_count = _ensure_non_negative_int(
            self.session_manifest_count,
            "session_manifest_count",
        )
        attachment_summary_count = _ensure_non_negative_int(
            self.attachment_summary_count,
            "attachment_summary_count",
        )
        conversation_manifest_count = _ensure_non_negative_int(
            self.conversation_manifest_count,
            "conversation_manifest_count",
        )
        normalized_record_count = _ensure_non_negative_int(
            self.normalized_record_count,
            "normalized_record_count",
        )
        message_unit_count = _ensure_non_negative_int(
            self.message_unit_count,
            "message_unit_count",
        )

        if session_manifest_count == 0:
            raise ValueError("session_manifest_count must be >= 1")
        if attachment_summary_count == 0:
            raise ValueError("attachment_summary_count must be >= 1")
        if conversation_manifest_count == 0:
            raise ValueError("conversation_manifest_count must be >= 1")
        if normalized_record_count == 0:
            raise ValueError("normalized_record_count must be >= 1")
        if message_unit_count == 0:
            raise ValueError("message_unit_count must be >= 1")
        if not self.store_acceptance_ready:
            raise ValueError("store_acceptance_ready must be True")

        object.__setattr__(self, "session_manifest_count", session_manifest_count)
        object.__setattr__(self, "attachment_summary_count", attachment_summary_count)
        object.__setattr__(self, "conversation_manifest_count", conversation_manifest_count)
        object.__setattr__(self, "normalized_record_count", normalized_record_count)
        object.__setattr__(self, "message_unit_count", message_unit_count)
