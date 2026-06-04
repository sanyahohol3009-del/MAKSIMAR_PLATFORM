import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.local_workflow_scope_contract import (
    build_mobile_local_workflow_scope_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_edge_contract import WorkflowEdgeContract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import (
    WorkflowGraphContract,
    build_sample_workflow_graph_contract,
    validate_workflow_graph_contract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_node_contract import WorkflowNodeContract


def test_workflow_graph_contract_accepts_valid_mobile_local_graph() -> None:
    graph = build_sample_workflow_graph_contract()

    assert validate_workflow_graph_contract(graph) is True
    assert graph.local_scope.execution_tier == "mobile_local"
    assert graph.n8n_compatible is True
    assert graph.contract_only is True
    assert graph.execution_authority_allowed is False
    assert graph.direct_core_write_allowed is False
    assert graph.direct_server_canonical_write_allowed is False
    assert graph.network_socket_tunnel_allowed is False
    assert graph.hidden_remote_control_allowed is False
    assert graph.to_read_model()["node_count"] == 3


def test_workflow_graph_contract_rejects_duplicate_node_ids() -> None:
    node = WorkflowNodeContract(
        node_id="node.same",
        node_kind="trigger",
        display_name="Duplicate",
        n8n_compatible_type="n8n.manualTrigger",
        execution_tier="mobile_local",
    )

    with pytest.raises(ValueError):
        WorkflowGraphContract(
            graph_id="graph.duplicates",
            schema_version="phase6.graph.v1",
            display_name="Duplicate Graph",
            nodes=(node, node),
            edges=(),
            local_scope=build_mobile_local_workflow_scope_contract(),
        )


def test_workflow_graph_contract_rejects_edges_to_missing_nodes() -> None:
    node = WorkflowNodeContract(
        node_id="trigger.manual",
        node_kind="trigger",
        display_name="Manual Trigger",
        n8n_compatible_type="n8n.manualTrigger",
        execution_tier="mobile_local",
    )
    edge = WorkflowEdgeContract(
        edge_id="edge.missing",
        source_node_id="trigger.manual",
        target_node_id="missing.target",
    )

    with pytest.raises(ValueError):
        WorkflowGraphContract(
            graph_id="graph.missing.target",
            schema_version="phase6.graph.v1",
            display_name="Missing Target",
            nodes=(node,),
            edges=(edge,),
            local_scope=build_mobile_local_workflow_scope_contract(),
        )


def test_workflow_graph_contract_rejects_execution_authority_and_runtime_flags() -> None:
    graph = build_sample_workflow_graph_contract()

    unsafe_flags = (
        {"execution_authority_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"network_allowed": True},
        {"socket_allowed": True},
        {"tunnel_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"runtime_mutation_allowed": True},
        {"graph_defines_workflow_truth": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowGraphContract(
                graph_id=f"graph.{next(iter(flag))}",
                schema_version=graph.schema_version,
                display_name=graph.display_name,
                nodes=graph.nodes,
                edges=graph.edges,
                local_scope=graph.local_scope,
                **flag,
            )


def test_workflow_graph_contract_rejects_node_tier_outside_scope() -> None:
    server_node = WorkflowNodeContract(
        node_id="server.node",
        node_kind="action",
        display_name="Server Node",
        n8n_compatible_type="n8n.serverAction",
        execution_tier="server_local",
    )

    with pytest.raises(ValueError):
        WorkflowGraphContract(
            graph_id="graph.invalid.tier",
            schema_version="phase6.graph.v1",
            display_name="Invalid Tier",
            nodes=(server_node,),
            edges=(),
            local_scope=build_mobile_local_workflow_scope_contract(),
        )
