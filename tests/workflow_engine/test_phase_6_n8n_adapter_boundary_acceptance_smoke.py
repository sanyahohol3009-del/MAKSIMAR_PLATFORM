from pathlib import Path

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import (
    build_n8n_adapter_contract,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.workflow_runtime_policy import (
    build_workflow_runtime_policy,
)


VENDOR_GATE_SOURCE = Path("MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_vendor_gate_runtime.py")
CONTAINER_CONTRACT = Path("CONTAINER_DEPLOYMENT/cubes/workflow_automation/container_contract.yaml")
RUNTIME_PROFILE = Path("CONTAINER_DEPLOYMENT/cubes/workflow_automation/runtime_profile.yaml")
NETWORK_POLICY = Path("CONTAINER_DEPLOYMENT/cubes/workflow_automation/network_policy.yaml")


def _assert_false_if_exposed(payload: dict[str, object], key: str) -> None:
    if key in payload:
        assert payload[key] is False


def test_phase_6_n8n_adapter_boundary_remains_external_and_disabled_by_default() -> None:
    adapter = build_n8n_adapter_contract()
    payload = adapter.to_read_model()
    container_text = CONTAINER_CONTRACT.read_text(encoding="utf-8")

    assert isinstance(payload, dict)
    assert payload["adapter_mode"] == "contract_only"
    assert payload["adapter_location"] == "external_server_adapter"
    assert payload["contract_only"] is True

    assert "adapter_kind: n8n_external_server_adapter" in container_text
    assert "core_embedding_allowed: false" in container_text
    assert "canonical_truth_allowed: false" in container_text
    assert "direct_core_write_allowed: false" in container_text
    assert "direct_server_canonical_write_allowed: false" in container_text
    assert "dashboard_execution_allowed: false" in container_text
    assert "hidden_remote_control_allowed: false" in container_text
    assert "direct_phone_control_allowed: false" in container_text
    assert "production_runtime_allowed: false" in container_text
    assert "download_allowed_by_default: false" in container_text
    assert "install_allowed_by_default: false" in container_text

    for key in (
        "direct_core_write_allowed",
        "direct_server_canonical_write_allowed",
        "dashboard_execution_allowed",
        "hidden_remote_control_allowed",
        "direct_phone_control_allowed",
        "download_allowed",
        "install_allowed",
        "production_runtime_allowed",
        "network_allowed",
        "socket_allowed",
        "tunnel_allowed",
        "runtime_mutation_allowed",
    ):
        _assert_false_if_exposed(payload, key)


def test_phase_6_workflow_runtime_policy_keeps_intent_metadata_only() -> None:
    policy = build_workflow_runtime_policy()
    payload = policy.to_read_model()
    runtime_profile_text = RUNTIME_PROFILE.read_text(encoding="utf-8")
    network_text = NETWORK_POLICY.read_text(encoding="utf-8")

    assert payload["runtime_mode"] == "intent_metadata_only"

    assert "server_role: optional_accelerator" in runtime_profile_text
    assert "mobile_role: local_first_node" in runtime_profile_text
    assert "runtime_execution_allowed_now: false" in runtime_profile_text
    assert "dashboard_read_only: true" in runtime_profile_text
    assert "preview_read_only: true" in runtime_profile_text
    assert "network_controls_enabled: false" in runtime_profile_text

    assert "default_network_mode: disabled" in network_text
    assert "network_enabled_by_default: false" in network_text
    assert "socket_enabled_by_default: false" in network_text
    assert "tunnel_enabled_by_default: false" in network_text

    for key in (
        "runtime_execution_allowed",
        "dashboard_execution_allowed",
        "preview_execution_allowed",
        "direct_core_write_allowed",
        "direct_server_canonical_write_allowed",
        "network_allowed_by_default",
        "socket_allowed_by_default",
        "tunnel_allowed_by_default",
        "network_allowed",
        "socket_allowed",
        "tunnel_allowed",
        "runtime_mutation_allowed",
    ):
        _assert_false_if_exposed(payload, key)


def test_phase_6_n8n_vendor_gate_source_keeps_sandbox_gate_and_production_boundary() -> None:
    source_text = VENDOR_GATE_SOURCE.read_text(encoding="utf-8")

    required_markers = (
        "N8nVendorGateRuntime",
        "N8nVendorGateDecision",
        "build_n8n_vendor_gate_runtime",
        "evaluate_sandbox_probe_request",
        "sandbox",
        "production",
    )

    for marker in required_markers:
        assert marker in source_text


def test_phase_6_workflow_container_and_network_policy_keep_runtime_disabled() -> None:
    container_text = CONTAINER_CONTRACT.read_text(encoding="utf-8")
    runtime_text = RUNTIME_PROFILE.read_text(encoding="utf-8")
    network_text = NETWORK_POLICY.read_text(encoding="utf-8")

    assert "adapter_kind: n8n_external_server_adapter" in container_text
    assert "production_runtime_allowed: false" in container_text
    assert "download_allowed_by_default: false" in container_text
    assert "install_allowed_by_default: false" in container_text

    assert "runtime_mode: intent_metadata_only" in runtime_text
    assert "runtime_execution_allowed_now: false" in runtime_text
    assert "n8n_download_allowed_now: false" in runtime_text
    assert "n8n_install_allowed_now: false" in runtime_text
    assert "n8n_production_runtime_allowed: false" in runtime_text

    assert "default_network_mode: disabled" in network_text
    assert "network_enabled_by_default: false" in network_text
    assert "socket_enabled_by_default: false" in network_text
    assert "tunnel_enabled_by_default: false" in network_text
    assert "outbound_connections_allowed_by_default: false" in network_text
    assert "external_internet_allowed_by_default: false" in network_text
