from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.chat_memory import ChatMemoryIndexContract


_REF_PREFIXES = ("chat-memory://", "android-local://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must be a reference")
    return value


def _ensure_refs(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    normalized = tuple(_ensure_ref(value, field_name[:-1] if field_name.endswith("s") else field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class AndroidChatMemoryIndexAdapter:
    adapter_id: str
    index_contract: ChatMemoryIndexContract
    device_id: str
    app_id: str
    owner_identity_id: str
    android_package_name: str
    local_index_ref: str
    indexed_record_refs: tuple[str, ...]
    supports_offline_search: bool
    stores_message_body: bool
    stores_heavy_payload: bool
    shell_adapter_only: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    mutation_allowed: bool
    network_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("adapter_id", "device_id", "app_id", "owner_identity_id", "android_package_name"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.index_contract, ChatMemoryIndexContract):
            raise ValueError("index_contract must be ChatMemoryIndexContract")
        if self.index_contract.device_id != self.device_id:
            raise ValueError("index_contract device_id must match adapter device_id")
        if self.index_contract.owner_identity_id != self.owner_identity_id:
            raise ValueError("index_contract owner_identity_id must match adapter owner_identity_id")

        object.__setattr__(self, "local_index_ref", _ensure_ref(self.local_index_ref, "local_index_ref"))
        object.__setattr__(self, "indexed_record_refs", _ensure_refs(self.indexed_record_refs, "indexed_record_refs"))

        required_true = {
            "supports_offline_search": self.supports_offline_search,
            "shell_adapter_only": self.shell_adapter_only,
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
            "mutation_allowed": self.mutation_allowed,
            "network_allowed": self.network_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_index(
        cls,
        *,
        adapter_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
        android_package_name: str,
        indexed_record_refs: tuple[str, ...],
    ) -> "AndroidChatMemoryIndexAdapter":
        index_contract = ChatMemoryIndexContract.local_chat_index(
            index_id=f"{adapter_id}_index",
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            indexed_record_refs=indexed_record_refs,
            audit_ref=f"ref://{adapter_id}/audit/index",
        )
        return cls(
            adapter_id=adapter_id,
            index_contract=index_contract,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            android_package_name=android_package_name,
            local_index_ref=f"android-local://{device_id}/chat-memory/index/{adapter_id}",
            indexed_record_refs=indexed_record_refs,
            supports_offline_search=True,
            stores_message_body=False,
            stores_heavy_payload=False,
            shell_adapter_only=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            mutation_allowed=False,
            network_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )
