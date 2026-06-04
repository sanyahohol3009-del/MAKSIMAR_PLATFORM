from pathlib import Path


NETWORK_POLICY_PATH = Path("CONTAINER_DEPLOYMENT/cubes/workflow_automation/network_policy.yaml")


def test_workflow_automation_network_policy_disables_network_socket_and_tunnel_by_default() -> None:
    text = NETWORK_POLICY_PATH.read_text(encoding="utf-8")

    assert "cube_id: workflow_automation" in text
    assert "default_network_mode: disabled" in text
    assert "network_enabled_by_default: false" in text
    assert "socket_enabled_by_default: false" in text
    assert "tunnel_enabled_by_default: false" in text
    assert "inbound_connections_allowed_by_default: false" in text
    assert "outbound_connections_allowed_by_default: false" in text
    assert "external_internet_allowed_by_default: false" in text
    assert "service_discovery_allowed_by_default: false" in text
    assert "direct_phone_control_allowed: false" in text
    assert "hidden_remote_control_allowed: false" in text
    assert "direct_core_write_allowed: false" in text
    assert "direct_server_canonical_write_allowed: false" in text
    assert "dashboard_execution_allowed: false" in text
    assert "runtime_mutation_allowed: false" in text
    assert "requires_explicit_network_policy_exception: true" in text
    assert "requires_operator_approval: true" in text
    assert "requires_security_scan: true" in text
    assert "requires_container_boundary: true" in text
    assert "requires_audit_event: true" in text
