from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import SwarmConflictReport
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import SwarmTaskRoute


@dataclass(frozen=True, slots=True)
class SwarmApprovalDecision:
    decision_id: str
    route_id: str
    selected_agent_role: str
    approved: bool
    approval_required: bool
    risk_gate_required: bool
    delegated_execution_surface: str
    action_library_candidate: bool
    direct_execution_by_swarm: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.decision_id, str) or not self.decision_id.strip():
            raise ValueError("decision_id must be a non-empty string")
        if self.direct_execution_by_swarm is not False:
            raise ValueError("direct_execution_by_swarm must be False")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "route_id": self.route_id,
            "selected_agent_role": self.selected_agent_role,
            "approved": self.approved,
            "approval_required": self.approval_required,
            "risk_gate_required": self.risk_gate_required,
            "delegated_execution_surface": self.delegated_execution_surface,
            "action_library_candidate": self.action_library_candidate,
            "direct_execution_by_swarm": self.direct_execution_by_swarm,
            "reason_codes": self.reason_codes,
        }


def build_swarm_approval_decision(route: SwarmTaskRoute, conflict_report: SwarmConflictReport) -> SwarmApprovalDecision:
    if conflict_report.conflict_detected:
        return SwarmApprovalDecision(
            decision_id="swarm_approval_decision_v1",
            route_id=route.route_id,
            selected_agent_role=route.selected_agent_role,
            approved=False,
            approval_required=True,
            risk_gate_required=conflict_report.risk_gate_required,
            delegated_execution_surface="risk_gate"
            if conflict_report.risk_gate_required
            else route.delegated_execution_surface,
            action_library_candidate=route.action_library_delegation_required,
            direct_execution_by_swarm=False,
            reason_codes=conflict_report.reason_codes,
        )
    if route.action_library_delegation_required:
        approved = route.task_contract.safe_direct_action_candidate
        return SwarmApprovalDecision(
            decision_id="swarm_approval_decision_v1",
            route_id=route.route_id,
            selected_agent_role=route.selected_agent_role,
            approved=approved,
            approval_required=not approved,
            risk_gate_required=False,
            delegated_execution_surface="action_library",
            action_library_candidate=True,
            direct_execution_by_swarm=False,
            reason_codes=("delegated_to_action_library",),
        )
    if route.risk_gate_required:
        return SwarmApprovalDecision(
            decision_id="swarm_approval_decision_v1",
            route_id=route.route_id,
            selected_agent_role=route.selected_agent_role,
            approved=False,
            approval_required=True,
            risk_gate_required=True,
            delegated_execution_surface="risk_gate",
            action_library_candidate=False,
            direct_execution_by_swarm=False,
            reason_codes=("risk_gate_required",),
        )
    return SwarmApprovalDecision(
        decision_id="swarm_approval_decision_v1",
        route_id=route.route_id,
        selected_agent_role=route.selected_agent_role,
        approved=True,
        approval_required=False,
        risk_gate_required=False,
        delegated_execution_surface="none",
        action_library_candidate=False,
        direct_execution_by_swarm=False,
        reason_codes=("proposal_only_read_path",),
    )
