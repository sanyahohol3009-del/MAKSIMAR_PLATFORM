import pytest

from IOS_SHELL.workflow_adapter.ios_workflow_capability_limits import (
    IOSWorkflowCapabilityLimits,
    build_ios_workflow_capability_limits,
)
from IOS_SHELL.workflow_adapter.ios_workflow_permission_bridge import (
    IOSWorkflowPermissionBridge,
    build_ios_workflow_permission_bridge,
)
from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract


def _proposal():
    return build_local_ai_workflow_proposal_contract(
        proposal_id="proposal.ios.permission.001",
        requester_id="owner",
        graph=build_sample_workflow_graph_contract(),
        natural_language_goal="Create iOS local workflow intent metadata",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level="medium",
    )


def test_ios_permission_bridge_allows_explicit_permission_and_owner_confirmed() -> None:
    bridge = build_ios_workflow_permission_bridge(
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )

    result = bridge.evaluate_proposal(_proposal())

    assert result.permission_decision.allowed is True
    assert result.permission_decision.reason_code == "allowed"
    assert result.permission_profile.platform == "ios"
    assert bridge.direct_phone_control_allowed is False
    assert bridge.hidden_remote_control_allowed is False
    assert bridge.direct_core_write_allowed is False
    assert bridge.direct_server_canonical_write_allowed is False
    assert bridge.network_allowed_by_default is False


def test_ios_permission_bridge_blocks_missing_explicit_permission_and_missing_capability() -> None:
    no_permission = build_ios_workflow_permission_bridge(
        explicit_user_permission_granted=False,
        device_owner_confirmed=True,
    )
    assert no_permission.evaluate_proposal(_proposal()).permission_decision.reason_code == "explicit_permission_missing"

    limited = IOSWorkflowCapabilityLimits(
        limits_id="ios.limited",
        allowed_capability_refs=("local_ai_workflow_proposal",),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
    )
    bridge = build_ios_workflow_permission_bridge(
        capability_limits=limited,
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    assert bridge.evaluate_proposal(_proposal()).permission_decision.reason_code == "capability_missing"


def test_ios_capability_limits_reject_hidden_remote_and_phone_control() -> None:
    with pytest.raises(ValueError):
        IOSWorkflowCapabilityLimits(
            limits_id="ios.hidden.remote",
            allowed_capability_refs=("local_ai_workflow_proposal",),
            platform_capability_refs=("local_ai_workflow_proposal",),
            hidden_remote_control_allowed=True,
        )

    with pytest.raises(ValueError):
        IOSWorkflowPermissionBridge(
            bridge_id="ios.direct.phone",
            capability_limits=build_ios_workflow_capability_limits(),
            explicit_user_permission_granted=True,
            device_owner_confirmed=True,
            direct_phone_control_allowed=True,
        )
