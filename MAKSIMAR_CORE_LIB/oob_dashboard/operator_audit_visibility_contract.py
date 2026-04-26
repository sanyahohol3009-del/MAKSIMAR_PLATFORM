from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_models import (
    OperatorAuditVisibilityContract,
    OperatorAuditVisibilityEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    build_operator_control_plane_handoff_contract,
)


def build_operator_audit_visibility_contract() -> OperatorAuditVisibilityContract:
    """Build the canonical operator audit visibility contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    handoff_contract = build_operator_control_plane_handoff_contract()

    handoff_map = {entry.dashboard_id: entry for entry in handoff_contract.entries}

    entries = tuple(
        OperatorAuditVisibilityEntry(
            dashboard_id=entry.dashboard_id,
            audit_surface_id="audit_timeline_surface",
            audit_scope="operator_action_audit",
            audit_visibility_mode="always_visible_audit_path",
            hidden_audit_allowed=False,
            policy_visibility_required=handoff_map[entry.dashboard_id].policy_gate_required,
            approval_visibility_required=handoff_map[entry.dashboard_id].approval_required,
            description=(
                "Canonical operator audit visibility contract. Submitted actions must "
                "remain visible through the audit path, including policy and approval "
                "visibility, with no hidden audit mode."
            ),
        )
        for entry in dashboard_contract.entries
    )

    return OperatorAuditVisibilityContract(entries=entries)
