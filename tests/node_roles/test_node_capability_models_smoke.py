from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    NodeCapabilityContract,
    NodeCapabilityEntry,
)


def test_node_capability_models_build() -> None:
    """Node capability models should build successfully."""
    contract = NodeCapabilityContract(
        total_nodes=3,
        nodes=(
            NodeCapabilityEntry(
                node_id="mobile_001",
                node_type="mobile_node",
                heavy_execution_allowed=False,
                security_root=False,
                static_capacity_class="low_capacity",
                allowed_workload_classes=(
                    "ui_action",
                    "chat_request",
                ),
                feature_flags=(
                    "supports_low_latency_io",
                ),
            ),
            NodeCapabilityEntry(
                node_id="dev_001",
                node_type="dev_node",
                heavy_execution_allowed=True,
                security_root=False,
                static_capacity_class="medium_capacity",
                allowed_workload_classes=(
                    "chat_request",
                    "automation_job",
                    "evaluation_job",
                    "media_job",
                ),
                feature_flags=(
                    "supports_background_jobs",
                ),
            ),
            NodeCapabilityEntry(
                node_id="home_001",
                node_type="home_node",
                heavy_execution_allowed=True,
                security_root=False,
                static_capacity_class="high_capacity",
                allowed_workload_classes=(
                    "chat_request",
                    "automation_job",
                    "simulation_task",
                    "media_job",
                    "evaluation_job",
                ),
                feature_flags=(
                    "supports_background_jobs",
                    "supports_gpu",
                ),
            ),
        ),
    )

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.nodes[0].static_capacity_class == "low_capacity"
    assert contract.nodes[-1].static_capacity_class == "high_capacity"
    assert contract.nodes[-1].feature_flags[-1] == "supports_gpu"
