from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import PermissionDecision
from MAKSIMAR_CORE_LIB.security_layer.host_approval_handshake import HostApprovalStore


def _decision(step: str = "step_a") -> PermissionDecision:
    return PermissionDecision(
        granted=False, capability_id="example.capability", identity_source="host",
        policy_version="semantic_policy.v1", denial_reason="approval_required",
        trace_id="trace_x", operation_id="example.mutate", approval_required=True,
        step_id=step,
    )


def test_host_approval_resumes_exact_stored_step_once() -> None:
    store = HostApprovalStore()
    resumed: list[str] = []
    pending = store.create(
        request_id="request_x", session_id="session_x", decision=_decision(),
        plan_step={"step_id": "step_a", "capability_id": "example.capability"},
        description="Approve bounded example mutation",
        resume=lambda decision: resumed.append(decision.step_id) or {"status": "COMPLETE"},
    )
    record, decision, result = store.decide(pending.approval_id, approved=True, approver_id="owner", session_id="session_x")
    assert record.status == "CONSUMED"
    assert decision is not None and decision.step_id == "step_a" and decision.granted is True
    assert result == {"status": "COMPLETE"}
    assert resumed == ["step_a"]


def test_host_approval_denial_has_no_resume_and_replay_is_rejected() -> None:
    store = HostApprovalStore()
    pending = store.create(
        request_id="request_x", session_id="session_x", decision=_decision(),
        plan_step={"step_id": "step_a"}, description="Approve bounded example mutation",
    )
    record, decision, result = store.decide(pending.approval_id, approved=False, approver_id="owner", session_id="session_x")
    assert record.status == "DENIED"
    assert decision is not None and decision.granted is False and decision.step_id == "step_a"
    assert result is None
    try:
        store.decide(pending.approval_id, approved=True, approver_id="owner", session_id="session_x")
    except ValueError as exc:
        assert "not pending" in str(exc)
    else:
        raise AssertionError("denied approval must not be replayable")


def test_pending_approval_rejects_mismatched_plan_step() -> None:
    store = HostApprovalStore()
    try:
        store.create(
            request_id="request_x", decision=_decision("step_a"),
            plan_step={"step_id": "step_b"}, description="mismatch",
        )
    except ValueError as exc:
        assert "step_id" in str(exc)
    else:
        raise AssertionError("mismatched step scope must fail closed")
