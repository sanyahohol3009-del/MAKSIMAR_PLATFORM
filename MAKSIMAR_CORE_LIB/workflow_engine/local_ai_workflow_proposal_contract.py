from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import WorkflowGraphContract


ALLOWED_WORKFLOW_RISK_LEVELS: Tuple[str, ...] = ("low", "medium", "high", "critical")
ALLOWED_PROPOSAL_STATES: Tuple[str, ...] = (
    "draft",
    "awaiting_permission",
    "awaiting_approval",
    "approved_for_intent",
    "rejected",
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


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str, *, require_non_empty: bool) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if require_non_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in local AI workflow proposal contracts")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in local AI workflow proposal contracts")


@dataclass(frozen=True)
class LocalAIWorkflowProposalContract:
    proposal_id: str
    requester_id: str
    graph: WorkflowGraphContract
    natural_language_goal: str
    requested_capability_refs: Tuple[str, ...]
    risk_level: str
    proposal_state: str = "draft"
    revision: int = 1
    requires_permission: bool = True
    requires_user_approval: bool = True
    sandbox_preview_required: bool = True
    audit_required: bool = True
    contract_only: bool = True
    proposal_is_execution_authority: bool = False
    execution_authority_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    network_socket_tunnel_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    runtime_mutation_allowed: bool = False
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "proposal_id", _require_non_empty_text(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "requester_id", _require_non_empty_text(self.requester_id, "requester_id"))
        if not isinstance(self.graph, WorkflowGraphContract):
            raise TypeError("graph must be a WorkflowGraphContract")
        object.__setattr__(
            self,
            "natural_language_goal",
            _require_non_empty_text(self.natural_language_goal, "natural_language_goal"),
        )
        object.__setattr__(
            self,
            "requested_capability_refs",
            _normalize_text_tuple(
                self.requested_capability_refs,
                "requested_capability_refs",
                require_non_empty=True,
            ),
        )
        object.__setattr__(
            self,
            "risk_level",
            _require_allowed(self.risk_level, "risk_level", ALLOWED_WORKFLOW_RISK_LEVELS),
        )
        object.__setattr__(
            self,
            "proposal_state",
            _require_allowed(self.proposal_state, "proposal_state", ALLOWED_PROPOSAL_STATES),
        )
        if not isinstance(self.revision, int) or self.revision < 1:
            raise ValueError("revision must be a positive integer")

        _require_true(self.requires_permission, "requires_permission")
        _require_true(self.requires_user_approval, "requires_user_approval")
        _require_true(self.sandbox_preview_required, "sandbox_preview_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.proposal_is_execution_authority, "proposal_is_execution_authority")
        _require_false(self.execution_authority_allowed, "execution_authority_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def proposal_fingerprint(self) -> str:
        payload = {
            "proposal_id": self.proposal_id,
            "requester_id": self.requester_id,
            "graph_id": self.graph.graph_id,
            "graph_schema_version": self.graph.schema_version,
            "natural_language_goal": self.natural_language_goal,
            "requested_capability_refs": self.requested_capability_refs,
            "risk_level": self.risk_level,
            "proposal_state": self.proposal_state,
            "revision": self.revision,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_read_model(self) -> dict[str, object]:
        return {
            "proposal_id": self.proposal_id,
            "requester_id": self.requester_id,
            "graph_id": self.graph.graph_id,
            "natural_language_goal": self.natural_language_goal,
            "requested_capability_refs": self.requested_capability_refs,
            "risk_level": self.risk_level,
            "proposal_state": self.proposal_state,
            "revision": self.revision,
            "proposal_fingerprint": self.proposal_fingerprint(),
            "requires_permission": self.requires_permission,
            "requires_user_approval": self.requires_user_approval,
            "sandbox_preview_required": self.sandbox_preview_required,
            "audit_required": self.audit_required,
            "contract_only": self.contract_only,
            "proposal_is_execution_authority": self.proposal_is_execution_authority,
            "execution_authority_allowed": self.execution_authority_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "network_socket_tunnel_allowed": self.network_socket_tunnel_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "platform_api_call_allowed": self.platform_api_call_allowed,
        }


def build_local_ai_workflow_proposal_contract(
    *,
    proposal_id: str,
    requester_id: str,
    graph: WorkflowGraphContract,
    natural_language_goal: str,
    requested_capability_refs: Tuple[str, ...],
    risk_level: str = "medium",
) -> LocalAIWorkflowProposalContract:
    return LocalAIWorkflowProposalContract(
        proposal_id=proposal_id,
        requester_id=requester_id,
        graph=graph,
        natural_language_goal=natural_language_goal,
        requested_capability_refs=requested_capability_refs,
        risk_level=risk_level,
        proposal_state="awaiting_permission",
    )


__all__ = [
    "ALLOWED_PROPOSAL_STATES",
    "ALLOWED_WORKFLOW_RISK_LEVELS",
    "LocalAIWorkflowProposalContract",
    "build_local_ai_workflow_proposal_contract",
]
