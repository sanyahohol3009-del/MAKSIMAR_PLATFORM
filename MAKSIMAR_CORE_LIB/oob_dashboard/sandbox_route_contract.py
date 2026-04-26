from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.replay_artifact_contract import (
    build_replay_artifact_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.sandbox_route_models import (
    SandboxRouteContract,
    SandboxRouteEntry,
)


def build_sandbox_route_contract() -> SandboxRouteContract:
    """Build canonical sandbox route contract."""
    replay_artifact_contract = build_replay_artifact_contract()

    entries = tuple(
        SandboxRouteEntry(
            sandbox_route_id=f"sandbox_route_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            panel_id=entry.panel_id,
            workspace_id=entry.workspace_id,
            sandbox_route_state="sandbox_route_ready",
            sandbox_route_class=(
                "approval_bound_sandbox_route"
                if entry.approval_required
                else "read_only_sandbox_route"
            ),
            sandbox_route_mode=(
                "preview_review_approval_simulation_replay_sandbox_route"
                if entry.approval_required
                else "preview_review_simulation_replay_sandbox_route"
            ),
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            sandbox_visible=entry.replay_visible,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical sandbox route entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(replay_artifact_contract.entries, start=1)
    )

    return SandboxRouteContract(
        contract_id="sandbox_route_contract_001",
        total_entries=len(entries),
        read_only_sandbox_entries=sum(
            1
            for entry in entries
            if entry.sandbox_route_class == "read_only_sandbox_route"
        ),
        approval_bound_sandbox_entries=sum(
            1
            for entry in entries
            if entry.sandbox_route_class == "approval_bound_sandbox_route"
        ),
        sandbox_visible_entries=sum(1 for entry in entries if entry.sandbox_visible),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
