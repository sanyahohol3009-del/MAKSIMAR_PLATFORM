from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_PRIVACY_CLASSES = ("local_private", "owner_private", "conversation_private")
_REFERENCE_PREFIXES = ("ref://", "local://", "chat-memory://", "secure-ref://")
_INLINE_MESSAGE_MARKERS = ("{", "[", "base64:", "data:", "inline:", "payload:", "\n")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


def _ensure_identity_refs(values: Tuple[str, ...]) -> Tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("participant_identity_refs must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "participant_identity_ref") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("participant_identity_refs must not contain duplicates")
    return normalized


def _ensure_message_ref(value: str) -> str:
    value = _ensure_non_empty(value, "message_ref")
    lowered = value.lower()
    if any(marker in lowered for marker in _INLINE_MESSAGE_MARKERS):
        raise ValueError("message_ref must be a reference, not an inline message body or payload")
    if not value.startswith(_REFERENCE_PREFIXES):
        raise ValueError(f"message_ref must start with one of {_REFERENCE_PREFIXES}")
    return value


@dataclass(frozen=True)
class ChatMemoryRecordContract:
    """Local mobile chat memory record contract.

    This contract stores message references and metadata only. It does not
    define OpenIM truth, MAKSIMAR core chat truth, persistence, sync, or server writes.
    """

    record_id: str
    chat_id: str
    conversation_id: str
    message_id: str
    device_id: str
    owner_identity_id: str
    participant_identity_refs: Tuple[str, ...]
    message_ref: str
    created_at: str
    updated_at: str
    schema_version: str
    privacy_classification: str
    retention_policy_id: str
    encryption_policy_id: str
    sync_eligible: bool
    sync_requires_policy: bool
    offline_replay_eligible: bool
    audit_ref: str
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in (
            "record_id",
            "chat_id",
            "conversation_id",
            "message_id",
            "device_id",
            "owner_identity_id",
            "created_at",
            "updated_at",
            "schema_version",
            "retention_policy_id",
            "encryption_policy_id",
            "audit_ref",
        ):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(self, "participant_identity_refs", _ensure_identity_refs(self.participant_identity_refs))
        object.__setattr__(self, "message_ref", _ensure_message_ref(self.message_ref))
        object.__setattr__(
            self,
            "privacy_classification",
            _ensure_allowed(self.privacy_classification, "privacy_classification", _ALLOWED_PRIVACY_CLASSES),
        )

        if not self.sync_requires_policy:
            raise ValueError("sync_requires_policy must be True")
        if not self.local_chat_memory_only:
            raise ValueError("local_chat_memory_only must be True")
        if self.openim_truth:
            raise ValueError("openim_truth must be False")
        if self.core_chat_truth:
            raise ValueError("core_chat_truth must be False")
        if self.canonical_truth:
            raise ValueError("canonical_truth must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.direct_server_write_allowed:
            raise ValueError("direct_server_write_allowed must be False")

    @classmethod
    def local_message_reference(
        cls,
        *,
        record_id: str,
        chat_id: str,
        conversation_id: str,
        message_id: str,
        device_id: str,
        owner_identity_id: str,
        participant_identity_refs: Tuple[str, ...],
        message_ref: str,
        created_at: str,
        updated_at: str,
        retention_policy_id: str,
        encryption_policy_id: str,
        audit_ref: str,
        sync_eligible: bool = True,
        offline_replay_eligible: bool = True,
    ) -> "ChatMemoryRecordContract":
        return cls(
            record_id=record_id,
            chat_id=chat_id,
            conversation_id=conversation_id,
            message_id=message_id,
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            participant_identity_refs=participant_identity_refs,
            message_ref=message_ref,
            created_at=created_at,
            updated_at=updated_at,
            schema_version="chat_memory_record.v1",
            privacy_classification="conversation_private",
            retention_policy_id=retention_policy_id,
            encryption_policy_id=encryption_policy_id,
            sync_eligible=sync_eligible,
            sync_requires_policy=True,
            offline_replay_eligible=offline_replay_eligible,
            audit_ref=audit_ref,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )
