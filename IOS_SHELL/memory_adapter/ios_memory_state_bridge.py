from __future__ import annotations

from dataclasses import dataclass

from IOS_SHELL.memory_adapter.ios_app_memory_store import IOSAppMemoryStoreAdapter


_REF_PREFIXES = ("ref://", "ios-local://", "ios-secure-ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must be a reference")
    return value


@dataclass(frozen=True)
class IOSMemoryStateBridge:
    bridge_id: str
    device_id: str
    app_id: str
    ios_bundle_id: str
    store_adapter_ref: str
    record_count: int
    encrypted_at_rest_required: bool
    retention_required: bool
    sync_policy_required: bool
    offline_first: bool
    last_audit_ref: str
    state_read_only: bool
    local_app_memory_only: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    mutation_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("bridge_id", "device_id", "app_id", "ios_bundle_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))
        object.__setattr__(self, "store_adapter_ref", _ensure_ref(self.store_adapter_ref, "store_adapter_ref"))
        object.__setattr__(self, "last_audit_ref", _ensure_ref(self.last_audit_ref, "last_audit_ref"))

        if not isinstance(self.record_count, int) or self.record_count < 0:
            raise ValueError("record_count must be a non-negative integer")

        required_true = {
            "encrypted_at_rest_required": self.encrypted_at_rest_required,
            "retention_required": self.retention_required,
            "sync_policy_required": self.sync_policy_required,
            "offline_first": self.offline_first,
            "state_read_only": self.state_read_only,
            "local_app_memory_only": self.local_app_memory_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "mutation_allowed": self.mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def from_store_adapter(
        cls,
        *,
        bridge_id: str,
        store_adapter: IOSAppMemoryStoreAdapter,
        record_count: int,
        last_audit_ref: str,
    ) -> "IOSMemoryStateBridge":
        if not isinstance(store_adapter, IOSAppMemoryStoreAdapter):
            raise ValueError("store_adapter must be IOSAppMemoryStoreAdapter")
        return cls(
            bridge_id=bridge_id,
            device_id=store_adapter.device_id,
            app_id=store_adapter.app_id,
            ios_bundle_id=store_adapter.ios_bundle_id,
            store_adapter_ref=f"ref://{store_adapter.adapter_id}",
            record_count=record_count,
            encrypted_at_rest_required=store_adapter.store_contract.encrypted_at_rest_required,
            retention_required=store_adapter.store_contract.retention_required,
            sync_policy_required=store_adapter.store_contract.sync_policy_required,
            offline_first=store_adapter.store_contract.offline_first,
            last_audit_ref=last_audit_ref,
            state_read_only=True,
            local_app_memory_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            mutation_allowed=False,
        )
