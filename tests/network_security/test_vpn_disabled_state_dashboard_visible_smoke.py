from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_security.vpn_policy_disable_contract import (
    VpnDisabledRuntimeState,
    build_default_vpn_disabled_runtime_state,
)


def test_vpn_disabled_state_dashboard_visible_smoke() -> None:
    state = build_default_vpn_disabled_runtime_state()

    assert isinstance(state, VpnDisabledRuntimeState)
    payload = state.to_dict()

    assert payload["dashboard_visible"] is True
    assert payload["runtime_disabled"] is True
    assert payload["containerization_ready"] is True
    assert payload["ports_opened"] is False
    assert payload["containers_started"] is False
    assert payload["active_deployment_created"] is False

    contract = payload["contract"]
    assert contract["runtime_disabled_by_default"] is True
    assert contract["external_network_access_enabled"] is False
    assert contract["network_egress_allowed_by_default"] is False

    adapters = payload["adapter_registry"]["adapters"]
    assert adapters
    for adapter in adapters:
        assert adapter["dashboard_visible"] is True
        assert adapter["runtime_implemented"] is False
        assert adapter["runtime_execution_verified"] is False
        assert adapter["external_network_access_enabled"] is False
        assert adapter["ports_opened"] is False
        assert adapter["containers_started"] is False
        assert adapter["active_deployment_created"] is False
        assert adapter["containerization_ready"] is True
