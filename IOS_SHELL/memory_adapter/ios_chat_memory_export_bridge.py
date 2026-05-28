from __future__ import annotations

from dataclasses import dataclass

from IOS_SHELL.memory_adapter.ios_chat_memory_index import IOSChatMemoryIndexAdapter
from IOS_SHELL.memory_adapter.ios_chat_memory_store import IOSChatMemoryStoreAdapter


_REF_PREFIXES = ("chat-memory://", "ios-local://", "ref://", "audit://")


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
class IOSChatMemoryExportBridge:
    bridge_id: str
    store_adapter: IOSChatMemoryStoreAdapter
    index_adapter: IOSChatMemoryIndexAdapter
    device_id: str
    app_id: str
    owner_identity_id: str
    ios_bundle_id: str
    export_scope: str
    exported_record_refs: tuple[str, ...]
    export_manifest_ref: str
    audit_ref: str
    read_only: bool
    reference_only_export: bool
    includes_message_body: bool
    includes_heavy_payload: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    platform_api_calls_allowed: bool
    sync_runtime_allowed: bool
    mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _ensure_non_empty(self.bridge_id, "bridge_id"))
        object.__setattr__(self, "export_scope", _ensure_non_empty(self.export_scope, "export_scope"))

        if not isinstance(self.store_adapter, IOSChatMemoryStoreAdapter):
            raise ValueError("store_adapter must be IOSChatMemoryStoreAdapter")
        if not isinstance(self.index_adapter, IOSChatMemoryIndexAdapter):
            raise ValueError("index_adapter must be IOSChatMemoryIndexAdapter")

        for field_name in ("device_id", "app_id", "owner_identity_id", "ios_bundle_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if self.store_adapter.device_id != self.device_id:
            raise ValueError("store_adapter device_id must match bridge device_id")
        if self.store_adapter.app_id != self.app_id:
            raise ValueError("store_adapter app_id must match bridge app_id")
        if self.store_adapter.owner_identity_id != self.owner_identity_id:
            raise ValueError("store_adapter owner_identity_id must match bridge owner_identity_id")
        if self.store_adapter.ios_bundle_id != self.ios_bundle_id:
            raise ValueError("store_adapter ios_bundle_id must match bridge ios_bundle_id")

        if self.index_adapter.device_id != self.device_id:
            raise ValueError("index_adapter device_id must match bridge device_id")
        if self.index_adapter.owner_identity_id != self.owner_identity_id:
            raise ValueError("index_adapter owner_identity_id must match bridge owner_identity_id")
        if self.index_adapter.ios_bundle_id != self.ios_bundle_id:
            raise ValueError("index_adapter ios_bundle_id must match bridge ios_bundle_id")

        object.__setattr__(self, "exported_record_refs", _ensure_refs(self.exported_record_refs, "exported_record_refs"))
        object.__setattr__(self, "export_manifest_ref", _ensure_ref(self.export_manifest_ref, "export_manifest_ref"))
        object.__setattr__(self, "audit_ref", _ensure_ref(self.audit_ref, "audit_ref"))

        required_true = {
            "read_only": self.read_only,
            "reference_only_export": self.reference_only_export,
            "local_chat_memory_only": self.local_chat_memory_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "includes_message_body": self.includes_message_body,
            "includes_heavy_payload": self.includes_heavy_payload,
            "openim_truth": self.openim_truth,
            "core_chat_truth": self.core_chat_truth,
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "platform_api_calls_allowed": self.platform_api_calls_allowed,
            "sync_runtime_allowed": self.sync_runtime_allowed,
            "mutation_allowed": self.mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def from_store_and_index(
        cls,
        *,
        bridge_id: str,
        store_adapter: IOSChatMemoryStoreAdapter,
        index_adapter: IOSChatMemoryIndexAdapter,
        exported_record_refs: tuple[str, ...],
    ) -> "IOSChatMemoryExportBridge":
        normalized_refs = _ensure_refs(exported_record_refs, "exported_record_refs")
        return cls(
            bridge_id=bridge_id,
            store_adapter=store_adapter,
            index_adapter=index_adapter,
            device_id=store_adapter.device_id,
            app_id=store_adapter.app_id,
            owner_identity_id=store_adapter.owner_identity_id,
            ios_bundle_id=store_adapter.ios_bundle_id,
            export_scope="ios_local_chat_memory_reference_export",
            exported_record_refs=normalized_refs,
            export_manifest_ref=f"ref://{bridge_id}/manifest",
            audit_ref=f"audit://{bridge_id}",
            read_only=True,
            reference_only_export=True,
            includes_message_body=False,
            includes_heavy_payload=False,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
            mutation_allowed=False,
        )
