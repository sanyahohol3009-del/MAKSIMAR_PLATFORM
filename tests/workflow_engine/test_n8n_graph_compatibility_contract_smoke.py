import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.n8n_graph_compatibility_contract import (
    N8nGraphCompatibilityContract,
    build_n8n_graph_compatibility_contract,
    validate_n8n_compatible_graph,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract


def test_n8n_graph_compatibility_accepts_contract_only_graph_semantics() -> None:
    compatibility = build_n8n_graph_compatibility_contract()
    graph = build_sample_workflow_graph_contract()

    assert validate_n8n_compatible_graph(graph, compatibility) is True
    assert compatibility.n8n_is_core is False
    assert compatibility.mobile_embeds_n8n is False
    assert compatibility.n8n_defines_workflow_truth is False
    assert compatibility.execution_allowed is False
    assert compatibility.network_socket_tunnel_allowed is False
    assert compatibility.runtime_mutation_allowed is False
    assert compatibility.to_read_model()["adapter_boundary"] == "external_server_adapter_container_runtime"


def test_n8n_graph_compatibility_rejects_core_embedding_and_runtime_authority() -> None:
    unsafe_flags = (
        {"n8n_is_core": True},
        {"mobile_embeds_n8n": True},
        {"n8n_defines_workflow_truth": True},
        {"execution_allowed": True},
        {"network_allowed": True},
        {"socket_allowed": True},
        {"tunnel_allowed": True},
        {"network_socket_tunnel_allowed": True},
        {"runtime_mutation_allowed": True},
        {"contract_only": False},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            N8nGraphCompatibilityContract(**flag)


def test_n8n_graph_compatibility_rejects_unsupported_graph_semantics() -> None:
    graph = build_sample_workflow_graph_contract()
    compatibility = N8nGraphCompatibilityContract(
        supported_node_kinds=("action",),
        supported_edge_kinds=("main", "approval"),
        supported_execution_tiers=("mobile_local",),
    )

    with pytest.raises(ValueError):
        validate_n8n_compatible_graph(graph, compatibility)


def test_n8n_graph_compatibility_rejects_empty_supported_values() -> None:
    with pytest.raises(ValueError):
        N8nGraphCompatibilityContract(supported_node_kinds=())

    with pytest.raises(ValueError):
        N8nGraphCompatibilityContract(supported_edge_kinds=())

    with pytest.raises(ValueError):
        N8nGraphCompatibilityContract(supported_execution_tiers=())
