import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    build_local_ai_workflow_proposal_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import (
    MobileWorkflowPermissionProfile,
    build_mobile_workflow_permission_profile,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract


def _proposal():
    return build_local_ai_workflow_proposal_contract(
        proposal_id="proposal.permission.001",
        requester_id="owner",
        graph=build_sample_workflow_graph_contract(),
        natural_language_goal="Create a local workflow proposal",
        requested_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        risk_level="medium",
    )


def test_mobile_workflow_permission_profile_allows_valid_permission_state() -> None:
    profile = build_mobile_workflow_permission_profile(
        profile_id="profile.android.owner",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )

    decision = profile.evaluate_proposal(_proposal())

    assert decision.allowed is True
    assert decision.reason_code == "allowed"
    assert profile.direct_phone_control_allowed is False
    assert profile.hidden_remote_control_allowed is False
    assert profile.direct_core_write_allowed is False
    assert profile.direct_server_canonical_write_allowed is False
    assert profile.network_socket_tunnel_allowed is False


def test_mobile_workflow_permission_profile_blocks_missing_permission_and_owner() -> None:
    profile_without_permission = build_mobile_workflow_permission_profile(
        profile_id="profile.no.permission",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=False,
        device_owner_confirmed=True,
    )
    assert profile_without_permission.evaluate_proposal(_proposal()).reason_code == "explicit_permission_missing"

    profile_without_owner = build_mobile_workflow_permission_profile(
        profile_id="profile.no.owner",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=False,
    )
    assert profile_without_owner.evaluate_proposal(_proposal()).reason_code == "device_owner_not_confirmed"


def test_mobile_workflow_permission_profile_blocks_missing_revoked_and_platform_capabilities() -> None:
    proposal = _proposal()

    missing_profile = build_mobile_workflow_permission_profile(
        profile_id="profile.missing.capability",
        platform="android",
        granted_capability_refs=("local_ai_workflow_proposal",),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    assert missing_profile.evaluate_proposal(proposal).reason_code == "capability_missing"

    revoked_profile = MobileWorkflowPermissionProfile(
        profile_id="profile.revoked.capability",
        platform="android",
        permission_source="user_settings",
        allowed_workflow_scopes=("local_app_workflow",),
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
        revoked_capability_refs=("explicit_user_approval",),
    )
    assert revoked_profile.evaluate_proposal(proposal).reason_code == "capability_revoked"

    platform_missing_profile = build_mobile_workflow_permission_profile(
        profile_id="profile.platform.missing",
        platform="ios",
        granted_capability_refs=("local_ai_workflow_proposal", "explicit_user_approval"),
        platform_capability_refs=("local_ai_workflow_proposal",),
        explicit_user_permission_granted=True,
        device_owner_confirmed=True,
    )
    assert platform_missing_profile.evaluate_proposal(proposal).reason_code == "platform_capability_missing"


def test_mobile_workflow_permission_profile_rejects_unsafe_flags() -> None:
    unsafe_flags = (
        {"direct_phone_control_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"runtime_mutation_allowed": True},
        {"platform_api_call_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            MobileWorkflowPermissionProfile(
                profile_id=f"profile.{next(iter(flag))}",
                platform="android",
                permission_source="user_settings",
                allowed_workflow_scopes=("local_app_workflow",),
                granted_capability_refs=("local_ai_workflow_proposal",),
                platform_capability_refs=("local_ai_workflow_proposal",),
                explicit_user_permission_granted=True,
                device_owner_confirmed=True,
                **flag,
            )
