from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_model_conductor_contract import (
    build_jarvis_live_model_conductor_contract,
)
from MAKSIMAR_CORE_LIB.real_voice_runtime.jarvis_live_disabled_gate_contract import (
    build_jarvis_live_disabled_gate_contract,
)


REQUIRED_NEXT_BATCHES: tuple[str, ...] = (
    "model_profile_resource_registry_binding",
    "worker_identity_binding_for_model_voice_screen_roles",
    "runtime_asset_storage_boundary_contract",
    "voice_live_disabled_status_read_model",
    "screen_observer_vision_candidate_binding",
    "security_action_allowlist_binding",
    "dashboard_observability_integration",
    "external_task_broker_contract_disabled",
    "live_sandbox_vendor_boundary_disabled",
)


def build_jarvis_live_readiness_summary() -> dict[str, Any]:
    conductor = build_jarvis_live_model_conductor_contract()
    disabled_gate = build_jarvis_live_disabled_gate_contract()
    conductor_read_model = conductor.to_read_model()
    gate_read_model = disabled_gate.to_read_model()

    status = "disabled_contract_entry_only"
    if disabled_gate.live_runtime_ready:
        status = "disabled_all_gates_ready"

    return {
        "summary_id": "jarvis_live_readiness_summary_v1",
        "status": status,
        "enabled": gate_read_model["jarvis_live_enabled"],
        "model_download_allowed": (
            conductor_read_model["model_download_allowed"]
            or gate_read_model["model_download_allowed"]
        ),
        "runtime_start_allowed": (
            conductor_read_model["runtime_start_allowed"]
            or gate_read_model["runtime_start_allowed"]
        ),
        "direct_execution_allowed": conductor_read_model["direct_execution_allowed"],
        "direct_shell_allowed": conductor_read_model["direct_shell_allowed"],
        "direct_core_write_allowed": conductor_read_model["direct_core_write_allowed"],
        "direct_app_control_allowed": conductor_read_model["direct_app_control_allowed"],
        "dashboard_execution_allowed": conductor_read_model["dashboard_execution_allowed"],
        "disabled_reasons": gate_read_model["denied_reasons"],
        "required_next_batches": REQUIRED_NEXT_BATCHES,
        "referenced_architecture_surfaces": conductor_read_model[
            "referenced_architecture_surfaces"
        ],
        "duplicated_registry_surfaces": conductor_read_model[
            "duplicated_registry_surfaces"
        ],
        "dashboard_safe": True,
        "read_only": True,
    }
