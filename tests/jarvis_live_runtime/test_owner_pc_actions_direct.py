from __future__ import annotations

from dataclasses import replace

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    IdentityContext,
    PermissionDecision,
)
from MAKSIMAR_CORE_LIB.security_layer.approval_service_contract import (
    ApprovalRecord,
    ApprovalStatus,
)
from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeIdentity
from tools.jarvis_live_runtime.owner_pc_actions import resolve_owner_pc_operation
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    build_windows_edge_executor_payload,
)


TRACE_ID = "trace_pc_boundary_001"
OWNER = IdentityContext(
    "aleksandr", "local_terminal_session", "owner", True, True, "Александр", "JARVIS"
)
DEVICE = CanonicalNodeIdentity("dev_001", "dev_node")


def _policy(operation_id: str, *, granted: bool = True, approval_required: bool = False) -> PermissionDecision:
    return PermissionDecision(
        granted=granted,
        capability_id="pc.control",
        identity_source=OWNER.identity_source,
        policy_version="semantic_policy.v1",
        denial_reason="" if granted else "step_policy_denied",
        trace_id=TRACE_ID,
        operation_id=operation_id,
        approval_required=approval_required,
    )


def _request(
    operation_id: str,
    target: str,
    parameters: dict[str, object] | None = None,
    *,
    identity: IdentityContext = OWNER,
    policy: PermissionDecision | None = None,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "target": target,
        "parameters": {} if parameters is None else parameters,
        "identity_context": identity,
        "policy_decision": policy or _policy(operation_id),
        "trace_id": TRACE_ID,
        "device_context": DEVICE,
    }


@pytest.mark.parametrize(
    ("operation_id", "target", "parameters", "executor_function"),
    (
        ("open_browser", "default_browser", {}, "open_browser"),
        ("type_text", "active_window", {"text": "typed boundary"}, "type_text"),
        ("close_opera", "opera", {}, "close_one_window"),
        ("close_all_opera", "opera", {}, "kill_all_processes"),
        ("volume_up", "system_volume", {}, "volume_up"),
        ("volume_down", "system_volume", {}, "volume_down"),
        ("volume_mute", "system_volume", {}, "volume_mute"),
    ),
)
def test_verified_owner_low_risk_operation_resolves_to_windows_mapping(
    operation_id: str,
    target: str,
    parameters: dict[str, object],
    executor_function: str,
) -> None:
    result = resolve_owner_pc_operation(_request(operation_id, target, parameters))

    assert result["ok"] is True
    assert result["owner_pc_action_eligible"] is True
    assert result["policy_execution_allowed"] is True
    assert result["pc_executor_available"] is None
    assert result["pc_operation_authorized_for_this_turn"] is True
    assert "runtime_target" not in result
    windows_executor = build_windows_edge_executor_payload(result)
    assert windows_executor["platform_adapter_id"] == "windows_edge_adapter"
    assert windows_executor["device_context"] == {"node_id": "dev_001", "node_type": "dev_node"}
    assert windows_executor["executor_function"] == executor_function
    assert windows_executor["target"] == target
    assert windows_executor["parameters"] == parameters
    assert result["executed"] is False
    assert result["execution_receipt"] is None


def test_close_one_window_and_kill_all_keep_distinct_windows_semantics() -> None:
    close_one = resolve_owner_pc_operation(_request("close_opera", "opera"))
    kill_all = resolve_owner_pc_operation(_request("close_all_opera", "opera"))

    close_one_windows = build_windows_edge_executor_payload(close_one)
    kill_all_windows = build_windows_edge_executor_payload(kill_all)
    assert close_one_windows["close_strategy"] == "graceful_single_window"
    assert close_one_windows["preferred_mechanism"] == "WM_CLOSE_or_AltF4"
    assert kill_all_windows["close_strategy"] == "force_all_processes"
    assert kill_all_windows["preferred_mechanism"] == "targeted_process_identity_required"


@pytest.mark.parametrize(
    "identity",
    (
        replace(OWNER, owner_verified=False),
        replace(OWNER, trusted=False),
        IdentityContext("maksim", "authenticated_http_session", "child", False, True, "Максим"),
        IdentityContext("anonymous", "http_unverified", "unknown", False, False),
    ),
)
def test_unverified_child_anonymous_or_untrusted_identity_cannot_inherit_owner_rights(
    identity: IdentityContext,
) -> None:
    result = resolve_owner_pc_operation(_request("open_browser", "default_browser", identity=identity))
    assert result["status"] == "DENIED"
    assert result["blocked_reason"] == "identity_not_authorized"
    assert result["owner_pc_action_eligible"] is False
    assert result["pc_operation_authorized_for_this_turn"] is False


def test_policy_denial_is_not_re_evaluated_or_overridden() -> None:
    result = resolve_owner_pc_operation(
        _request("open_browser", "default_browser", policy=_policy("open_browser", granted=False))
    )
    assert result["status"] == "DENIED"
    assert result["blocked_reason"] == "policy_denied"


def test_approval_required_without_valid_evidence_is_denied() -> None:
    result = resolve_owner_pc_operation(
        _request(
            "open_browser",
            "default_browser",
            policy=_policy("open_browser", approval_required=True),
        )
    )
    assert result["status"] == "DENIED"
    assert result["blocked_reason"] == "approval_required"


def test_approval_required_with_matching_canonical_evidence_resolves() -> None:
    operation_request = _request(
        "open_browser",
        "default_browser",
        policy=_policy("open_browser", approval_required=True),
    )
    operation_request["approval_evidence"] = ApprovalRecord(
        approval_id="approval_pc_001",
        request_id="request_pc_001",
        trace_id=TRACE_ID,
        status=ApprovalStatus.APPROVED,
        approver_id="aleksandr",
        reason="explicit owner approval",
    )

    result = resolve_owner_pc_operation(operation_request)
    assert result["status"] == "RESOLVED_OPERATION"
    assert result["pc_operation_authorized_for_this_turn"] is True


def test_unknown_operation_and_raw_string_are_unresolved() -> None:
    unknown = resolve_owner_pc_operation(_request("not_registered", "desktop"))
    raw = resolve_owner_pc_operation("открой браузер")  # type: ignore[arg-type]

    assert unknown["status"] == "UNRESOLVED_OPERATION"
    assert raw["status"] == "UNRESOLVED_OPERATION"


@pytest.mark.parametrize(
    "operation_request",
    (
        {},
        {"operation_id": "open_browser"},
        {
            "operation_id": "type_text",
            "target": "active_window",
            "parameters": {},
            "identity_context": OWNER,
            "policy_decision": _policy("type_text"),
            "trace_id": TRACE_ID,
        },
    ),
)
def test_missing_required_typed_fields_or_parameters_fail_closed(operation_request: dict[str, object]) -> None:
    result = resolve_owner_pc_operation(operation_request)
    assert result["ok"] is False
    assert result["executed"] is False


def test_target_policy_operation_and_trace_must_match_typed_request() -> None:
    wrong_target = resolve_owner_pc_operation(_request("close_opera", "chrome"))
    wrong_operation = resolve_owner_pc_operation(
        _request("open_browser", "default_browser", policy=_policy("volume_up"))
    )
    wrong_trace_policy = replace(_policy("open_browser"), trace_id="other_trace")
    wrong_trace = resolve_owner_pc_operation(
        _request("open_browser", "default_browser", policy=wrong_trace_policy)
    )

    assert wrong_target["blocked_reason"] == "invalid_typed_target_or_parameters"
    assert wrong_operation["blocked_reason"] == "policy_denied"
    assert wrong_trace["blocked_reason"] == "policy_denied"
