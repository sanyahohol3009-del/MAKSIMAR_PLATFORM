from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters import ActionWorkerAdapterContract


def build_cad_cam_worker_adapter_contract() -> ActionWorkerAdapterContract:
    return ActionWorkerAdapterContract(
        capability_id="cad_cam_worker",
        adapter_kind="cad_cam_worker_adapter",
        risk_class="risk_gate",
        read_only=False,
        side_effects=("machine_control", "fabrication_command"),
        requires_verified_owner=True,
        safe_direct_allowed=False,
        recording_required=True,
        replay_preview_required=True,
    )
