from __future__ import annotations

from MAKSIMAR_SERVER.NETWORK_SECURITY_RUNTIME.network_posture_summary_builder import (
    NetworkPostureSummary,
    build_network_posture_summary,
)


def test_network_posture_summary_builder_smoke() -> None:
    summary = build_network_posture_summary()

    assert isinstance(summary, NetworkPostureSummary)
    assert summary.network_security_runtime_ready is True
    assert summary.runtime_policy_gated is True
    assert summary.vpn_runtime_disabled is True
    assert summary.egress_denied_by_default is True
    assert summary.external_network_access_enabled is False
    assert summary.ports_opened is False
    assert summary.containers_started is False
    assert summary.active_deployment_created is False
    assert summary.runtime_mutation_allowed is False
    assert summary.dashboard_visible is True
    assert summary.containerization_ready is True

    payload = summary.to_dict()
    assert payload["vpn_decision"]["runtime_execution_performed"] is False
    assert payload["egress_decision"]["external_connection_attempted"] is False
