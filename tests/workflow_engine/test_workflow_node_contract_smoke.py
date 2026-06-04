import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_node_contract import WorkflowNodeContract


def test_workflow_node_contract_accepts_valid_contract_only_node() -> None:
    node = WorkflowNodeContract(
        node_id="trigger.manual",
        node_kind="trigger",
        display_name="Manual Trigger",
        n8n_compatible_type="n8n.manualTrigger",
        execution_tier="mobile_local",
        capability_refs=("local_app_workflow",),
    )

    assert node.node_id == "trigger.manual"
    assert node.contract_only is True
    assert node.execution_authority_allowed is False
    assert node.direct_core_write_allowed is False
    assert node.direct_server_canonical_write_allowed is False
    assert node.network_socket_tunnel_allowed is False
    assert node.hidden_remote_control_allowed is False
    assert node.to_read_model()["execution_tier"] == "mobile_local"


def test_workflow_node_contract_rejects_invalid_identity_and_kind() -> None:
    with pytest.raises(ValueError):
        WorkflowNodeContract(
            node_id="",
            node_kind="trigger",
            display_name="Manual Trigger",
            n8n_compatible_type="n8n.manualTrigger",
            execution_tier="mobile_local",
        )

    with pytest.raises(ValueError):
        WorkflowNodeContract(
            node_id="node.invalid",
            node_kind="runtime_executor",
            display_name="Invalid",
            n8n_compatible_type="n8n.invalid",
            execution_tier="mobile_local",
        )


def test_workflow_node_contract_rejects_execution_and_hidden_control_authority() -> None:
    with pytest.raises(ValueError):
        WorkflowNodeContract(
            node_id="node.exec",
            node_kind="action",
            display_name="Unsafe Execution",
            n8n_compatible_type="n8n.executeCommand",
            execution_tier="mobile_local",
            execution_authority_allowed=True,
        )

    with pytest.raises(ValueError):
        WorkflowNodeContract(
            node_id="node.remote",
            node_kind="action",
            display_name="Hidden Remote Control",
            n8n_compatible_type="n8n.remoteControl",
            execution_tier="mobile_local",
            hidden_remote_control_allowed=True,
        )


def test_workflow_node_contract_rejects_core_server_and_network_authority() -> None:
    unsafe_flags = (
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_allowed": True},
        {"socket_allowed": True},
        {"tunnel_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"runtime_mutation_allowed": True},
        {"platform_api_call_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowNodeContract(
                node_id=f"node.{next(iter(flag))}",
                node_kind="action",
                display_name="Unsafe Node",
                n8n_compatible_type="n8n.unsafe",
                execution_tier="mobile_local",
                **flag,
            )
