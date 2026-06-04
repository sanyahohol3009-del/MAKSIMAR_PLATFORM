import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.n8n_adapter_contract import (
    N8nAdapterContract,
    build_n8n_adapter_contract,
)


def test_n8n_adapter_contract_is_external_contract_only_boundary() -> None:
    adapter = build_n8n_adapter_contract()

    assert adapter.external_adapter_only is True
    assert adapter.contract_only is True
    assert adapter.requires_vendor_gate is True
    assert adapter.requires_sandbox_boundary is True
    assert adapter.requires_container_boundary is True
    assert adapter.n8n_is_core is False
    assert adapter.n8n_is_canonical_truth is False
    assert adapter.n8n_defines_workflow_truth is False
    assert adapter.download_allowed_now is False
    assert adapter.install_allowed_now is False
    assert adapter.runtime_execution_allowed_now is False
    assert adapter.direct_core_write_allowed is False
    assert adapter.direct_server_canonical_write_allowed is False
    assert adapter.network_allowed is False
    assert adapter.socket_allowed is False
    assert adapter.tunnel_allowed is False


def test_n8n_adapter_contract_rejects_core_truth_download_and_runtime_flags() -> None:
    unsafe_flags = (
        {"n8n_is_core": True},
        {"n8n_is_canonical_truth": True},
        {"n8n_defines_workflow_truth": True},
        {"download_allowed_now": True},
        {"install_allowed_now": True},
        {"runtime_execution_allowed_now": True},
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
            N8nAdapterContract(
                adapter_id=f"adapter.{next(iter(flag))}",
                adapter_mode="contract_only",
                adapter_location="external_server_adapter",
                supported_graph_semantics=("nodes",),
                supported_runtime_events=("intent_requested",),
                **flag,
            )
