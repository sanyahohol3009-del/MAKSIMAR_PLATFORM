from pathlib import Path


CONTRACT_PATH = Path("CONTAINER_DEPLOYMENT/cubes/workflow_automation/container_contract.yaml")
RUNTIME_PROFILE_PATH = Path("CONTAINER_DEPLOYMENT/cubes/workflow_automation/runtime_profile.yaml")


def _text(path: Path) -> str:
    assert path.exists()
    return path.read_text(encoding="utf-8")


def test_workflow_automation_container_contract_declares_external_adapter_boundary() -> None:
    text = _text(CONTRACT_PATH)

    assert "cube_id: workflow_automation" in text
    assert "runtime_kind: external_adapter_boundary" in text
    assert "adapter_kind: n8n_external_server_adapter" in text
    assert "core_embedding_allowed: false" in text
    assert "canonical_truth_allowed: false" in text
    assert "direct_core_write_allowed: false" in text
    assert "direct_server_canonical_write_allowed: false" in text
    assert "dashboard_execution_allowed: false" in text
    assert "hidden_remote_control_allowed: false" in text
    assert "direct_phone_control_allowed: false" in text
    assert "network_enabled_by_default: false" in text
    assert "socket_enabled_by_default: false" in text
    assert "tunnel_enabled_by_default: false" in text
    assert "requires_vendor_gate: true" in text
    assert "production_runtime_allowed: false" in text
    assert "download_allowed_by_default: false" in text
    assert "install_allowed_by_default: false" in text


def test_workflow_automation_runtime_profile_is_intent_metadata_only() -> None:
    text = _text(RUNTIME_PROFILE_PATH)

    assert "runtime_mode: intent_metadata_only" in text
    assert "server_role: optional_accelerator" in text
    assert "mobile_role: local_first_node" in text
    assert "runtime_execution_allowed_now: false" in text
    assert "n8n_download_allowed_now: false" in text
    assert "n8n_install_allowed_now: false" in text
    assert "n8n_production_runtime_allowed: false" in text
    assert "dashboard_read_only: true" in text
    assert "preview_read_only: true" in text
    assert "execution_controls_enabled: false" in text
    assert "network_controls_enabled: false" in text
