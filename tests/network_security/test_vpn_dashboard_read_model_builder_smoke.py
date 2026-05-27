from __future__ import annotations

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_dashboard_read_model_builder import (
    VpnDashboardReadModel,
    build_vpn_dashboard_read_model,
)


def test_vpn_dashboard_read_model_builder_smoke() -> None:
    read_model = build_vpn_dashboard_read_model()

    assert isinstance(read_model, VpnDashboardReadModel)
    assert read_model.read_only is True
    assert read_model.action_buttons_enabled is False
    assert read_model.control_plane_handoff_required is True
    assert read_model.direct_execution_allowed is False
    assert read_model.dashboard_to_runtime_write_allowed is False
    assert read_model.ports_opened is False
    assert read_model.containers_started is False
    assert read_model.active_deployment_created is False
    assert read_model.external_network_access_enabled is False
    assert read_model.containerization_ready is True

    payload = read_model.to_dict()
    assert payload["vpn_status"]["read_only"] is True
    assert payload["vpn_status"]["action_buttons_enabled"] is False
    assert payload["egress_policy"]["deny_by_default"] is True
    assert payload["posture_summary"]["network_security_runtime_ready"] is True
