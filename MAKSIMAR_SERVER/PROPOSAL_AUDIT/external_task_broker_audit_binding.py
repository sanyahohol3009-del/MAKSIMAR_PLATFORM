from __future__ import annotations

from typing import Any

from MAKSIMAR_SERVER.AI_ORCHESTRATION.external_task_broker_read_model import (
    build_external_task_broker_read_model,
)


def build_external_task_broker_audit_binding_read_model() -> dict[str, Any]:
    broker_model = build_external_task_broker_read_model()
    return {
        "summary_id": "external_task_broker_audit_binding_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "audit_required": True,
        "approval_required": True,
        "preview_required": True,
        "allowlist_required": True,
        "proposal_only": True,
        "audit_event_kind": "external_task_broker_proposal",
        "broker_count": broker_model["broker_count"],
        "broker_ids": broker_model["broker_ids"],
        "allowed_task_categories": broker_model["allowed_task_categories"],
        "forbidden_capabilities": broker_model["forbidden_capabilities"],
        "direct_execution_allowed": False,
        "local_mutation_allowed": False,
        "runtime_start_allowed": False,
        "model_download_allowed": False,
        "pc_control_allowed": False,
    }

