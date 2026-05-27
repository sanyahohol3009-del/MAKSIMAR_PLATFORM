from pathlib import Path

from tools.chat_sync_preview import build_chat_sync_preview
from tools.chat_system_preview import build_chat_system_preview


CONTAINER_CONTRACT = Path("CONTAINER_DEPLOYMENT/cubes/chat_command/container_contract.yaml")


def test_chat_command_container_contract_smoke() -> None:
    text = CONTAINER_CONTRACT.read_text(encoding="utf-8")

    assert "id: chat_command_container_contract_v1" in text
    assert "cube_id: chat_command" in text
    assert "container_ready: true" in text
    assert "adapter_only: true" in text
    assert "read_model_only: true" in text
    assert "required_security_gate: chat_command_security_gate_v1" in text


def test_chat_command_preview_tools_are_safe() -> None:
    system_preview = build_chat_system_preview()
    sync_preview = build_chat_sync_preview()

    assert system_preview["dashboard_read_only"] is True
    assert system_preview["direct_execution_allowed"] is False
    assert system_preview["dashboard_control_allowed"] is False
    assert sync_preview["direct_sync_execution_allowed"] is False
    assert sync_preview["external_network_access_allowed"] is False
