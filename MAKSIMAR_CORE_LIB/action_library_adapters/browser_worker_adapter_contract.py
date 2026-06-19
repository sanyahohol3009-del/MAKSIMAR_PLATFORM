from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters import ActionWorkerAdapterContract


def build_browser_worker_adapter_contract() -> ActionWorkerAdapterContract:
    return ActionWorkerAdapterContract(
        capability_id="browser_worker",
        adapter_kind="browser_worker_adapter",
        risk_class="safe_direct",
        read_only=False,
        side_effects=("launch_browser",),
        requires_verified_owner=True,
        safe_direct_allowed=True,
        recording_required=True,
        replay_preview_required=True,
    )
