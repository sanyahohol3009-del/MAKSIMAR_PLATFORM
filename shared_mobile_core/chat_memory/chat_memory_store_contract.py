from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_record_kinds(values: Tuple[str, ...]) -> Tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("supported_record_kinds must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "supported_record_kind") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("supported_record_kinds must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class ChatMemoryStoreContract:
    """Local mobile chat memory store contract.

    Shell adapters can implement this boundary later. The contract is not
    OpenIM truth, core chat truth, canonical storage, or a server write path.
    """

    store_id: str
    device_id: str
    app_id: str
    owner_identity_id: str
    storage_scope: str
    encrypted_at_rest_required: bool
    retention_required: bool
    offline_first: bool
    sync_policy_required: bool
    shell_adapter_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    supported_record_kinds: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("store_id", "device_id", "app_id", "owner_identity_id", "storage_scope"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "supported_record_kinds", _ensure_record_kinds(self.supported_record_kinds))

        if not self.encrypted_at_rest_required:
            raise ValueError("encrypted_at_rest_required must be True")
        if not self.retention_required:
            raise ValueError("retention_required must be True")
        if not self.offline_first:
            raise ValueError("offline_first must be True")
        if not self.sync_policy_required:
            raise ValueError("sync_policy_required must be True")
        if not self.shell_adapter_only:
            raise ValueError("shell_adapter_only must be True")
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
    def default_mobile_chat_store(
        cls,
        *,
        store_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
    ) -> "ChatMemoryStoreContract":
        return cls(
            store_id=store_id,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            storage_scope="local_mobile_chat_memory",
            encrypted_at_rest_required=True,
            retention_required=True,
            offline_first=True,
            sync_policy_required=True,
            shell_adapter_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            supported_record_kinds=("message_reference", "conversation_reference", "offline_replay_reference"),
        )
