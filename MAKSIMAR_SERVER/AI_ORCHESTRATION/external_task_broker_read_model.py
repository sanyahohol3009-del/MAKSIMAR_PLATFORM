from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.external_task_broker_contract import (
    build_external_task_broker_contract,
)


def build_external_task_broker_read_model() -> dict[str, Any]:
    contract = build_external_task_broker_contract().to_read_model()
    return {
        "summary_id": "external_task_broker_read_model_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "broker_count": contract["broker_count"],
        "broker_ids": contract["broker_ids"],
        "broker_modes": contract["broker_modes"],
        "allowed_task_categories": contract["allowed_task_categories"],
        "forbidden_capabilities": contract["forbidden_capabilities"],
        "proposal_only": True,
        "direct_execution_allowed": False,
        "local_mutation_allowed": False,
        "runtime_start_allowed": False,
        "model_download_allowed": False,
        "pc_control_allowed": False,
        "external_api_call_allowed": False,
        "network_call_allowed": False,
        "brokers": contract["brokers"],
    }

