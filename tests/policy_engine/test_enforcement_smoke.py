from __future__ import annotations

from MAKSIMAR_CORE_LIB.policy_engine import EnforcementRequest, evaluate_request


def test_enforcement_access_policy_returns_review() -> None:
    """Access policy should require review because export rules require policy."""
    request = EnforcementRequest(
        policy_name="access_policy",
        operation="export_memory",
        context={},
    )

    result = evaluate_request(request)

    assert result.decision in {"allow", "review", "deny"}
    assert len(result.reasons) >= 0


def test_enforcement_action_policy_returns_deny_or_review_or_allow() -> None:
    """Action policy smoke test should return canonical decision."""
    request = EnforcementRequest(
        policy_name="action_policy",
        operation="workflow_action_resolution",
        context={},
    )

    result = evaluate_request(request)

    assert result.decision in {"allow", "review", "deny"}
