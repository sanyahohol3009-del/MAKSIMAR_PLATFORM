from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.chat_memory import ChatMemoryIndexContract


_REF_PREFIXES = ("ios-local://", "chat-memory://", "ref://", "audit://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_refs(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, field_name[:-1] if field_name.endswith("s") else field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    for value in normalized:
        if not value.startswith(_REF_PREFIXES):
            raise ValueError(f"{field_name} values must be references")
    return normalized


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must be a reference")
    return value


@dataclass(frozen=True)
class IOSChatMemoryIndexAdapter:
    index_adapter_id: str
    index_contract: ChatMemoryIndexContract
    device_id: str
    owner_identity_id: str
    ios_bundle_id: str
    indexed_record_refs: tuple[str, ...]
    index_storage_ref: str
    index_rebuild_policy_ref: str
    supports_offline_search: bool
    stores_message_body: bool
    stores_heavy_payload: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    platform_api_calls_allowed: bool
    sync_runtime_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("index_adapter_id", "device_id", "owner_identity_id", "ios_bundle_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.index_contract, ChatMemoryIndexContract):
            raise ValueError("index_contract must be ChatMemoryIndexContract")
        if self.index_contract.device_id != self.device_id:
            raise ValueError("index_contract device_id must match adapter device_id")
        if self.index_contract.owner_identity_id != self.owner_identity_id:
            raise ValueError("index_contract owner_identity_id must match adapter owner_identity_id")

        object.__setattr__(self, "indexed_record_refs", _ensure_refs(self.indexed_record_refs, "indexed_record_refs"))
        if self.index_contract.indexed_record_refs != self.indexed_record_refs:
            raise ValueError("index_contract indexed_record_refs must match adapter indexed_record_refs")

        object.__setattr__(self, "index_storage_ref", _ensure_ref(self.index_storage_ref, "index_storage_ref"))
        object.__setattr__(self, "index_rebuild_policy_ref", _ensure_ref(self.index_rebuild_policy_ref, "index_rebuild_policy_ref"))

        required_true = {
            "supports_offline_search": self.supports_offline_search,
            "local_chat_memory_only": self.local_chat_memory_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "stores_message_body": self.stores_message_body,
            "stores_heavy_payload": self.stores_heavy_payload,
            "openim_truth": self.openim_truth,
            "core_chat_truth": self.core_chat_truth,
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "platform_api_calls_allowed": self.platform_api_calls_allowed,
            "sync_runtime_allowed": self.sync_runtime_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

        if self.index_contract.stores_message_body:
            raise ValueError("index_contract stores_message_body must be False")
        if self.index_contract.stores_heavy_payload:
            raise ValueError("index_contract stores_heavy_payload must be False")
        if self.index_contract.openim_truth:
            raise ValueError("index_contract openim_truth must be False")
        if self.index_contract.core_chat_truth:
            raise ValueError("index_contract core_chat_truth must be False")
        if self.index_contract.canonical_truth:
            raise ValueError("index_contract canonical_truth must be False")

    @classmethod
    def default_index(
        cls,
        *,
        index_adapter_id: str,
        device_id: str,
        owner_identity_id: str,
        ios_bundle_id: str,
        indexed_record_refs: tuple[str, ...],
        audit_ref: str,
    ) -> "IOSChatMemoryIndexAdapter":
        normalized_refs = _ensure_refs(indexed_record_refs, "indexed_record_refs")
        index_contract = ChatMemoryIndexContract.local_chat_index(
            index_id=f"{index_adapter_id}_contract",
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            indexed_record_refs=normalized_refs,
            audit_ref=audit_ref,
        )
        return cls(
            index_adapter_id=index_adapter_id,
            index_contract=index_contract,
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            ios_bundle_id=ios_bundle_id,
            indexed_record_refs=normalized_refs,
            index_storage_ref=f"ios-local://{device_id}/chat-memory/index/{index_adapter_id}",
            index_rebuild_policy_ref=f"ref://{index_adapter_id}/rebuild-policy",
            supports_offline_search=True,
            stores_message_body=False,
            stores_heavy_payload=False,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
        )
