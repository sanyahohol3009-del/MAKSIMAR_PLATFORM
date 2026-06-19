from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters import ActionWorkerAdapterContract


def build_cli_worker_adapter_contract() -> ActionWorkerAdapterContract:
    return ActionWorkerAdapterContract(
        capability_id="cli_worker",
        adapter_kind="cli_worker_adapter",
        risk_class="risk_gate",
        read_only=False,
        side_effects=("shell_command", "filesystem_mutation"),
        requires_verified_owner=True,
        safe_direct_allowed=False,
        recording_required=True,
        replay_preview_required=True,
    )
