from __future__ import annotations

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.egress_guard_runtime import (
    evaluate_egress_guard_runtime,
)


def test_egress_guard_runtime_smoke() -> None:
    decision = evaluate_egress_guard_runtime("openai.com")

    assert decision.decision == "deny_external_egress"
    assert decision.allowed is False
    assert decision.dns_resolution_performed is False
    assert decision.external_connection_attempted is False
    assert decision.public_ingress_enabled is False
    assert decision.tunnel_creation_attempted is False
    assert decision.ports_opened is False
    assert decision.containers_started is False
    assert decision.active_deployment_created is False
    assert decision.runtime_mutation_allowed is False
    assert decision.audit_required is True
    assert decision.dashboard_visible is True
    assert decision.containerization_ready is True
