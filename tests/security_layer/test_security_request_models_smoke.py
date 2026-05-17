from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)


def test_high_risk_request_requires_approval_and_voice_identity() -> None:
    request = build_security_request(
        request_id="sec_req_001",
        trace_id="trace_001",
        subject_id="owner",
        subject_kind=SecuritySubjectKind.OWNER,
        roles=("owner",),
        authenticated=True,
        resource_id="core",
        resource_kind=SecurityResourceKind.CORE,
        action=SecurityActionKind.EXECUTE,
        risk_level=SecurityRiskLevel.HIGH,
        source_layer_id="CONTROL_PLANE",
        target_layer_id="CORE_ROOT",
        reason="high risk command",
    )

    assert request.requires_approval is True
    assert request.requires_voice_identity is True
    assert request.dashboard_safe is True
    assert request.runtime_mutation_allowed is False
    assert request.canonical_write_allowed is False


def test_update_request_requires_signature() -> None:
    request = build_security_request(
        request_id="sec_req_update_001",
        trace_id="trace_update_001",
        subject_id="service",
        subject_kind=SecuritySubjectKind.SERVICE,
        roles=("update_service",),
        authenticated=True,
        resource_id="update_channel",
        resource_kind=SecurityResourceKind.UPDATE_RECOVERY,
        action=SecurityActionKind.UPDATE,
        risk_level=SecurityRiskLevel.MEDIUM,
        source_layer_id="UPDATE_RECOVERY",
        target_layer_id="CORE_ROOT",
        reason="update package",
    )

    assert request.requires_signature is True


def test_dashboard_subject_cannot_carry_execution_roles() -> None:
    with pytest.raises(ValueError, match="dashboard subjects"):
        build_security_request(
            request_id="sec_req_dashboard_001",
            trace_id="trace_dashboard_001",
            subject_id="dashboard",
            subject_kind=SecuritySubjectKind.DASHBOARD,
            roles=("operator",),
            authenticated=True,
            resource_id="runtime",
            resource_kind=SecurityResourceKind.EXECUTION_RUNTIME,
            action=SecurityActionKind.EXECUTE,
            risk_level=SecurityRiskLevel.LOW,
            source_layer_id="DASHBOARD",
            target_layer_id="EXECUTION_RUNTIME",
            reason="forbidden dashboard execution",
        )
