import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import build_n8n_adapter_contract
from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.workflow_runtime_policy import (
    WorkflowRuntimePolicy,
    build_workflow_runtime_policy,
)


def test_workflow_runtime_policy_allows_external_adapter_contract_only() -> None:
    adapter = build_n8n_adapter_contract()
    policy = build_workflow_runtime_policy(adapter)

    assert policy.allows_adapter_contract(adapter) is True
    assert policy.server_optional_accelerator is True
    assert policy.intent_metadata_only is True
    assert policy.requires_vendor_gate_for_n8n is True
    assert policy.requires_sandbox_boundary_for_n8n is True
    assert policy.requires_container_boundary_for_n8n is True
    assert policy.runtime_execution_allowed_now is False
    assert policy.n8n_download_allowed_now is False
    assert policy.n8n_install_allowed_now is False
    assert policy.direct_core_write_allowed is False
    assert policy.direct_server_canonical_write_allowed is False
    assert policy.network_allowed is False
    assert policy.socket_allowed is False
    assert policy.tunnel_allowed is False


def test_workflow_runtime_policy_rejects_runtime_download_and_network_flags() -> None:
    unsafe_flags = (
        {"runtime_execution_allowed_now": True},
        {"n8n_download_allowed_now": True},
        {"n8n_install_allowed_now": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"dashboard_execution_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"direct_phone_control_allowed": True},
        {"network_allowed": True},
        {"socket_allowed": True},
        {"tunnel_allowed": True},
        {"runtime_mutation_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowRuntimePolicy(
                policy_id=f"policy.{next(iter(flag))}",
                runtime_mode="intent_metadata_only",
                allowed_adapter_ids=("phase6.n8n.external.adapter.v1",),
                allowed_execution_tiers=("mobile_local",),
                **flag,
            )
