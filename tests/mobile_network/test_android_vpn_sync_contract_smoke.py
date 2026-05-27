from __future__ import annotations

from ANDROID_SHELL.network_vpn.vpn_sync_contract import (
    AndroidVpnSyncContract,
    build_android_vpn_sync_contract,
)


def test_android_vpn_sync_contract_smoke() -> None:
    sync = build_android_vpn_sync_contract()

    assert isinstance(sync, AndroidVpnSyncContract)
    assert sync.platform == "android"
    assert sync.sync_enabled is False
    assert sync.sync_execution_performed is False
    assert sync.app_memory_mutation_allowed is False
    assert sync.chat_memory_mutation_allowed is False
    assert sync.file_sync_allowed is False
    assert sync.external_network_access_enabled is False
    assert sync.tunnel_required is False
    assert sync.runtime_mutation_allowed is False
    assert sync.control_plane_handoff_required is True
    assert sync.operator_approval_required is True
    assert sync.dashboard_visible is True
    assert sync.read_only is True
    assert sync.containerization_ready is True
