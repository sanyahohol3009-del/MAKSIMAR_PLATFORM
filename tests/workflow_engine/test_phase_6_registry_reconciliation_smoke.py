from tools.project_readiness_control.roadmap_expected_files_registry import get_expected_batch


def test_phase_6_batches_are_registered_with_expected_titles() -> None:
    expected_titles = {
        "6.0": "PHASE 6 Registry Reconciliation / Mobile Local Workflow Correction",
        "6.1": "Workflow Graph Contracts",
        "6.2": "Workflow Governance Contracts",
        "6.3": "Server Workflow Runtime / n8n Adapter Boundary",
        "6.4": "Android/iOS Mobile Local Workflow Engine Boundary",
        "6.5": "Workflow Dashboard / Preview / Container Contract",
        "6.6": "PHASE 6 Acceptance",
    }

    for batch_id, title in expected_titles.items():
        batch = get_expected_batch(batch_id)

        assert batch.title == title
        assert batch.expected_files


def test_phase_6_reconciliation_batch_tracks_docs_and_tests() -> None:
    batch = get_expected_batch("6.0")
    paths = {entry.path for entry in batch.expected_files}

    assert "docs/architecture/workflow_engine/phase_6_workflow_automation_registry_reconciliation_v1.md" in paths
    assert "docs/architecture/workflow_engine/phase_6_mobile_local_workflow_semantic_decision_v1.md" in paths
    assert "tests/workflow_engine/test_phase_6_registry_reconciliation_smoke.py" in paths
    assert "tests/workflow_engine/test_phase_6_mobile_local_workflow_semantic_decision_smoke.py" in paths


def test_phase_6_registry_extends_existing_workflow_surfaces() -> None:
    graph_batch = get_expected_batch("6.1")
    mobile_batch = get_expected_batch("6.4")

    graph_paths = {entry.path for entry in graph_batch.expected_files}
    mobile_paths = {entry.path for entry in mobile_batch.expected_files}

    assert "MAKSIMAR_CORE_LIB/workflow_engine/workflow_graph_contract.py" in graph_paths
    assert "ANDROID_SHELL/workflow_adapter/android_local_workflow_intent_client.py" in mobile_paths
    assert "IOS_SHELL/workflow_adapter/ios_local_workflow_intent_client.py" in mobile_paths
    assert not any(path.startswith("WORKFLOW_CORE/") for path in graph_paths | mobile_paths)
