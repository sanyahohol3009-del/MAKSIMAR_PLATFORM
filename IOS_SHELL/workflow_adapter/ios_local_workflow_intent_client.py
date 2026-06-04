from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

from IOS_SHELL.workflow_adapter.ios_workflow_permission_bridge import (
    IOSWorkflowPermissionBridge,
)
from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_approval_gate_contract import WorkflowApprovalGateContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_audit_contract import WorkflowAuditEventContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_safety_policy_contract import (
    WorkflowSafetyDecision,
    WorkflowSafetyPolicyContract,
    build_workflow_safety_policy_contract,
)


IOS_LOCAL_WORKFLOW_PLATFORM = "ios"


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in iOS local workflow intent client")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in iOS local workflow intent client")


@dataclass(frozen=True)
class IOSLocalWorkflowIntentDecision:
    local_intent_id: str
    client_id: str
    proposal_id: str
    graph_id: str
    allowed_for_local_intent: bool
    decision_code: str
    safety_decision: WorkflowSafetyDecision
    audit_event_id: str
    platform: str = IOS_LOCAL_WORKFLOW_PLATFORM
    metadata_only: bool = True
    local_first: bool = True
    server_optional: bool = True
    offline_queue_eligible: bool = True
    execution_performed: bool = False
    direct_phone_control_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed_by_default: bool = False
    socket_allowed_by_default: bool = False
    tunnel_allowed_by_default: bool = False
    runtime_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "local_intent_id", _require_non_empty_text(self.local_intent_id, "local_intent_id"))
        object.__setattr__(self, "client_id", _require_non_empty_text(self.client_id, "client_id"))
        object.__setattr__(self, "proposal_id", _require_non_empty_text(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "graph_id", _require_non_empty_text(self.graph_id, "graph_id"))
        if not isinstance(self.allowed_for_local_intent, bool):
            raise TypeError("allowed_for_local_intent must be a boolean")
        object.__setattr__(self, "decision_code", _require_non_empty_text(self.decision_code, "decision_code"))
        if not isinstance(self.safety_decision, WorkflowSafetyDecision):
            raise TypeError("safety_decision must be a WorkflowSafetyDecision")
        object.__setattr__(self, "audit_event_id", _require_non_empty_text(self.audit_event_id, "audit_event_id"))
        if self.platform != IOS_LOCAL_WORKFLOW_PLATFORM:
            raise ValueError("platform must be ios")

        _require_true(self.metadata_only, "metadata_only")
        _require_true(self.local_first, "local_first")
        _require_true(self.server_optional, "server_optional")
        _require_true(self.offline_queue_eligible, "offline_queue_eligible")
        _require_false(self.execution_performed, "execution_performed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed_by_default, "network_allowed_by_default")
        _require_false(self.socket_allowed_by_default, "socket_allowed_by_default")
        _require_false(self.tunnel_allowed_by_default, "tunnel_allowed_by_default")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")

    def intent_fingerprint(self) -> str:
        payload = {
            "local_intent_id": self.local_intent_id,
            "client_id": self.client_id,
            "proposal_id": self.proposal_id,
            "graph_id": self.graph_id,
            "allowed_for_local_intent": self.allowed_for_local_intent,
            "decision_code": self.decision_code,
            "audit_event_id": self.audit_event_id,
            "platform": self.platform,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    def to_read_model(self) -> dict[str, object]:
        return {
            "local_intent_id": self.local_intent_id,
            "client_id": self.client_id,
            "proposal_id": self.proposal_id,
            "graph_id": self.graph_id,
            "allowed_for_local_intent": self.allowed_for_local_intent,
            "decision_code": self.decision_code,
            "safety_decision": self.safety_decision.to_read_model(),
            "audit_event_id": self.audit_event_id,
            "platform": self.platform,
            "intent_fingerprint": self.intent_fingerprint(),
            "metadata_only": self.metadata_only,
            "local_first": self.local_first,
            "server_optional": self.server_optional,
            "offline_queue_eligible": self.offline_queue_eligible,
            "execution_performed": self.execution_performed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "socket_allowed_by_default": self.socket_allowed_by_default,
            "tunnel_allowed_by_default": self.tunnel_allowed_by_default,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }


@dataclass(frozen=True)
class IOSLocalWorkflowIntentClient:
    client_id: str
    permission_bridge: IOSWorkflowPermissionBridge
    safety_policy: WorkflowSafetyPolicyContract
    local_first: bool = True
    server_optional: bool = True
    offline_queue_enabled: bool = True
    metadata_only: bool = True
    contract_only: bool = True
    execution_performed: bool = False
    direct_phone_control_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed_by_default: bool = False
    socket_allowed_by_default: bool = False
    tunnel_allowed_by_default: bool = False
    runtime_mutation_allowed: bool = False
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "client_id", _require_non_empty_text(self.client_id, "client_id"))
        if not isinstance(self.permission_bridge, IOSWorkflowPermissionBridge):
            raise TypeError("permission_bridge must be an IOSWorkflowPermissionBridge")
        if not isinstance(self.safety_policy, WorkflowSafetyPolicyContract):
            raise TypeError("safety_policy must be a WorkflowSafetyPolicyContract")

        _require_true(self.local_first, "local_first")
        _require_true(self.server_optional, "server_optional")
        _require_true(self.offline_queue_enabled, "offline_queue_enabled")
        _require_true(self.metadata_only, "metadata_only")
        _require_true(self.contract_only, "contract_only")
        _require_false(self.execution_performed, "execution_performed")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed_by_default, "network_allowed_by_default")
        _require_false(self.socket_allowed_by_default, "socket_allowed_by_default")
        _require_false(self.tunnel_allowed_by_default, "tunnel_allowed_by_default")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def build_local_intent_id(self, proposal: LocalAIWorkflowProposalContract, audit_event: WorkflowAuditEventContract) -> str:
        payload = {
            "client_id": self.client_id,
            "platform": IOS_LOCAL_WORKFLOW_PLATFORM,
            "proposal_id": proposal.proposal_id,
            "graph_id": proposal.graph.graph_id,
            "audit_event_id": audit_event.audit_event_id,
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        return f"ios.local.workflow.intent.{digest[:24]}"

    def request_local_workflow_intent(
        self,
        *,
        proposal: LocalAIWorkflowProposalContract,
        approval_ticket: WorkflowApprovalGateContract,
        audit_event: WorkflowAuditEventContract,
    ) -> IOSLocalWorkflowIntentDecision:
        if not isinstance(proposal, LocalAIWorkflowProposalContract):
            raise TypeError("proposal must be a LocalAIWorkflowProposalContract")
        if not isinstance(approval_ticket, WorkflowApprovalGateContract):
            raise TypeError("approval_ticket must be a WorkflowApprovalGateContract")
        if not isinstance(audit_event, WorkflowAuditEventContract):
            raise TypeError("audit_event must be a WorkflowAuditEventContract")
        if audit_event.proposal_id != proposal.proposal_id:
            raise ValueError("audit_event proposal_id must match proposal_id")

        permission_result = self.permission_bridge.evaluate_proposal(proposal)
        if permission_result.permission_decision.allowed is not True:
            safety_decision = WorkflowSafetyDecision(
                allowed_for_intent_creation=False,
                decision_code="permission_denied",
                reason="iOS permission bridge denied the local workflow proposal",
                permission_decision=permission_result.permission_decision,
            )
        else:
            safety_decision = self.safety_policy.evaluate_proposal(
                proposal,
                permission_result.permission_profile,
                approval_ticket,
            )

        allowed = safety_decision.allowed_for_intent_creation is True
        return IOSLocalWorkflowIntentDecision(
            local_intent_id=self.build_local_intent_id(proposal, audit_event),
            client_id=self.client_id,
            proposal_id=proposal.proposal_id,
            graph_id=proposal.graph.graph_id,
            allowed_for_local_intent=allowed,
            decision_code=safety_decision.decision_code,
            safety_decision=safety_decision,
            audit_event_id=audit_event.audit_event_id,
        )


def build_ios_local_workflow_intent_client(
    *,
    client_id: str = "ios.local.workflow.intent.client.v1",
    permission_bridge: IOSWorkflowPermissionBridge,
    safety_policy: WorkflowSafetyPolicyContract | None = None,
) -> IOSLocalWorkflowIntentClient:
    return IOSLocalWorkflowIntentClient(
        client_id=client_id,
        permission_bridge=permission_bridge,
        safety_policy=safety_policy or build_workflow_safety_policy_contract(),
    )


__all__ = [
    "IOS_LOCAL_WORKFLOW_PLATFORM",
    "IOSLocalWorkflowIntentClient",
    "IOSLocalWorkflowIntentDecision",
    "build_ios_local_workflow_intent_client",
]
