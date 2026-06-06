from pathlib import Path

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_graph_contract import build_sample_workflow_graph_contract
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_status_bridge import (
    build_workflow_dashboard_read_only_projection,
    build_workflow_status_bridge_read_model,
)


ACCEPTANCE_DOC = Path("docs/architecture/workflow_engine/phase_6_workflow_automation_acceptance_v1.md")


PHASE_6_REQUIRED_FILES = (
    "docs/architecture/workflow_engine/phase_6_workflow_automation_registry_reconciliation_v1.md",
    "docs/architecture/workflow_engine/phase_6_mobile_local_workflow_semantic_decision_v1.md",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_graph_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_node_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_edge_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/local_workflow_scope_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/n8n_graph_compatibility_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/local_ai_workflow_proposal_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/mobile_workflow_permission_profile.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_approval_gate_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_audit_contract.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_safety_policy_contract.py",
    "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_adapter_contract.py",
    "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/workflow_runtime_policy.py",
    "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/workflow_execution_intent_runtime.py",
    "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_vendor_gate_runtime.py",
    "ANDROID_SHELL/workflow_adapter/android_local_workflow_intent_client.py",
    "IOS_SHELL/workflow_adapter/ios_local_workflow_intent_client.py",
    "MAKSIMAR_CORE_LIB/workflow_engine/workflow_status_bridge.py",
    "tools/workflow_status_preview.py",
    "CONTAINER_DEPLOYMENT/cubes/workflow_automation/container_contract.yaml",
    "CONTAINER_DEPLOYMENT/cubes/workflow_automation/runtime_profile.yaml",
    "CONTAINER_DEPLOYMENT/cubes/workflow_automation/network_policy.yaml",
)


def test_phase_6_acceptance_doc_contains_required_architecture_markers() -> None:
    text = ACCEPTANCE_DOC.read_text(encoding="utf-8")

    required_markers = (
        "PHASE 6 — Workflow Automation Acceptance v1",
        "Workflow Graph Contracts",
        "Workflow Governance Contracts",
        "Server Workflow Runtime / n8n Adapter Boundary",
        "Android/iOS Mobile Local Workflow Engine Boundary",
        "Workflow Dashboard / Preview / Container Contract",
        "n8n is accepted only as an external server adapter/container/runtime boundary",
        "Mobile remains a local-first JARVIS node",
        "The workflow dashboard surface is a read-model surface only",
        "network/socket/tunnel disabled by default",
        "No duplicate workflow root was created",
        "No parallel mobile workflow world was created",
        "No dashboard-to-execution path was created",
    )

    for marker in required_markers:
        assert marker in text


def test_phase_6_required_surfaces_exist() -> None:
    missing = [path for path in PHASE_6_REQUIRED_FILES if not Path(path).exists()]
    assert missing == []


def test_phase_6_workflow_status_bridge_is_read_only_and_non_executing() -> None:
    graph = build_sample_workflow_graph_contract()
    status = build_workflow_status_bridge_read_model(graph=graph)
    payload = status.to_read_model()
    projection = build_workflow_dashboard_read_only_projection()

    assert payload["dashboard_read_only"] is True
    assert payload["preview_read_only"] is True
    assert payload["status_bridge_only"] is True
    assert payload["runtime_execution_allowed"] is False
    assert payload["dashboard_execution_allowed"] is False
    assert payload["preview_execution_allowed"] is False
    assert payload["direct_core_write_allowed"] is False
    assert payload["direct_server_canonical_write_allowed"] is False
    assert payload["hidden_remote_control_allowed"] is False
    assert payload["direct_phone_control_allowed"] is False
    assert payload["network_disabled_by_default"] is True
    assert payload["socket_disabled_by_default"] is True
    assert payload["tunnel_disabled_by_default"] is True
    assert projection["execution_controls_enabled"] is False
    assert projection["mutation_controls_enabled"] is False
