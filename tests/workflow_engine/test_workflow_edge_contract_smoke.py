import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_edge_contract import WorkflowEdgeContract


def test_workflow_edge_contract_accepts_valid_n8n_like_connection() -> None:
    edge = WorkflowEdgeContract(
        edge_id="edge.trigger.to.action",
        source_node_id="trigger.manual",
        target_node_id="action.prepare",
        source_handle="main",
        target_handle="main",
        edge_kind="main",
        n8n_connection_type="main",
    )

    assert edge.referenced_node_ids() == ("trigger.manual", "action.prepare")
    assert edge.to_read_model()["n8n_connection_type"] == "main"


def test_workflow_edge_contract_rejects_empty_fields() -> None:
    with pytest.raises(ValueError):
        WorkflowEdgeContract(
            edge_id="",
            source_node_id="trigger.manual",
            target_node_id="action.prepare",
        )

    with pytest.raises(ValueError):
        WorkflowEdgeContract(
            edge_id="edge.empty.target",
            source_node_id="trigger.manual",
            target_node_id="",
        )


def test_workflow_edge_contract_rejects_self_loop() -> None:
    with pytest.raises(ValueError):
        WorkflowEdgeContract(
            edge_id="edge.self",
            source_node_id="node.same",
            target_node_id="node.same",
        )


def test_workflow_edge_contract_rejects_unknown_kinds() -> None:
    with pytest.raises(ValueError):
        WorkflowEdgeContract(
            edge_id="edge.unknown",
            source_node_id="trigger.manual",
            target_node_id="action.prepare",
            edge_kind="runtime_dispatch",
        )

    with pytest.raises(ValueError):
        WorkflowEdgeContract(
            edge_id="edge.connection.unknown",
            source_node_id="trigger.manual",
            target_node_id="action.prepare",
            n8n_connection_type="raw_socket",
        )
