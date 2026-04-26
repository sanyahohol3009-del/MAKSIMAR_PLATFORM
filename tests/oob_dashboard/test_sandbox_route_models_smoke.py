from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.sandbox_route_models import (
    SandboxRouteContract,
    SandboxRouteEntry,
)


def test_sandbox_route_entry_builds() -> None:
    """Sandbox route entry should build successfully."""
    entry = SandboxRouteEntry(
        sandbox_route_id="sandbox_route_001",
        operator_intent_id="operator_intent_001",
        panel_id="action_queue",
        workspace_id="workspace_operator_main",
        sandbox_route_state="sandbox_route_ready",
        sandbox_route_class="read_only_sandbox_route",
        sandbox_route_mode="preview_review_simulation_replay_sandbox_route",
        approval_required=False,
        handoff_ready=True,
        sandbox_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Canonical sandbox route entry.",
    )

    assert entry.sandbox_route_id == "sandbox_route_001"
    assert entry.sandbox_route_state == "sandbox_route_ready"
    assert entry.sandbox_route_class == "read_only_sandbox_route"


def test_sandbox_route_entry_rejects_non_sandbox_visible() -> None:
    """Sandbox route entry must remain sandbox-visible."""
    with pytest.raises(
        ValueError,
        match="sandbox_visible must remain true for canonical sandbox routes.",
    ):
        SandboxRouteEntry(
            sandbox_route_id="sandbox_route_invalid",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            sandbox_route_state="sandbox_route_ready",
            sandbox_route_class="read_only_sandbox_route",
            sandbox_route_mode="preview_review_simulation_replay_sandbox_route",
            approval_required=False,
            handoff_ready=True,
            sandbox_visible=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid sandbox route entry.",
        )


def test_sandbox_route_contract_builds() -> None:
    """Sandbox route contract should build successfully."""
    entries = (
        SandboxRouteEntry(
            sandbox_route_id="sandbox_route_001",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            sandbox_route_state="sandbox_route_ready",
            sandbox_route_class="read_only_sandbox_route",
            sandbox_route_mode="preview_review_simulation_replay_sandbox_route",
            approval_required=False,
            handoff_ready=True,
            sandbox_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Read-only sandbox route entry.",
        ),
        SandboxRouteEntry(
            sandbox_route_id="sandbox_route_002",
            operator_intent_id="operator_intent_003",
            panel_id="approval_queue",
            workspace_id="workspace_operator_main",
            sandbox_route_state="sandbox_route_ready",
            sandbox_route_class="approval_bound_sandbox_route",
            sandbox_route_mode="preview_review_approval_simulation_replay_sandbox_route",
            approval_required=True,
            handoff_ready=True,
            sandbox_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Approval-bound sandbox route entry.",
        ),
    )

    contract = SandboxRouteContract(
        contract_id="sandbox_route_contract_001",
        total_entries=2,
        read_only_sandbox_entries=1,
        approval_bound_sandbox_entries=1,
        sandbox_visible_entries=2,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.read_only_sandbox_entries == 1
    assert contract.approval_bound_sandbox_entries == 1
