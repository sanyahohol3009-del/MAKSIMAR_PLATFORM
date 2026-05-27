from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_security.vpn_session_contract import build_disabled_vpn_session


def test_vpn_capability_required_server_smoke() -> None:
    session = build_disabled_vpn_session()

    assert session.state == "disabled"
    assert session.started is False
    assert session.connected is False
    assert session.tunnel_active is False
    assert session.egress_active is False
    assert session.runtime_execution_verified is False
    assert session.runtime_mutation_allowed is False
    assert session.ports_opened is False
    assert session.containers_started is False
    assert session.active_deployment_created is False
    assert session.dashboard_visible is True
    assert session.disable_safe is True
    assert session.containerization_ready is True
