from __future__ import annotations

"""Typed JL-14/P10 PC-operation boundary.

The canonical Semantic Spine owns natural-language understanding and policy.  This
module only validates and resolves an already selected operation.  JL-14 has no
runtime executor integration yet, so a successful resolution never claims that
the action was executed or is currently available for execution.
"""

from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    IdentityContext,
    PermissionDecision,
)
from MAKSIMAR_CORE_LIB.security_layer.approval_service_contract import (
    ApprovalRecord,
    ApprovalStatus,
)
from MAKSIMAR_CORE_LIB.security_layer.jarvis_family_profile_contract import (
    build_owner_profile,
)
from MAKSIMAR_CORE_LIB.security_layer.jarvis_speaker_profile_resolver import (
    resolve_family_profile,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeIdentity
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    resolve_direct_pc_action,
)


REQUIRED_OPERATION_FIELDS = (
    "operation_id",
    "target",
    "parameters",
    "identity_context",
    "policy_decision",
    "trace_id",
    "device_context",
)


def resolve_owner_pc_operation(request: dict[str, Any]) -> dict[str, Any]:
    """Resolve one fully typed, pre-authorized PC operation; never parse text."""
    unresolved = _unresolved()
    if not isinstance(request, dict) or any(field not in request for field in REQUIRED_OPERATION_FIELDS):
        return unresolved

    operation_id = request.get("operation_id")
    target = request.get("target")
    parameters = request.get("parameters")
    identity = request.get("identity_context")
    policy = request.get("policy_decision")
    trace_id = request.get("trace_id")
    device_context = request.get("device_context")
    if (
        not isinstance(operation_id, str)
        or not operation_id.strip()
        or not isinstance(target, str)
        or not target.strip()
        or not isinstance(parameters, dict)
        or not isinstance(identity, IdentityContext)
        or not isinstance(policy, PermissionDecision)
        or not isinstance(trace_id, str)
        or not trace_id.strip()
        or not isinstance(device_context, CanonicalNodeIdentity)
    ):
        return unresolved

    operation_id = operation_id.strip()
    trace_id = trace_id.strip()
    resolved = resolve_direct_pc_action(operation_id)
    if not resolved.get("ok"):
        return unresolved
    if not _valid_identity(identity):
        return _denied(operation_id, "identity_not_authorized")
    if not _valid_policy(policy, operation_id=operation_id, trace_id=trace_id):
        return _denied(operation_id, "policy_denied")
    if policy.approval_required and not _valid_approval(
        request.get("approval_evidence"), identity=identity, trace_id=trace_id
    ):
        return _denied(operation_id, "approval_required")
    if not _valid_target_and_parameters(resolved, target=target, parameters=parameters):
        return _denied(operation_id, "invalid_typed_target_or_parameters")

    resolution = {
        "ok": True,
        "matched": True,
        "route": "CANONICAL_PC_OPERATION",
        "status": "RESOLVED_OPERATION",
        "operation_id": operation_id,
        "action_id": operation_id,
        "action_family": resolved["action_family"],
        "target": target.strip(),
        "parameters": dict(parameters),
        "trace_id": trace_id,
        "identity_context": identity.to_read_model(),
        "policy_decision": policy.to_read_model(),
        "device_context": {"node_id": device_context.node_id, "node_type": device_context.node_type},
        "executor_function": resolved["executor_function"],
        "owner_pc_action_eligible": True,
        "policy_execution_allowed": True,
        "pc_executor_available": None,
        "pc_operation_authorized_for_this_turn": True,
        "canonical_write_allowed": False,
        "executed": False,
        "execution_receipt": None,
        "integration_owner": "P10 device adapter integration gate",
    }
    return {**resolved, **resolution}


def _valid_identity(identity: IdentityContext) -> bool:
    if not identity.owner_authorized:
        return False
    profile = resolve_family_profile(
        identity_id=identity.identity_id,
        profile_type=identity.profile_type,
    )
    owner_contract = build_owner_profile()
    return bool(
        profile is not None
        and profile.profile_type == "owner"
        and profile.direct_pc_action_eligible
        and owner_contract.can_request_pc_action
    )


def _valid_policy(policy: PermissionDecision, *, operation_id: str, trace_id: str) -> bool:
    return bool(
        policy.granted
        and policy.capability_id == "pc.control"
        and policy.operation_id == operation_id
        and policy.trace_id == trace_id
    )


def _valid_approval(
    approval: object,
    *,
    identity: IdentityContext,
    trace_id: str,
) -> bool:
    return bool(
        isinstance(approval, ApprovalRecord)
        and approval.status is ApprovalStatus.APPROVED
        and approval.trace_id == trace_id
        and approval.approver_id == identity.identity_id
    )


def _valid_target_and_parameters(
    resolved: dict[str, Any],
    *,
    target: str,
    parameters: dict[str, Any],
) -> bool:
    expected_target = str(resolved.get("target", "")).strip()
    if expected_target and target.strip() != expected_target:
        return False
    required_parameters = tuple(resolved.get("required_parameters", ()))
    if any(key not in parameters for key in required_parameters):
        return False
    if "text" in required_parameters and (
        not isinstance(parameters.get("text"), str) or not parameters["text"].strip()
    ):
        return False
    if "query" in required_parameters and (
        not isinstance(parameters.get("query"), str) or not parameters["query"].strip()
    ):
        return False
    return set(parameters).issubset(set(resolved.get("allowed_parameters", ())))


def _unresolved() -> dict[str, Any]:
    return {
        "ok": False,
        "matched": False,
        "route": "UNRESOLVED_OPERATION",
        "status": "UNRESOLVED_OPERATION",
        "owner_pc_action_eligible": None,
        "policy_execution_allowed": None,
        "pc_executor_available": None,
        "pc_operation_authorized_for_this_turn": False,
        "canonical_write_allowed": False,
        "executed": False,
        "execution_receipt": None,
    }


def _denied(operation_id: str, reason: str) -> dict[str, Any]:
    return {
        "ok": False,
        "matched": True,
        "route": "CANONICAL_PC_OPERATION",
        "status": "DENIED",
        "operation_id": operation_id,
        "blocked_reason": reason,
        "owner_pc_action_eligible": reason != "identity_not_authorized",
        "policy_execution_allowed": False,
        "pc_executor_available": None,
        "pc_operation_authorized_for_this_turn": False,
        "canonical_write_allowed": False,
        "executed": False,
        "execution_receipt": None,
    }
