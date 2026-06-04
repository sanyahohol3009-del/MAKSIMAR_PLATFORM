import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.local_workflow_scope_contract import (
    LocalWorkflowScopeContract,
    build_default_local_workflow_scopes,
    build_mobile_local_workflow_scope_contract,
)


def test_mobile_local_workflow_scope_is_local_first_and_server_optional() -> None:
    scope = build_mobile_local_workflow_scope_contract()

    assert scope.workflow_scope == "local_app_workflow"
    assert scope.execution_tier == "mobile_local"
    assert scope.mobile_local_first is True
    assert scope.server_optional is True
    assert scope.explicit_permission_required is True
    assert scope.user_approval_required is True
    assert scope.audit_visible is True
    assert scope.dashboard_visible is True
    assert scope.execution_authority_allowed is False
    assert scope.direct_core_write_allowed is False
    assert scope.direct_server_canonical_write_allowed is False
    assert scope.network_socket_tunnel_allowed is False
    assert scope.hidden_remote_control_allowed is False


def test_default_local_workflow_scopes_cover_all_execution_tiers() -> None:
    scopes = build_default_local_workflow_scopes()
    tiers = {scope.execution_tier for scope in scopes}

    assert tiers == {"mobile_local", "server_local", "hybrid", "cloud_optional"}


def test_local_workflow_scope_rejects_invalid_scope_and_tier() -> None:
    with pytest.raises(ValueError):
        LocalWorkflowScopeContract(
            scope_id="invalid.scope",
            workflow_scope="remote_control_workflow",
            execution_tier="mobile_local",
            mobile_local_first=True,
        )

    with pytest.raises(ValueError):
        LocalWorkflowScopeContract(
            scope_id="invalid.tier",
            workflow_scope="local_app_workflow",
            execution_tier="unbounded_runtime",
            mobile_local_first=True,
        )


def test_local_workflow_scope_requires_permission_approval_and_audit() -> None:
    unsafe_flags = (
        {"explicit_permission_required": False},
        {"user_approval_required": False},
        {"audit_visible": False},
        {"dashboard_visible": False},
        {"execution_authority_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"runtime_mutation_allowed": True},
        {"platform_api_call_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            LocalWorkflowScopeContract(
                scope_id=f"scope.{next(iter(flag))}",
                workflow_scope="local_app_workflow",
                execution_tier="mobile_local",
                mobile_local_first=True,
                **flag,
            )
