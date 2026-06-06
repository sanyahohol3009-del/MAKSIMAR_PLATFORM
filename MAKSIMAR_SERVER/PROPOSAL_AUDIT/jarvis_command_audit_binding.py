from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.security_layer.jarvis_action_allowlist_contract import (
    build_jarvis_action_allowlist_contract,
)
from MAKSIMAR_CORE_LIB.security_layer.jarvis_command_security_binding_contract import (
    build_jarvis_command_security_binding_contract,
)


def build_jarvis_command_audit_binding_read_model() -> dict[str, Any]:
    allowlist = build_jarvis_action_allowlist_contract().to_read_model()
    security = build_jarvis_command_security_binding_contract().to_read_model()

    return {
        "summary_id": "jarvis_command_audit_binding_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "audit_required": security["audit_required"],
        "approval_required": security["approval_required"],
        "preview_required": security["preview_required"],
        "allowlist_required": security["allowlist_required"],
        "execution_enabled": False,
        "allowed_action_candidates": allowlist["allowed_action_candidates"],
        "allowed_action_ids": allowlist["allowed_action_ids"],
        "forbidden_actions": allowlist["forbidden_actions"],
        "audit_event_kind": "jarvis_command_proposal",
        "proposal_only": True,
        "direct_execution_allowed": security["direct_execution_allowed"],
        "shell_allowed": security["shell_allowed"],
        "browser_control_allowed": security["browser_control_allowed"],
        "app_control_allowed": security["app_control_allowed"],
        "network_port_open_allowed": security["network_port_open_allowed"],
        "file_delete_allowed": security["file_delete_allowed"],
        "code_edit_allowed": security["code_edit_allowed"],
        "git_operation_allowed": security["git_operation_allowed"],
        "model_download_allowed": security["model_download_allowed"],
        "runtime_start_allowed": security["runtime_start_allowed"],
        "dashboard_execution_allowed": security["dashboard_execution_allowed"],
    }
