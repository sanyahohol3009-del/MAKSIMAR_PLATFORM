from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_record_refs(values: Tuple[str, ...]) -> Tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("indexed_record_refs must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "indexed_record_ref") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("indexed_record_refs must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class ChatMemoryIndexContract:
    """Local mobile chat memory index contract.

    The index stores record references and metadata only; it never stores full
    message bodies, media, OpenIM truth, or core chat truth.
    """

    index_id: str
    device_id: str
    owner_identity_id: str
    indexed_record_refs: Tuple[str, ...]
    index_scope: str
    supports_offline_search: bool
    stores_message_body: bool
    stores_heavy_payload: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    rebuild_requires_policy: bool
    audit_ref: str

    def __post_init__(self) -> None:
        for field_name in ("index_id", "device_id", "owner_identity_id", "index_scope", "audit_ref"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "indexed_record_refs", _ensure_record_refs(self.indexed_record_refs))

        if not self.supports_offline_search:
            raise ValueError("supports_offline_search must be True")
        if self.stores_message_body:
            raise ValueError("stores_message_body must be False")
        if self.stores_heavy_payload:
            raise ValueError("stores_heavy_payload must be False")
        if not self.local_chat_memory_only:
            raise ValueError("local_chat_memory_only must be True")
        if self.openim_truth:
            raise ValueError("openim_truth must be False")
        if self.core_chat_truth:
            raise ValueError("core_chat_truth must be False")
        if self.canonical_truth:
            raise ValueError("canonical_truth must be False")
        if not self.rebuild_requires_policy:
            raise ValueError("rebuild_requires_policy must be True")

    @classmethod
    def local_chat_index(
        cls,
        *,
        index_id: str,
        device_id: str,
        owner_identity_id: str,
        indexed_record_refs: Tuple[str, ...],
        audit_ref: str,
    ) -> "ChatMemoryIndexContract":
        return cls(
            index_id=index_id,
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            indexed_record_refs=indexed_record_refs,
            index_scope="local_mobile_chat_memory",
            supports_offline_search=True,
            stores_message_body=False,
            stores_heavy_payload=False,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            rebuild_requires_policy=True,
            audit_ref=audit_ref,
        )
