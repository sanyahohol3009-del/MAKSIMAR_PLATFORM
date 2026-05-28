from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.app_memory import AppMemoryStoreContract


_REF_PREFIXES = ("ios-local://", "ios-secure-ref://", "secure-ref://", "ref://")


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
class IOSAppMemoryStoreAdapter:
    adapter_id: str
    store_contract: AppMemoryStoreContract
    device_id: str
    app_id: str
    owner_identity_id: str
    ios_bundle_id: str
    storage_backend_ref: str
    secure_local_store_ref: str
    encryption_bridge_ref: str
    retention_runtime_ref: str
    state_bridge_ref: str
    shell_adapter_only: bool
    local_app_memory_only: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    platform_api_calls_allowed: bool
    sync_runtime_allowed: bool

    def __post_init__(self) -> None:
        for field_name in (
            "adapter_id",
            "device_id",
            "app_id",
            "owner_identity_id",
            "ios_bundle_id",
        ):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.store_contract, AppMemoryStoreContract):
            raise ValueError("store_contract must be AppMemoryStoreContract")
        if self.store_contract.device_id != self.device_id:
            raise ValueError("store_contract device_id must match adapter device_id")
        if self.store_contract.app_id != self.app_id:
            raise ValueError("store_contract app_id must match adapter app_id")
        if self.store_contract.owner_identity_id != self.owner_identity_id:
            raise ValueError("store_contract owner_identity_id must match adapter owner_identity_id")

        for field_name in (
            "storage_backend_ref",
            "secure_local_store_ref",
            "encryption_bridge_ref",
            "retention_runtime_ref",
            "state_bridge_ref",
        ):
            object.__setattr__(self, field_name, _ensure_ref(getattr(self, field_name), field_name))

        required_true = {
            "shell_adapter_only": self.shell_adapter_only,
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
            "platform_api_calls_allowed": self.platform_api_calls_allowed,
            "sync_runtime_allowed": self.sync_runtime_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_adapter(
        cls,
        *,
        adapter_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
        ios_bundle_id: str,
    ) -> "IOSAppMemoryStoreAdapter":
        store_contract = AppMemoryStoreContract.default_mobile_store(
            store_id=f"{adapter_id}_store",
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
        )
        return cls(
            adapter_id=adapter_id,
            store_contract=store_contract,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            ios_bundle_id=ios_bundle_id,
            storage_backend_ref=f"ios-local://{device_id}/app-memory/store",
            secure_local_store_ref=f"ios-secure-ref://{device_id}/app-memory/secure-store",
            encryption_bridge_ref=f"ref://{adapter_id}/encryption-bridge",
            retention_runtime_ref=f"ref://{adapter_id}/retention-runtime",
            state_bridge_ref=f"ref://{adapter_id}/state-bridge",
            shell_adapter_only=True,
            local_app_memory_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
        )
