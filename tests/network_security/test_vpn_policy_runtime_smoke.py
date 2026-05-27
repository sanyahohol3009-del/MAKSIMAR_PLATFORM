from __future__ import annotations

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.vpn_policy_runtime import (
    evaluate_vpn_policy_runtime,
)


def test_vpn_policy_runtime_smoke() -> None:
    decision = evaluate_vpn_policy_runtime("create_tunnel")

    assert decision.decision == "deny_tunnel_create"
    assert decision.allowed is False
    assert decision.operator_approval_required is True
    assert decision.runtime_execution_performed is False
    assert decision.tunnel_created is False
    assert decision.external_network_access_enabled is False
    assert decision.ports_opened is False
    assert decision.containers_started is False
    assert decision.active_deployment_created is False
    assert decision.audit_required is True
    assert decision.dashboard_visible is True
    assert decision.containerization_ready is True


def test_vpn_policy_runtime_allows_read_model_only_as_denied_action_surface() -> None:
    decision = evaluate_vpn_policy_runtime("read_status")

    assert decision.decision == "allow_read_model_only"
    assert decision.allowed is False
    assert decision.runtime_execution_performed is False
    assert decision.tunnel_created is False
