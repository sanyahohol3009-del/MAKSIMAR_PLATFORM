from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ANDROID_SHELL.network_vpn.vpn_state_bridge import (
    AndroidVpnStateBridge,
    build_android_vpn_state_bridge,
)


@dataclass(frozen=True, slots=True)
class AndroidVpnSyncContract:
    """Android VPN sync contract.

    Sync is a read-only state projection. It does not perform network sync or runtime mutation.
    """

    schema_version: str
    sync_id: str
    platform: str
    state_bridge: AndroidVpnStateBridge
    sync_enabled: bool
    sync_execution_performed: bool
    app_memory_mutation_allowed: bool
    chat_memory_mutation_allowed: bool
    file_sync_allowed: bool
    external_network_access_enabled: bool
    tunnel_required: bool
    control_plane_handoff_required: bool
    operator_approval_required: bool
    runtime_mutation_allowed: bool
    dashboard_visible: bool
    read_only: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "android_vpn_sync_contract.v1":
            raise ValueError("schema_version must be android_vpn_sync_contract.v1")
        if self.sync_id != "android_vpn_sync_disabled_default":
            raise ValueError("sync_id must be android_vpn_sync_disabled_default")
        if self.platform != "android":
            raise ValueError("platform must be android")
        if not isinstance(self.state_bridge, AndroidVpnStateBridge):
            raise TypeError("state_bridge must be AndroidVpnStateBridge")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise ValueError("reason_codes must be a non-empty tuple")

        required_true = {
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "containerization_ready": self.containerization_ready,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must remain true")

        required_false = {
            "sync_enabled": self.sync_enabled,
            "sync_execution_performed": self.sync_execution_performed,
            "app_memory_mutation_allowed": self.app_memory_mutation_allowed,
            "chat_memory_mutation_allowed": self.chat_memory_mutation_allowed,
            "file_sync_allowed": self.file_sync_allowed,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_required": self.tunnel_required,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "sync_id": self.sync_id,
            "platform": self.platform,
            "state_bridge": self.state_bridge.to_dict(),
            "sync_enabled": self.sync_enabled,
            "sync_execution_performed": self.sync_execution_performed,
            "app_memory_mutation_allowed": self.app_memory_mutation_allowed,
            "chat_memory_mutation_allowed": self.chat_memory_mutation_allowed,
            "file_sync_allowed": self.file_sync_allowed,
            "external_network_access_enabled": self.external_network_access_enabled,
            "tunnel_required": self.tunnel_required,
            "control_plane_handoff_required": self.control_plane_handoff_required,
            "operator_approval_required": self.operator_approval_required,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_visible": self.dashboard_visible,
            "read_only": self.read_only,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


def build_android_vpn_sync_contract() -> AndroidVpnSyncContract:
    return AndroidVpnSyncContract(
        schema_version="android_vpn_sync_contract.v1",
        sync_id="android_vpn_sync_disabled_default",
        platform="android",
        state_bridge=build_android_vpn_state_bridge(),
        sync_enabled=False,
        sync_execution_performed=False,
        app_memory_mutation_allowed=False,
        chat_memory_mutation_allowed=False,
        file_sync_allowed=False,
        external_network_access_enabled=False,
        tunnel_required=False,
        control_plane_handoff_required=True,
        operator_approval_required=True,
        runtime_mutation_allowed=False,
        dashboard_visible=True,
        read_only=True,
        containerization_ready=True,
        reason_codes=("android_vpn_sync_contract_read_only_until_network_policy_gate",),
    )
