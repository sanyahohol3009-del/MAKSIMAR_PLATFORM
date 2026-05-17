from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.security_layer.security_decision_models import (
    SecurityDecision,
    SecurityDecisionStatus,
    build_security_decision_read_model,
    deny_security_request,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)


def test_deny_security_request_is_dashboard_safe() -> None:
    request = build_security_request(
        request_id="sec_req_deny_001",
        trace_id="trace_deny_001",
        subject_id="unknown",
        subject_kind=SecuritySubjectKind.UNKNOWN,
        roles=(),
        authenticated=False,
        resource_id="core",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.HIGH,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="unauthorized high risk",
    )

    decision = deny_security_request(
        request,
        reason_codes=("unauthorized_subject",),
        human_summary="Denied unauthorized high risk request.",
    )
    read_model = build_security_decision_read_model(decision)

    assert decision.action_execution_allowed is False
    assert read_model.status == "deny"
    assert read_model.dashboard_safe is True
    assert read_model.runtime_mutation_allowed is False


def test_non_allow_decision_cannot_execute() -> None:
    with pytest.raises(ValueError, match="only ALLOW decisions"):
        SecurityDecision(
            request_id="sec_req_bad",
            trace_id="trace_bad",
            status=SecurityDecisionStatus.DENY,
            risk_level=SecurityRiskLevel.LOW,
            reason_codes=("bad",),
            human_summary="bad",
            approval_required=False,
            voice_identity_required=False,
            signature_required=False,
            action_execution_allowed=True,
        )
