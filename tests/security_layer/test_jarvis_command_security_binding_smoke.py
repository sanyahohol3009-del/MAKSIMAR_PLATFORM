from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.security_layer.jarvis_command_security_binding_contract import (
    JarvisCommandSecurityBindingContract,
    build_jarvis_command_security_binding_contract,
)


def test_jarvis_command_security_binding_requires_all_gates() -> None:
    read_model = build_jarvis_command_security_binding_contract().to_read_model()

    assert read_model["explicit_owner_command_required"] is True
    assert read_model["owner_voice_or_text_confirmation_required"] is True
    assert read_model["approval_required"] is True
    assert read_model["audit_required"] is True
    assert read_model["preview_required"] is True
    assert read_model["rollback_or_stop_required"] is True
    assert read_model["allowlist_required"] is True


def test_jarvis_command_security_binding_disables_dangerous_controls() -> None:
    read_model = build_jarvis_command_security_binding_contract().to_read_model()

    assert read_model["direct_execution_allowed"] is False
    assert read_model["shell_allowed"] is False
    assert read_model["browser_control_allowed"] is False
    assert read_model["app_control_allowed"] is False
    assert read_model["mouse_keyboard_control_allowed"] is False
    assert read_model["network_port_open_allowed"] is False
    assert read_model["file_delete_allowed"] is False
    assert read_model["code_edit_allowed"] is False
    assert read_model["git_operation_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False


def test_jarvis_command_security_binding_rejects_enabled_dangerous_flags() -> None:
    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisCommandSecurityBindingContract(
            binding_id="jarvis_command_security_binding_contract_v0_1",
            shell_allowed=True,
        )
    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisCommandSecurityBindingContract(
            binding_id="jarvis_command_security_binding_contract_v0_1",
            direct_execution_allowed=True,
        )

