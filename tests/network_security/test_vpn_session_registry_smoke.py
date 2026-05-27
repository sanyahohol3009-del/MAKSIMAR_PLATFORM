from __future__ import annotations

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_session_registry import (
    VpnSessionRegistry,
    build_default_vpn_session_registry,
)


def test_vpn_session_registry_smoke() -> None:
    registry = build_default_vpn_session_registry()

    assert isinstance(registry, VpnSessionRegistry)
    assert registry.runtime_started is False
    assert registry.tunnel_created is False
    assert registry.external_network_access_enabled is False
    assert registry.ports_opened is False
    assert registry.containers_started is False
    assert registry.active_deployment_created is False
    assert registry.runtime_mutation_allowed is False
    assert registry.direct_core_import_allowed is False
    assert registry.source_of_truth_override_allowed is False
    assert registry.dashboard_visible is True
    assert registry.containerization_ready is True
    assert registry.sessions
