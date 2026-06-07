from __future__ import annotations

from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_project_context_reader_contract import (
    build_jarvis_live_project_context_reader_contract,
)


def test_jarvis_live_project_context_reader_is_read_only_contract() -> None:
    read_model = build_jarvis_live_project_context_reader_contract().to_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["project_read_only_summary_allowed"] is True
    assert read_model["source_scope"] == "read_only_project_summary"
    assert "roadmap_status" in read_model["allowed_context_sources"]
    assert "jarvis_live_ci_status" in read_model["allowed_context_sources"]
    assert "architecture_summary" in read_model["allowed_context_sources"]
    assert "test_status_summary" in read_model["allowed_context_sources"]
    assert "voice_profile_summary" in read_model["allowed_context_sources"]
    assert read_model["source_file_mutation_allowed"] is False
    assert read_model["git_operation_allowed"] is False
    assert read_model["shell_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["memory_truth_write_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["pc_control_allowed"] is False

