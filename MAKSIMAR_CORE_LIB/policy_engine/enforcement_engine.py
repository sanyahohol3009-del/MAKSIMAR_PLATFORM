from __future__ import annotations

from MAKSIMAR_CORE_LIB.policy_engine.enforcement_models import (
    EnforcementRequest,
    EnforcementResult,
)
from MAKSIMAR_CORE_LIB.policy_engine.enforcement_rules import (
    evaluate_approval_required,
    evaluate_forbidden_flags,
    evaluate_rules_text,
)
from MAKSIMAR_CORE_LIB.policy_engine.policy_accessor import get_policy


def evaluate_request(request: EnforcementRequest) -> EnforcementResult:
    """Evaluate one enforcement request against loaded policy.

    Current decision model:
    - explicit forbidden flag -> deny
    - explicit approval requirement -> review
    - otherwise -> allow

    Args:
        request: Enforcement request.

    Returns:
        Enforcement decision with reasons.
    """
    policy = get_policy(request.policy_name)
    payload = policy.payload

    forbidden_reasons = evaluate_forbidden_flags(payload)
    if forbidden_reasons:
        result = EnforcementResult(decision="deny")
        for reason in forbidden_reasons:
            result.add_reason(reason.path, reason.message)
        return result

    approval_reasons = evaluate_approval_required(payload)
    if approval_reasons:
        result = EnforcementResult(decision="review")
        for reason in approval_reasons:
            result.add_reason(reason.path, reason.message)

        for rule_reason in evaluate_rules_text(payload):
            result.add_reason(rule_reason.path, rule_reason.message)

        return result

    result = EnforcementResult(decision="allow")
    for rule_reason in evaluate_rules_text(payload):
        result.add_reason(rule_reason.path, rule_reason.message)

    return result
