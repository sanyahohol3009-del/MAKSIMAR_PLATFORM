import pytest

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_status_bridge import (
    WorkflowStatusBridgeReadModel,
    build_workflow_status_bridge_read_model,
)


def test_workflow_status_bridge_builds_read_only_status_model() -> None:
    model = build_workflow_status_bridge_read_model()
    payload = model.to_read_model()

    assert payload["bridge_id"] == "phase6.workflow.status.bridge.v1"
    assert payload["dashboard_read_only"] is True
    assert payload["preview_read_only"] is True
    assert payload["status_bridge_only"] is True
    assert payload["container_contract_declared"] is True
    assert payload["runtime_profile_declared"] is True
    assert payload["network_policy_declared"] is True
    assert payload["runtime_execution_allowed"] is False
    assert payload["dashboard_execution_allowed"] is False
    assert payload["preview_execution_allowed"] is False
    assert payload["direct_core_write_allowed"] is False
    assert payload["direct_server_canonical_write_allowed"] is False
    assert payload["network_disabled_by_default"] is True
    assert payload["socket_disabled_by_default"] is True
    assert payload["tunnel_disabled_by_default"] is True


def test_workflow_status_bridge_rejects_dashboard_execution_or_mutation_flags() -> None:
    unsafe_flags = (
        {"dashboard_read_only": False},
        {"preview_read_only": False},
        {"runtime_execution_allowed": True},
        {"dashboard_execution_allowed": True},
        {"preview_execution_allowed": True},
        {"direct_core_write_allowed": True},
        {"direct_server_canonical_write_allowed": True},
        {"hidden_remote_control_allowed": True},
        {"direct_phone_control_allowed": True},
        {"runtime_mutation_allowed": True},
        {"n8n_download_allowed_now": True},
        {"n8n_install_allowed_now": True},
        {"n8n_production_runtime_allowed": True},
    )

    for flag in unsafe_flags:
        with pytest.raises(ValueError):
            WorkflowStatusBridgeReadModel(
                bridge_id=f"bridge.{next(iter(flag))}",
                graph_id="graph.001",
                graph_schema_version="phase6.graph.v1",
                node_count=1,
                edge_count=0,
                execution_tier="mobile_local",
                status_panel_id="workflow.status",
                preview_tool_path="tools/workflow_status_preview.py",
                container_contract_path="CONTAINER_DEPLOYMENT/cubes/workflow_automation/container_contract.yaml",
                runtime_profile_path="CONTAINER_DEPLOYMENT/cubes/workflow_automation/runtime_profile.yaml",
                network_policy_path="CONTAINER_DEPLOYMENT/cubes/workflow_automation/network_policy.yaml",
                visible_status_items=("graph_contract",),
                readiness_flags=("ready",),
                **flag,
            )
