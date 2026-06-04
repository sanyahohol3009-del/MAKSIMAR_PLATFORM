from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import MobileWorkflowPermissionProfile
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import WorkflowApprovalGateContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_audit_contract import WorkflowAuditEventContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_safety_policy_contract import (
    WorkflowSafetyPolicyContract,
)
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import N8nAdapterContract
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.workflow_runtime_policy import WorkflowRuntimePolicy


ALLOWED_INTENT_STATES: Tuple[str, ...] = (
    "created",
    "blocked",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_allowed(value: str, field_name: str, allowed_values: Tuple[str, ...]) -> str:
    normalized = _require_non_empty_text(value, field_name)
    if normalized not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in workflow execution intent records")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in workflow execution intent records")


@dataclass(frozen=True)
class WorkflowExecutionIntentRecord:
    intent_id: str
    proposal_id: str
    graph_id: str
    adapter_id: str
    execution_tier: str
    intent_state: str
    safety_decision_code: str
    audit_event_id: str
    metadata_only: bool = True
    single_run_intent: bool = True
    policy_gated: bool = True
    contract_only: bool = True
    runtime_execution_allowed_now: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    dashboard_execution_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_phone_control_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    runtime_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "intent_id", _require_non_empty_text(self.intent_id, "intent_id"))
        object.__setattr__(self, "proposal_id", _require_non_empty_text(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "graph_id", _require_non_empty_text(self.graph_id, "graph_id"))
        object.__setattr__(self, "adapter_id", _require_non_empty_text(self.adapter_id, "adapter_id"))
        object.__setattr__(self, "execution_tier", _require_non_empty_text(self.execution_tier, "execution_tier"))
        object.__setattr__(
            self,
            "intent_state",
            _require_allowed(self.intent_state, "intent_state", ALLOWED_INTENT_STATES),
        )
        object.__setattr__(
            self,
            "safety_decision_code",
            _require_non_empty_text(self.safety_decision_code, "safety_decision_code"),
        )
        object.__setattr__(self, "audit_event_id", _require_non_empty_text(self.audit_event_id, "audit_event_id"))

        _require_true(self.metadata_only, "metadata_only")
        _require_true(self.single_run_intent, "single_run_intent")
        _require_true(self.policy_gated, "policy_gated")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.runtime_execution_allowed_now, "runtime_execution_allowed_now")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.dashboard_execution_allowed, "dashboard_execution_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")

    def intent_fingerprint(self) -> str:
        payload = {
            "intent_id": self.intent_id,
            "proposal_id": self.proposal_id,
            "graph_id": self.graph_id,
            "adapter_id": self.adapter_id,
            "execution_tier": self.execution_tier,
            "intent_state": self.intent_state,
            "safety_decision_code": self.safety_decision_code,
            "audit_event_id": self.audit_event_id,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_read_model(self) -> dict[str, object]:
        return {
            "intent_id": self.intent_id,
            "proposal_id": self.proposal_id,
            "graph_id": self.graph_id,
            "adapter_id": self.adapter_id,
            "execution_tier": self.execution_tier,
            "intent_state": self.intent_state,
            "safety_decision_code": self.safety_decision_code,
            "audit_event_id": self.audit_event_id,
            "intent_fingerprint": self.intent_fingerprint(),
            "metadata_only": self.metadata_only,
            "single_run_intent": self.single_run_intent,
            "policy_gated": self.policy_gated,
            "contract_only": self.contract_only,
            "runtime_execution_allowed_now": self.runtime_execution_allowed_now,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }


@dataclass(frozen=True)
class WorkflowExecutionIntentRuntime:
    runtime_id: str
    adapter: N8nAdapterContract
    runtime_policy: WorkflowRuntimePolicy
    safety_policy: WorkflowSafetyPolicyContract
    read_only_runtime: bool = True
    contract_only: bool = True
    execution_allowed_now: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "runtime_id", _require_non_empty_text(self.runtime_id, "runtime_id"))
        if not isinstance(self.adapter, N8nAdapterContract):
            raise TypeError("adapter must be an N8nAdapterContract")
        if not isinstance(self.runtime_policy, WorkflowRuntimePolicy):
            raise TypeError("runtime_policy must be a WorkflowRuntimePolicy")
        if not isinstance(self.safety_policy, WorkflowSafetyPolicyContract):
            raise TypeError("safety_policy must be a WorkflowSafetyPolicyContract")
        _require_true(self.read_only_runtime, "read_only_runtime")
        _require_true(self.contract_only, "contract_only")
        _require_false(self.execution_allowed_now, "execution_allowed_now")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        if self.runtime_policy.allows_adapter_contract(self.adapter) is not True:
            raise ValueError("runtime_policy does not allow the configured adapter contract")

    def create_policy_gated_intent(
        self,
        *,
        intent_id: str,
        proposal: LocalAIWorkflowProposalContract,
        permission_profile: MobileWorkflowPermissionProfile,
        approval_ticket: WorkflowApprovalGateContract,
        audit_event: WorkflowAuditEventContract,
    ) -> WorkflowExecutionIntentRecord:
        if not isinstance(audit_event, WorkflowAuditEventContract):
            raise TypeError("audit_event must be a WorkflowAuditEventContract")
        if audit_event.proposal_id != proposal.proposal_id:
            raise ValueError("audit event proposal_id must match proposal proposal_id")

        safety_decision = self.safety_policy.evaluate_proposal(
            proposal,
            permission_profile,
            approval_ticket,
        )

        intent_state = "created" if safety_decision.allowed_for_intent_creation else "blocked"
        if intent_state == "created" and self.runtime_policy.allows_execution_tier(
            proposal.graph.local_scope.execution_tier,
        ) is not True:
            intent_state = "blocked"

        return WorkflowExecutionIntentRecord(
            intent_id=intent_id,
            proposal_id=proposal.proposal_id,
            graph_id=proposal.graph.graph_id,
            adapter_id=self.adapter.adapter_id,
            execution_tier=proposal.graph.local_scope.execution_tier,
            intent_state=intent_state,
            safety_decision_code=safety_decision.decision_code,
            audit_event_id=audit_event.audit_event_id,
        )


__all__ = [
    "ALLOWED_INTENT_STATES",
    "WorkflowExecutionIntentRecord",
    "WorkflowExecutionIntentRuntime",
]
